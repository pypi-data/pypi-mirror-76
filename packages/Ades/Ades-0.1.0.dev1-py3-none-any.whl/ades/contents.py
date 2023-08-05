from dataclasses import dataclass, field
from functools import singledispatch
from typing import List, Mapping

from ades.common import Value


@dataclass
class Content:
    pass


@dataclass
class Primitive(Content):
    @classmethod
    def repeated(cls, *args, **kwargs):
        return Array(default=cls(*args, **kwargs))


@dataclass
class String(Primitive):
    pass


@dataclass
class Number(Primitive):
    pass


@dataclass
class Integer(Primitive):
    pass


@dataclass
class Boolean(Primitive):
    pass


@dataclass
class Null(Primitive):
    pass


@dataclass
class AnyContent(Content):
    pass


@dataclass
class Array(Content):
    by_indexes: List[Content] = field(default_factory=list)
    default: Content = field(default_factory=AnyContent)

    def __getitem__(self, index):
        try:
            return self.by_indexes[index]
        except IndexError:
            return self.default


@dataclass
class Object(Content):
    by_keys: Mapping[str, Content] = field(default_factory=dict)
    default: Content = field(default_factory=AnyContent)

    def __getitem__(self, key):
        try:
            return self.by_keys[key]
        except KeyError:
            return self.default


@singledispatch
def factory(schema) -> Content:
    raise TypeError


@factory.register
def _(schema: Content):
    return schema


@factory.register
def _(schema: bool):
    return AnyContent()


@factory.register
def _(schema: list) -> List[Content]:
    return [factory(c) for c in schema]


@factory.register
def _(schema: dict) -> Content:
    if schema["type"] == "string":
        return String()
    if schema["type"] == "number":
        return Number()
    if schema["type"] == "integer":
        return Integer()
    if schema["type"] == "boolean":
        return Boolean()

    if schema["type"] == "null":
        return Null()

    if schema["type"] == "array":
        items = factory(schema.get("items", True))
        if isinstance(items, Content):
            fallback, items = items, []
        else:
            fallback = factory(schema.get("additionalItems", False))
        return Array(by_indexes=items, default=fallback)
    if schema["type"] == "object":
        properties = {k: factory(v) for k, v in schema.get("properties", {}).items()}
        fallback = factory(schema.get("additionalProperties", False))
        return Object(by_keys=properties, default=fallback)


def cast(content: Content, value):
    if isinstance(value, Value):
        return value, []

    return cast_content(content, value)


@singledispatch
def cast_content(content, value):
    raise NotImplementedError


@cast_content.register
def _(content: String, value):
    return str(value), []


@cast_content.register
def _(content: Number, value):
    try:
        return float(value), []
    except ValueError:
        return Value.DISCARDED, ["Could not cast to number"]


@cast_content.register
def _(content: Integer, value):
    try:
        return int(value), []
    except ValueError:
        return Value.DISCARDED, ["Could not cast to integer"]


@cast_content.register
def _(content: Boolean, value):
    if value in ["true", "on"]:
        return True, []
    if value in ["false", "off"]:
        return False, []
    return Value.DISCARDED, ["Could not cast to boolean"]


@cast_content.register
def _(content: Null, value):
    if value in ["null"]:
        return None, []
    return Value.DISCARDED, ["Could not cast to null"]


@cast_content.register
def _(content: Array, value):
    errors = []
    if isinstance(value, list):
        value = list(value)
    else:
        value = Value.DISCARDED
        errors = ["Could not cast to array"]
    if not errors:
        for i, element in enumerate(value):
            value[i], errs = cast(content[i], element)
            if errs:
                errors.append((i, errs))
    return value, errors


@cast_content.register
def _(content: Object, value):
    errors = []
    try:
        value = dict(value)
    except ValueError:
        value = Value.DISCARDED
        errors = ["Could not cast to object"]
    if not errors:
        for key, member in value.items():
            value[key], errs = cast(content[key], member)
            if errs:
                errors.append((key, errs))
    return value, errors
