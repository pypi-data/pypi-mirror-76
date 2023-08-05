from __future__ import annotations

import json
from dataclasses import dataclass
from functools import cached_property, singledispatch, singledispatchmethod
from logging import getLogger
from typing import Any, List, Mapping, Protocol, Sequence, Tuple

from .common import MultiValuesDict, Schema, Value
from .contents import Array, Content, Object, Primitive, cast
from .contents import factory as content_factory
from .utils import grouper

logger = getLogger("ades.serializers")


def get_serializer(
    content_type: str = None,
    *,
    name: str,
    schema: Schema,
    location: str = None,
    style: str = None,
    explode: bool = None,
) -> Serializer:
    if content_type == "application/json":
        return JSONSerializer(name=name)

    if content_type == "application/xml":
        return XMLSerializer(name=name)

    if style == "simple":
        return SimpleSerializer(name=name, explode=explode, schema=schema)

    if style == "label":
        return LabelSerializer(name=name, explode=explode, schema=schema)

    if style == "matrix":
        return MatrixSerializer(name=name, explode=explode, schema=schema)

    if style == "form":
        return FormSerializer(name=name, explode=explode, schema=schema)

    if style == "spaceDelimited":
        return SpaceDelimitedSerializer(name=name, explode=explode, schema=schema)

    if style == "pipeDelimited":
        return PipeDelimitedSerializer(name=name, explode=explode, schema=schema)

    if style == "deepObject":
        return DeepObjectSerializer(name=name, explode=explode, schema=schema)


def load_json(payload):
    if isinstance(payload, Value):
        return payload, []
    try:
        return json.loads(payload), []
    except json.decoder.JSONDecodeError as error:
        logger.info(error)
        return Value.DISCARDED, ["Malformed json content"]


def load_xml(payload):
    if isinstance(payload, Value):
        return payload, []
    raise NotImplementedError


def load_csv(payload, sep):
    if isinstance(payload, Value):
        return payload, []
    if sep in payload:
        return payload.split(sep), []
    return [payload], []


@dataclass
class Serializer:
    name: str

    def deserialize(self, payload: MultiValuesDict[str, bytes]) -> Tuple[Any, MultiValuesDict, List[str]]:
        raise NotImplementedError


@dataclass
class JSONSerializer(Serializer):
    def deserialize(self, payload: MultiValuesDict[str, bytes]):
        value, payload, errors = pop(payload, self.name)
        if not errors:
            value, errors = load_json(value)
        return value, payload, errors


@dataclass
class XMLSerializer(Serializer):
    def deserialize(self, payload: Mapping[str, List[bytes]]):
        value, payload, errors = pop(payload, self.name)
        if not errors:
            value, errors = load_xml(value)
        return value, payload, errors


@dataclass
class SimpleSerializer(Serializer):
    explode: bool
    schema: Schema

    @cached_property
    def content(self) -> Content:
        return content_factory(self.schema)

    def deserialize(self, payload):
        value, payload, errors = self.deserialize_content(self.content, payload)
        if not errors:
            value, errors = cast(self.content, value)
        return value, payload, errors

    @singledispatchmethod
    def deserialize_content(self, field, payload):
        raise NotImplementedError

    @deserialize_content.register
    def _(self, field: Primitive, payload):
        value, payload, errors = pop(payload, self.name)
        return value, payload, errors

    @deserialize_content.register
    def _(self, field: Array, payload):
        value, payload, errors = pop(payload, self.name)
        if not errors:
            value, errors = load_csv(value, sep=",")
        return value, payload, errors

    @deserialize_content.register
    def _(self, field: Object, payload):
        value, payload, errors = pop(payload, self.name)
        if not errors:
            value, errors = load_csv(value, sep=",")
        if not errors:
            if self.explode:
                value = unpair_dict(value)
            else:
                value = regroup_dict(value)
        return value, payload, errors


