from __future__ import annotations

from dataclasses import dataclass, field
from re import L, M
from typing import Any, List, Mapping, Optional, Tuple

from . import multipart
from .common import Location, MultiValuesDict, Request, Schema, Value, multivalues_factory
from .serializers import Serializer, get_serializer
from .validators import validate


@dataclass
class Parameter:
    name: str
    schema: Schema
    serializer: Serializer
    required: bool = False

    def deserialize(self, variables):
        return self.serializer.deserialize(variables)

    def validate(self, value: Any):
        if value == Value.MISSING and self.required:
            return value, ["Mandatory"]
        return validate(self.schema, value)


@dataclass
class Parameters:
    parameters: Mapping[str, Parameter] = field(default_factory=dict)

    def deserialize(self, variables: Mapping[str, str]):
        values = {}
        errors = []
        for field, parameter in self.parameters.items():
            values[field], variables, errs = parameter.deserialize(variables)
            if errs:
                errors.append((field, errs))
        return values, variables, errors

    def validate(self, values: Mapping[str, Any]):
        values = dict(values)
        errors = []
        for field, parameter in self.parameters.items():
            value = values.get(field, Value.MISSING)
            values[field], errs = parameter.validate(value)
            if errs:
                errors.append((field, errs))
        return values, errors


@dataclass
class Query:
    parameters: Mapping[str, Parameter] = field(default_factory=dict)

    def deserialize(self, payload: str):
        variables = multivalues_factory(payload)
        values = {}
        errors = []
        for field, parameter in self.parameters.items():
            values[field], variables, errs = parameter.deserialize(variables)
            if errs:
                errors.append((field, errs))
        return values, variables, errors

    def validate(self, values: Mapping[str, Any]):
        values = dict(values)
        errors = []
        for field, parameter in self.parameters.items():
            value = values.get(field, Value.MISSING)
            values[field], errs = parameter.validate(value)
            if errs:
                errors.append((field, errs))
        return values, errors


@dataclass
class Body:
    contents: Mapping[str, BodyContent]
    required: bool = False

    def find_content(self, media_type: str) -> Tuple[Optional[str], Optional[BodyContent], List]:
        if media_type is None:
            return None, None, [(Location.HEADER, "Content-Type", ["Mandatory"]), "Required media-type",]
        if content := self.contents.get(media_type):
            return media_type, content, []
        main_content = "%s/*" % media_type.partition("/")[0]
        if content := self.contents.get(main_content):
            return main_content, content, []
        if content := self.contents.get("/*"):
            return "*/*", content, []
        return None, None, [(Location.HEADER, "Content-Type", ["Unhandled media-type"]), "Unhandled media-type"]

    def deserialize(self, request: Request):
        _, content, errors = self.find_content(request.content_type)
        if not errors:
            return content.deserialize(request)
        return Value.DISCARDED, None, errors


def load_parameters(payload):
    locations: Mapping[Location, Parameters] = {
        Location.QUERY: Query(),
        Location.PATH: Parameters(),
        Location.HEADER: Parameters(),
        Location.COOKIE: Parameters(),
    }
    for parameter in payload:
        location = parameter["in"]
        name = parameter["name"]
        locations[Location(location)].parameters[name] = load_parameter(parameter)
    return locations


def load_parameter(payload) -> Parameter:
    location = payload["in"]
    if location == "path":
        return load_path_parameter(payload)
    elif location == "query":
        return load_query_parameter(payload)
    elif location == "header":
        return load_header_parameter(payload)
    elif location == "cookie":
        return load_cookie_parameter(payload)
    raise NotImplementedError


def load_path_parameter(payload) -> Parameter:
    location = payload["in"]
    name = payload["name"]
    required = payload.get("required", True)
    if c := payload.get("content", []):
        content_type = next(iter(c))
        schema = c[content_type].get("schema", True)
        serializer = get_serializer(content_type=content_type, name=name, schema=schema)
    else:
        style = payload.get("style", "simple")
        explode = payload.get("explode", False)
        schema = payload.get("schema", True)
        serializer = get_serializer(location=location, style=style, explode=explode, name=name, schema=schema)
    return Parameter(name, schema=schema, serializer=serializer, required=required)


def load_query_parameter(payload) -> Parameter:
    location = payload["in"]
    name = payload["name"]
    required = payload.get("required", False)
    if c := payload.get("content", []):
        content_type = next(iter(c))
        schema = c[content_type].get("schema", True)
        serializer = get_serializer(content_type=content_type, name=name, schema=schema)
    else:
        style = payload.get("style", "form")
        explode = payload.get("explode", True)
        schema = payload.get("schema", True)
        serializer = get_serializer(location=location, style=style, explode=explode, name=name, schema=schema)
    return Parameter(name, schema=schema, serializer=serializer, required=required)


def load_header_parameter(payload) -> Parameter:
    location = payload["in"]
    name = payload["name"]
    required = payload.get("required", False)
    if c := payload.get("content", []):
        content_type = next(iter(c))
        schema = c[content_type].get("schema", True)
        serializer = get_serializer(content_type=content_type, name=name, schema=schema)
    else:
        style = payload.get("style", "simple")
        explode = payload.get("explode", False)
        schema = payload.get("schema", True)
        serializer = get_serializer(location=location, style=style, explode=explode, name=name, schema=schema)
    return Parameter(name, schema=schema, serializer=serializer, required=required)


