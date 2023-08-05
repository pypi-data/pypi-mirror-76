from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cached_property, wraps
from typing import Any, Iterator, List, Mapping, Optional, Set, Tuple

from ades.common import Location, Request, Value

from .loaders import load_body, load_parameters


def cast_list(meth):
    @wraps(meth)
    def inner(self):
        return list(meth(self))

    return inner


class Ades:
    def __init__(self, sources: List[Mapping]):
        self.sources = sources

    def filter(self, uri: str, method: str) -> Iterator[MatchedUri]:
        for operation in self.operations:
            yield from operation.match_uri(uri, method)

    @cached_property
    def specs(self) -> List[Spec]:
        return [Spec(source) for source in self.sources]

    @cached_property
    @cast_list
    def operations(self) -> List[Operation]:
        for spec in self.specs:
            yield from spec.operations


@dataclass
class Spec:
    document: Mapping

    @cached_property
    @cast_list
    def paths(self) -> List[Path]:
        servers = self.document.get("servers") or [{"url": "/"}]
        for path, doc in self.document.get("paths", {}).items():
            doc = dict(doc)
            doc.setdefault("servers", servers)
            yield Path(path, doc)

    @cached_property
    @cast_list
    def operations(self) -> List[Operation]:
        for path in self.paths:
            yield from path.operations


@dataclass
class Path:
    path: str
    document: Mapping

    @cached_property
    @cast_list
    def operations(self) -> List[Operation]:
        path = self.path
        parameters = self.document.get("parameters") or []
        servers = self.document.get("servers") or [{"url": "/"}]
        for method in ("get", "put", "post", "delete", "options", "head", "patch", "trace"):
            if doc := self.document.get(method):
                doc = dict(doc)
                doc.setdefault("servers", list(servers))
                doc.setdefault("parameters", []).extend(parameters)
                yield Operation(method, path, doc)


@dataclass
class Operation:
    method: str
    path: str
    document: Mapping = field(repr=False)

    @cached_property
    def uri_templates(self) -> List[re.Pattern]:
        uri_templates = []
        path_pattern = get_path_pattern(self.path)
        for server in self.document.get("servers", {"url": "/"}):
            server_pattern = get_server_pattern(server)
            pattern = "%s/%s" % (server_pattern.rstrip("/"), path_pattern.lstrip("/"))
            uri_templates.append(re.compile(pattern))
        return uri_templates

    @cached_property
    def parameters(self):
        parameters = self.document.get("parameters") or []
        return load_parameters(parameters)

    @cached_property
    def request_body(self):
        request_body = self.document.get("requestBody", {})
        return load_body(request_body)

    def match_uri(self, uri: str, method: str) -> Iterator[MatchedUri]:
        if method == self.method:
            for uri_template in self.uri_templates:
                if match := uri_template.fullmatch(uri):
                    variables = match.groupdict()
                    yield MatchedUri(self, variables)

    def validate(self, request):
        full = {}
        full[Location.PATH], errors = self.validate_parameters(Location.PATH, request.path_variables)

        if not errors:
            full[Location.HEADER], errors = self.validate_parameters(Location.HEADER, request.headers)

        if not errors:
            full[Location.COOKIE], errors = self.validate_parameters(Location.COOKIE, request.cookies)

        if not errors:
            full[Location.QUERY], errors = self.validate_parameters(Location.QUERY, request.query_string)

        if not errors and request.method in ["post", "patch", "put"]:
            full[Location.BODY], errors = self.validate_body(request)

        if errors:
            return failure(full, errors)

        return success(full)

    def validate_parameters(self, location: Location, payload):
        parameters = self.parameters[location]
        values, variables, errors = parameters.deserialize(payload)
        values = {**variables, **values}
        if not errors:
            values, errors = parameters.validate(values)
        errors = fix_errors_location(errors, location)
        return values, errors

    def validate_body(self, request: Request):
        values = Value.DISCARDED
        _, content, errors = self.request_body.find_content(request.content_type)
        if not errors:
            values, payload, errors = content.deserialize(request)
            if payload:
                # TODO: it should have no remaining payload?!?
                raise NotImplementedError
            if not errors:
                values, errors = content.validate(values)
        errors = fix_errors_location(errors, Location.BODY)
        return values, errors


@dataclass
class Validation:
    value: Any = field(default=Value.MISSING)
    errors: List = field(default_factory=list)

    def __bool__(self):
        return not self.errors


@dataclass
class Report:
    result: bool
    headers: Mapping[str, Validation] = field(default_factory=dict)
    query: Mapping[str, Validation] = field(default_factory=dict)
    cookie: Mapping[str, Validation] = field(default_factory=dict)
    body: Optional[Validation] = None

    def __bool__(self):
        return self.result


def failure(full, errors):
    result = True
    report = {location: defaultdict(Validation) for location in Location}
    for location, key, errs in errors:
        report[location][key].errors.extend(errs)
        result = False
    for location, keys in full.items():
        if not isinstance(keys, dict):
            keys = {None: keys}
        # if location == Location.BODY and not isinstance(keys, dict):
        #     report[location] = Validation(value=keys)
        #     continue
        for key, value in keys.items():
            report[location][key].value = value
    return Report(
        result=result,
        headers=dict(report[Location.HEADER]),
        query=dict(report[Location.QUERY]),
        body=dict(report[Location.BODY]),
    )


def success(full):
    return failure(full, [])


def fix_errors_location(errors: List, location: Location) -> Iterator[Tuple[Location, Optional[str], List[str]]]:
    errors = list(do_fix_errors_location(errors, location))
    return errors


def do_fix_errors_location(errors: List, location: Location) -> Iterator[Tuple[Location, Optional[str], List[str]]]:
    for err in errors:
        if isinstance(err, str):
            err = (location, None, [err])
        elif isinstance(err, list):
            err = (location, None, err)
        elif isinstance(err, tuple) and len(err) == 2:
            err = (location, *err)
        yield err


@dataclass
class MatchedUri:
    operation: Operation
    variables: Mapping


def get_server_pattern(server: Mapping):
    pattern: str = server.get("url")
    if variables := server.get("variables"):
        for field, doc in variables.items():
            values = set(doc.get("enum") or [])
            if default := doc.get("default"):
                values.add(default)
            values = sorted(values)
            values = "'(%s)" % "|".join(re.escape(val) for val in values)
            pattern = pattern.replace(f"{{{field}}}", values)
    return pattern


def get_path_pattern(path: str):
    pattern = re.sub(r"\{(\w+)\}", r"(?P<\1>.+?)", path)
    return pattern