@dataclass
class LabelSerializer(Serializer):
    explode: bool
    schema: Schema

    @cached_property
    def content(self) -> Content:
        return content_factory(self.schema)

    def deserialize(self, payload):
        value, payload, errors = self.deserialize_content(self.content, payload)
        if not errors:
            value, errors = cast(self.content, value)
        return value, payload, errors

    @singledispatchmethod
    def deserialize_content(self, field, payload):
        raise NotImplementedError

    @deserialize_content.register
    def _(self, field: Primitive, payload):
        value, payload, errors = pop(payload, self.name)
        if not errors:
            if isinstance(value, str):
                if value.startswith("."):
                    value = value[1:]
                else:
                    value = Value.DISCARDED
                    errors = ["Not a label"]
        return value, payload, errors

    @deserialize_content.register
    def _(self, field: Array, payload):
        value, payload, errors = pop(payload, self.name)
        if not errors:
            if isinstance(value, str):
                if value.startswith("."):
                    value = value[1:]
                else:
                    value = Value.DISCARDED
                    errors = ["Not a label"]
        if not errors:
            if self.explode:
                value, errors = load_csv(value, sep=".")
            else:
                value, errors = load_csv(value, sep=",")
        return value, payload, errors

    @deserialize_content.register
    def _(self, field: Object, payload):
        value, payload, errors = pop(payload, self.name)
        if not errors:
            if isinstance(value, str):
                if value.startswith("."):
                    value = value[1:]
                else:
                    value = Value.DISCARDED
                    errors = ["Not a label"]
        if not errors:
            if self.explode:
                value, errors = load_csv(value, sep=".")
                if not errors:
                    value = unpair_dict(value)
            else:
                value, errors = load_csv(value, sep=",")
                if not errors:
                    value = regroup_dict(value)
        return value, payload, errors


@dataclass
class MatrixSerializer(Serializer):
    explode: bool
    schema: Schema

    @cached_property
    def prefix(self):
        return f";{self.name}="

    @cached_property
    def prefix_len(self):
        return len(self.prefix)

    @cached_property
    def content(self) -> Content:
        return content_factory(self.schema)

    def deserialize(self, payload):
        value, payload, errors = self.deserialize_content(self.content, payload)
        if not errors:
            value, errors = cast(self.content, value)
        return value, payload, errors

    @singledispatchmethod
    def deserialize_content(self, field, payload):
        raise NotImplementedError

    @deserialize_content.register
    def _(self, field: Primitive, payload):
        value, payload, errors = pop(payload, self.name)
        if not errors:
            if isinstance(value, str):
                if value.startswith(self.prefix):
                    value = value[self.prefix_len :]
                else:
                    value = Value.DISCARDED
                    errors = ["Not a matrix value"]
        return value, payload, errors

    @deserialize_content.register
    def _(self, field: Array, payload):
        value, payload, errors = pop(payload, self.name)
        if not errors:
            if isinstance(value, str):
                if value.startswith(self.prefix):
                    value = value[self.prefix_len :]
                else:
                    value = Value.DISCARDED
                    errors = ["Not a matrix value"]
        if not errors:
            if self.explode:
                value, errors = load_csv(value, sep=self.prefix)
            else:
                value, errors = load_csv(value, sep=",")
        return value, payload, errors

    @deserialize_content.register
    def _(self, field: Object, payload):
        value, payload, errors = pop(payload, self.name)
        if not errors:
            if isinstance(value, str):
                if not value.startswith(";"):
                    value = Value.DISCARDED
                    errors = ["Not a matrix value"]
        if not errors:
            if self.explode:
                value = value[1:]
                value, errors = load_csv(value, sep=";")
                if not errors:
                    value = unpair_dict(value)
            else:
                value = value[self.prefix_len :]
                value, errors = load_csv(value, sep=",")
                if not errors:
                    value = regroup_dict(value)
        return value, payload, errors