def load_cookie_parameter(payload) -> Parameter:
    location = payload["in"]
    name = payload["name"]
    required = payload.get("required", False)
    if c := payload.get("content", []):
        content_type = next(iter(c))
        schema = c[content_type].get("schema", True)
        serializer = get_serializer(content_type=content_type, name=name, schema=schema)
    else:
        style = payload.get("style", "form")
        explode = payload.get("explode", True)
        schema = payload.get("schema", True)
        serializer = get_serializer(location=location, style=style, explode=explode, name=name, schema=schema)
    return Parameter(name, schema=schema, serializer=serializer, required=required)


def load_body(payload) -> Body:
    required = payload.get("required", False)
    contents = {}
    for content_type, content in payload.get("content", {}).items():
        if content_type == "application/x-www-form-urlencoded":
            loaded_content = load_body_form(content_type, content)
        elif content_type == "multipart/form-data":
            loaded_content = load_body_multipart(content_type, content)
        elif content_type == "application/json":
            loaded_content = load_body_json(content_type, content)
        elif content_type == "application/xml":
            loaded_content = load_body_xml(content_type, content)
        else:
            loaded_content = load_body_document(content_type, content)
        contents[content_type] = loaded_content
    return Body(contents, required)


def load_body_json(content_type, payload):
    schema = payload["schema"]
    return JSONContent(schema=schema)


def load_body_xml(content_type, payload):
    schema = payload["schema"]
    return XMLContent(schema=schema)


def load_body_form(content_type, payload):
    parameters = {}
    for name, schema in payload["schema"]["properties"].items():
        encoding = payload.get("encoding", {}).get(name, {})
        parameters[name] = load_body_form_parameter(name, schema, encoding)
    return FormContent(parameters=parameters)


def load_body_form_parameter(name, schema, encoding):
    if "style" in encoding or "explode" in encoding:
        style = encoding.get("style", "form")
        explode = encoding.get("explode", True)
        serializer = get_serializer(name=name, style=style, explode=explode, schema=schema)
    elif content_type := encoding.get("contentType"):
        serializer = get_serializer(name=name, content_type=content_type, schema=schema)
    else:
        serializer = get_serializer(name=name, style="form", explode=True, schema=schema)
    return Parameter(name, schema=schema, serializer=serializer)


def load_body_multipart(content_type, payload):
    parameters = {}
    for name, schema in payload["schema"]["properties"].items():
        encoding = payload.get("encoding", {}).get(name, {})
        parameters[name] = load_body_multipart_parameter(name, schema, encoding)
    return MultipartContent(parameters=parameters)


def load_body_multipart_parameter(name, schema, encoding):
    # When passing complex objects in the application/x-www-form-urlencoded content type, the default serialization strategy of such properties is described in the Encoding Object's style property as form.
    if "style" in encoding or "explode" in encoding:
        style = encoding.get("style", "form")
        explode = encoding.get("explode", True)
        serializer = get_serializer(name=name, style=style, explode=explode, schema=schema)
    elif content_type := encoding.get("contentType"):
        serializer = get_serializer(name=name, content_type=content_type, schema=schema)
    elif schema["type"] in ("string", "number", "integer", "boolean", "null"):
        content_type = "text/plain"
        serializer = get_serializer(name=name, content_type=content_type, style="form", explode=True, schema=schema)
    elif schema["type"] == "array" and schema["items"]["type"] in ("string", "number", "integer", "boolean", "null"):
        content_type = "text/plain"
        serializer = get_serializer(name=name, content_type=content_type, style="form", explode=True, schema=schema)
    elif schema["type"] in ("object", "array"):
        content_type = "application/json"
        serializer = get_serializer(name=name, content_type=content_type, schema=schema)
    else:
        serializer = get_serializer(name=name, style="form", explode=True, schema=schema)
    return Parameter(name, schema=schema, serializer=serializer)


def load_body_document(content_type, payload):
    return DocumentContent(content_type=content_type)


class BodyContent:
    def deserialize(self, request: Request):
        raise NotImplementedError

    def validate(self, values):
        raise NotImplementedError


@dataclass
class FormContent(BodyContent):
    parameters: Mapping[str, Parameter]

    def deserialize(self, request: Request):
        variables = multivalues_factory(request.read().decode("utf-8"))
        values = {}
        errors = []
        for field, parameter in self.parameters.items():
            values[field], variables, errs = parameter.deserialize(variables)
            if errs:
                errors.append((field, errs))
        return values, variables, errors


@dataclass
class Part:
    body: bytes
    content_type: str


@dataclass
class MultipartContent(BodyContent):
    parameters: Mapping[str, Parameter]

    def deserialize(self, request: Request):
        fields, _ = multipart.decode_data(request.read(), request.headers)
        variables = {}
        for name, body, content_type, filename in fields:
            if content_type == "text/plain":
                body = body.decode("utf-8")
            variables.setdefault(name, []).append(body)
        variables = MultiValuesDict(variables)
        values = {}
        errors = []
        for field, parameter in self.parameters.items():
            values[field], variables, errs = parameter.deserialize(variables)
            if errs:
                errors.append((field, errs))
        return values, variables, errors


@dataclass
class JSONContent(BodyContent):
    schema: Schema

    def deserialize(self, request: Request):
        import json

        value = json.loads(request.read())
        return value, b"", []

    def validate(self, values: Mapping):
        return validate(self.schema, values)


@dataclass
class XMLContent(BodyContent):
    schema: Schema

    def deserialize(self, request: Request):
        raise NotImplementedError


@dataclass
class DocumentContent(BodyContent):
    content_type: str

    def deserialize(self, request: Request):
        return request.body, b"", []
