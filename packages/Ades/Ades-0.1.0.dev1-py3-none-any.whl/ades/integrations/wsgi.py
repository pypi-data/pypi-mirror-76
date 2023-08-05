import wsgiref.util
from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from tempfile import SpooledTemporaryFile
from typing import Any, List, Mapping, Union

from ades import Ades
from ades.common import Value, Request


class WSGIMiddleware:
    def __init__(self, app, sources):
        self.app = app
        self.ades = Ades(sources)

    def __call__(self, environ, start_response):
        environ, operation = self.validate_request(environ)
        response = self.app(environ, start_response)
        response = self.validate_response(environ, operation)
        return response

    def validate_request(self, environ):
        request = WSGIRequest(environ)
        for match in self.ades.filter(uri=request.uri, method=request.method):
            validated = match.operation.validate(request=MatchedRequest(request, match.variables))
            environ["ades.matched_uri"] = match
            environ["ades.validated"] = validated
            return environ, match
        environ["ades.matched_uri"] = None
        return environ, None

    def validate_response(self, response, operation):
        return response


@dataclass
class MatchedRequest(Request):
    request: Request
    path_variables: Mapping[str, str]

    def __getattr__(self, name):
        return getattr(self.request, name)

    def read(self):
        return self.request.read()


@dataclass
class WSGIRequest:
    environ: Mapping[str, Any]

    @cached_property
    def content_type(self):
        if content_type := self.environ.get("CONTENT_TYPE"):
            return content_type.partition(";")[0].strip()

    @cached_property
    def uri(self) -> str:
        return wsgiref.util.request_uri(dict(self.environ), include_query=False)

    @cached_property
    def query_string(self) -> str:
        return self.environ.get("QUERY_STRING", "")

    @cached_property
    def query(self) -> Mapping[str, Union[List[str], Value]]:
        query = {}
        if query_string := self.query_string:
            for q in query_string.split("&"):
                a, b, c = q.partition("=")
                if b == "=":
                    query.setdefault(a, []).append(c)
                else:
                    query[a] = Value.EMPTY
        return query

    @cached_property
    def method(self) -> str:
        return self.environ["REQUEST_METHOD"].lower()

    @cached_property
    def headers(self) -> Mapping[str, str]:
        headers = defaultdict(list)
        for key, value in self.environ.items():
            if key.startswith("HTTP_"):
                name = key[5:].replace("_", "-").title()
                headers[name].append(value)
            elif key in ["CONTENT_TYPE", "CONTENT_LENGTH"]:
                name = key.replace("_", "-").title()
                headers[name].append(value)
        return {name: ",".join(values) for name, values in headers.items()}

    @cached_property
    def cookies(self) -> Mapping[str, str]:
        if header := self.environ.get("HTTP_COOKIE"):
            buffer = (value.strip().partition("=") for value in header.split("; "))
            return {k: v for k, _, v in buffer}
        return {}

    def read(self):
        # see https://gist.github.com/mitsuhiko/5721547 for wsgi.input_terminated
        stream = self.environ["wsgi.input"]
        if self.environ.get("wsgi.input_terminated") == True:
            data = stream.read()
            stream.read(0)
        elif length := self.environ.get("CONTENT_LENGTH"):
            data = stream.read(int(length))
            stream.read(0)
        else:
            return None  # TODO: Cannot be processed for now ?!?

        if stream.seekable():
            stream.seek(0)
        else:
            stream = SpooledTemporaryFile(5 * 1_024)
            stream.write(data)
            self.environ["wsgi.input"] = stream
            self.environ["wsgi.input_terminated"] = True
        return data