@dataclass
class FormSerializer(Serializer):
    explode: bool
    schema: Schema

    @cached_property
    def content(self) -> Content:
        return content_factory(self.schema)

    def deserialize(self, payload):
        value, payload, errors = self.deserialize_content(self.content, payload)
        if not errors:
            value, errors = cast(self.content, value)
        return value, payload, errors

    @singledispatchmethod
    def deserialize_content(self, field, payload):
        raise NotImplementedError

    @deserialize_content.register
    def _(self, field: Primitive, payload):
        value, payload, errors = pop(payload, self.name, multi=False)
        return value, payload, errors

    @deserialize_content.register
    def _(self, field: Array, payload):
        value, payload, errors = pop(payload, self.name, multi=self.explode)
        if not errors:
            if not self.explode:
                value, errors = load_csv(value, sep=",")
        return value, payload, errors

    @deserialize_content.register
    def _(self, field: Object, payload):
        value = {}
        errors = []
        if self.explode:
            for key in field.by_keys:
                value[key], payload, errs = pop(payload, key)
                errors.extend(errs)
        else:
            value, payload, errors = pop(payload, self.name)
            if not errors:
                value, errors = load_csv(value, sep=",")
            if not errors:
                value = regroup_dict(value)
        return value, payload, errors


@dataclass
class SpaceDelimitedSerializer(Serializer):
    explode: bool
    schema: Schema

    @cached_property
    def content(self) -> Content:
        return content_factory(self.schema)

    def deserialize(self, payload):
        value, payload, errors = self.deserialize_content(self.content, payload)
        if not errors:
            value, errors = cast(self.content, value)
        return value, payload, errors

    @singledispatchmethod
    def deserialize_content(self, field, payload):
        raise NotImplementedError

    @deserialize_content.register
    def _(self, field: Array, payload):
        value, payload, errors = pop(payload, self.name, multi=self.explode)
        if not errors:
            if not self.explode:
                value, errors = load_csv(value, sep=" ")
        return value, payload, errors


@dataclass
class PipeDelimitedSerializer(Serializer):
    explode: bool
    schema: Schema

    @cached_property
    def content(self) -> Content:
        return content_factory(self.schema)

    def deserialize(self, payload):
        value, payload, errors = self.deserialize_content(self.content, payload)
        if not errors:
            value, errors = cast(self.content, value)
        return value, payload, errors

    @singledispatchmethod
    def deserialize_content(self, field, payload):
        raise NotImplementedError

    @deserialize_content.register
    def _(self, field: Array, payload):
        value, payload, errors = pop(payload, self.name, multi=self.explode)
        if not errors:
            if not self.explode:
                value, errors = load_csv(value, sep="|")
        return value, payload, errors


@dataclass
class DeepObjectSerializer(Serializer):
    explode: bool
    schema: Schema

    @cached_property
    def content(self) -> Content:
        content = content_factory(self.schema)
        content.id = self.name
        return content

    def deserialize(self, payload):
        value, payload, errors = self.deserialize_content(self.content, payload)
        if not errors:
            value, errors = cast(self.content, value)
        return value, payload, errors

    @singledispatchmethod
    def deserialize_content(self, field, payload):
        raise NotImplementedError

    @deserialize_content.register
    def _(self, field: Object, payload):
        value = {}
        errors = []
        for key in field.by_keys:
            value[key], payload, errs = pop(payload, f"{self.name}[{key}]")
            errors.extend(errs)
        prefix = f"{self.name}["
        prefix_len = len(prefix)
        for key in payload:
            if key.startswith(prefix) and key.endswith("]"):
                value[key[prefix_len:-1]], payload, errs = pop(payload, key)
        return value, payload, errors


def unpair_dict(values, sep="=", default=Value.EMPTY):
    result = {}
    for a, b, c in (d.partition(sep) for d in values):
        result[a] = c if b == "=" else default
    return result


def regroup_dict(values, default=Value.EMPTY):
    if isinstance(values, Value):
        return values
    return dict(grouper(values, 2, default))


@singledispatch
def pop(payload: Mapping, key, *, multi=False):
    payload = payload.copy()
    value = payload.pop(key, Value.MISSING)
    if multi and not isinstance(value, Value):
        value = [value]
    return value, payload, []


@pop.register
def _(payload: MultiValuesDict, key, *, multi=False):
    value = payload.poplist(key, Value.MISSING)
    errors = []
    if value == []:
        value = Value.MISSING
    elif multi is False and isinstance(value, list):
        if len(value) == 1:
            value = value[0]
        else:
            value = Value.DISCARDED
            errors = ["Too many values"]
    return value, payload, errors
