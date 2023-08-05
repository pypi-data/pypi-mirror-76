from __future__ import annotations

import json
import logging
import re
from collections import defaultdict
from copy import copy
from datetime import date, datetime, time
from functools import singledispatch
from itertools import chain, cycle
from typing import Any, Callable, Dict, List, Literal, Mapping, NamedTuple, Set, Tuple, Union

from .common import Value

logger = logging.getLogger("ades")
applicators: Dict[str, List[Tuple[int, Callable]]] = defaultdict(list)
formats: Dict[str, Callable[[str], bool]] = {}

Errors = Union[List, Tuple, str]
Validation = Tuple[Any, Errors]


def register_format(name):
    def wrapper(func):
        formats[name] = func
        return func

    return wrapper


def apply_to(*types, order: int = None):
    types = types or ("string", "number", "null", "boolean", "object", "array")

    def wrapper(func):
        for type in types:
            applicators[type].append((order, func))
        return func

    return wrapper


@register_format("date")
def check_date(value):
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


@register_format("date-time")
def check_datetime(value: str):
    try:
        if value.endswith("Z"):
            value = value[:-1]
        datetime.fromisoformat(value)
        return True
    except ValueError:
        return False


@register_format("time")
def check_time(value: str):
    try:
        if value.endswith("Z"):
            value = value[:-1]
        time.fromisoformat(value)
        return True
    except ValueError:
        return False


@register_format("duration")
def check_duration(value: str):
    if re.fullmatch("P((\d+)([SMHDWMY]))+", value, re.I):
        # FIXME: very weak, need to be rewritten
        return True
    return False


Schema = Union[Literal[True], Literal[False], Mapping]


def validate(document: Schema, value) -> Validation:
    if document is True:
        return ok(value)
    if document is False:
        return fail(value, "Value forbidden")

    if not isinstance(value, Value):
        value = copy(value)
    value, errors = dispatch(document, value)
    value, errors = maybe(value, errors)
    return value, clean(errors)


def dispatch(document, value):
    value_type = get_type(value)
    errors = []
    if value_type != "undefined" and (types := document.get("type")):
        if value_type not in types:
            if value_type == "number" and "integer" in types and int(value) == value:
                pass  # OK
            else:
                errors.append("Wrong type")
    for _, applicator in applicators[value_type]:
        value, errs = applicator(document, value)
        errors.extend(errs)
    return maybe(value, errors)


def get_type(value) -> str:
    if value in (Value.MISSING, Value.EMPTY):
        return "undefined"
    if isinstance(value, str):
        return "string"
    if isinstance(value, bool):
        return "boolean"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    raise TypeError


@apply_to("string")
def validate_max_length(document, value) -> Validation:
    if "maxLength" in document:
        other = document["maxLength"]
        if len(value) > other:
            return fail(value, f"Greater than {other}")
    return ok(value)


@apply_to("string")
def validate_min_length(document, value) -> Validation:
    if "minLength" in document:
        other = document["minLength"]
        if len(value) < other:
            return fail(value, f"Lower than {other}")
    return ok(value)


@apply_to("string")
def validate_pattern(document, value) -> Validation:
    if "pattern" in document:
        other = document["pattern"]
        if not re.match(other, value):
            return fail(value, f"Does not match {other}")
    return ok(value)


@apply_to("string")
def validate_format(document, value) -> Validation:
    if "format" in document:
        other = document["format"]
        if checker := formats.get(other):
            if not checker(value):
                return fail(value, "Bad format")
        else:
            logger.info("format %s not implemented", other)
    return ok(value)


@apply_to("number")
def validate_multiple_of(document, value) -> Validation:
    if "multipleOf" in document:
        other = document["multipleOf"]
        if value % other != 0:
            return fail(value, f"Value is not a multiple of {other}")
    return ok(value)


@apply_to("number")
def validate_maximum(document, value) -> Validation:
    if "maximum" in document:
        other = document["maximum"]
        if value > other:
            return fail(value, f"Value is greater than {other}")
    return ok(value)


@apply_to("number")
def validate_exclusive_maximum(document, value) -> Validation:
    if "exclusiveMaximum" in document:
        other = document["exclusiveMaximum"]
        if value >= other:
            return fail(value, f"Value must be lower than {other}")
    return ok(value)


@apply_to("number")
def validate_minimum(document, value) -> Validation:
    if "minimum" in document:
        other = document["minimum"]
        if value < other:
            return fail(value, f"Value is lesser than {other}")
    return ok(value)


@apply_to("number")
def validate_exclusive_minimum(document, value) -> Validation:
    if "exclusiveMinimum" in document:
        other = document["exclusiveMinimum"]
        if value <= other:
            return fail(value, f"Value is lesser than {other}")
    return ok(value)


@apply_to("boolean")
def validate_boolean(document, value) -> Validation:
    return ok(value)


@apply_to("null")
def validate_null(document, value) -> Validation:
    return ok(value)


@apply_to("undefined")
def validate_default(document: Mapping, value) -> Validation:
    if "default" in document:
        value = document["default"]
    return ok(value)


@apply_to("object")
def validate_properties(document: Mapping, value: Mapping) -> Validation:
    value = dict(value)
    annotation: Set[str] = set()
    errors = []
    for key, subdoc in document.get("properties", {}).items():
        annotation.add(key)
        subval = value.get(key, Value.MISSING)
        subval, errs = validate(subdoc, subval)
        errors.append((key, errs))
        if subval is not Value.MISSING:
            value[key] = subval
            annotation.add(key)

    for pattern, subdoc in document.get("patternProperties", {}).items():
        for key, subval in value.items():
            if re.match(pattern, key):
                annotation.add(key)
                value[key], errs = validate(subdoc, subval)
                errors.append((key, errs))
    if "additionalProperties" in document:
        subdoc = document.get("additionalProperties")
        for key, subval in value.items():
            if key not in annotation:
                annotation.add(key)
                value[key], errs = validate(subdoc, subval)
                errors.append((key, errs))
    value = {k: v for k, v in value.items() if v != Value.MISSING}
    return maybe(value, errors)


@apply_to("object", order=1000)
def validate_unevaluated_properties(document, value) -> Validation:
    if "unevaluatedProperties" in document:
        raise NotImplementedError
    return ok(value)


@apply_to("object")
def validate_property_names(document, value) -> Validation:
    errors = []
    if "propertyNames" in document:
        subdoc = document.get("propertyNames")
        for key in value:
            _, errs = validate(subdoc, key)
            if errs:
                errors.append((key, ["Unallowed property name"]))
    return maybe(value, errors)


@apply_to()
def validate_enum(document, value) -> Validation:
    if "enum" in document:
        value_type = get_type(value)
        if not any(value == other and value_type == get_type(other) for other in document["enum"]):
            return fail(value, "Value not allowed")
    return ok(value)


@apply_to()
def validate_const(document, value) -> Validation:
    errors = []
    if "const" in document:
        other = document["const"]
        if value != other or get_type(value) != get_type(other):
            return fail(value, "Value not allowed")
    return ok(value)


@apply_to()
def validate_not(document, value) -> Validation:
    if "not" in document:
        not_document = document.get("not")
        _, errors = validate(not_document, value)
        if not errors:
            return fail(value, "Must not validate")
    return ok(value)


@apply_to()
def validate_any_of(document, value) -> Validation:
    if "anyOf" in document:
        errors = []
        for document in document.get("anyOf"):
            version, errs = validate(document, value)
            if not errs:
                return ok(version)
            errors.extend(errs)
        return fail(value, errors + ["None validated"])
    return ok(value)


@apply_to()
def validate_one_of(document, value) -> Validation:
    if "oneOf" in document:
        versions = []
        errors = []
        for document in document.get("oneOf"):
            version, errs = validate(document, value)
            if not errs:
                versions.append(version)
            errors.extend(errs)
        if not versions:
            return fail(value, errors + ["None validated"])
        elif len(versions) > 1:
            return fail(value, errors + ["Too many validated"])
        return ok(versions.pop())
    return ok(value)


@apply_to()
def validate_all_of(document, value) -> Validation:
    if "allOf" in document:
        versions = []
        errors = []
        for subdoc in document.get("allOf"):
            version, errs = validate(subdoc, value)
            versions.append(version)
            errors.extend(errs)
        if not errors:
            # TODO: ensure that all versions have the same value
            pass
        return maybe(versions.pop(), errors)
    return ok(value)


@apply_to()
def validate_ternary(document, value) -> Validation:
    if "if" in document:
        if_document = document.get("if")
        _, errs = validate(if_document, value)
        if not errs:
            then_document = document.get("then")
            value, errors = validate(then_document, value)
        else:
            else_document = document.get("else")
            value, errors = validate(else_document, value)
        return maybe(value, errors)
    return ok(value)


@apply_to("object")
def validate_dependent_schemas(document, value):
    if "dependentSchemas" in document:
        versions = [value]
        errors = []
        for key, document in document.get("dependentSchemas").items():
            if key in value:
                version, errs = validate(document, value)
                versions.append(version)
                errors.extend(errs)
        return versions.pop(), errors
    return ok(value)


@apply_to("object")
def validate_max_properties(document, value) -> Validation:
    if other := document.get("maxProperties"):
        if len(value) > other:
            return fail(value, f"Cannot have more than {other} properties")
    return ok(value)


@apply_to("object")
def validate_min_properties(document, value) -> Validation:
    if other := document.get("minProperties"):
        if len(value) < other:
            return fail(value, f"Cannot have less than {other} properties")
    return ok(value)


@apply_to("object", order=1100)
def validate_required(document, value) -> Validation:
    if "required" in document:
        errors = []
        for m in document.get("required"):
            if value.get(m, Value.MISSING) == Value.MISSING:
                errors.append((m, ["Mandatory"]))
        return maybe(value, errors)
    return ok(value)


@apply_to("object")
def validate_dependent_required(document, value) -> Validation:
    if requirements := document.get("dependentRequired"):
        for key, others in requirements.items():
            if key in value and (missing := set(others) - set(value)):
                errors = [(k, "Mandatory") for k in missing]
                return fail(value, errors)
    return ok(value)


@apply_to("array")
def validate_items(document, value):
    # items & additionalItems
    errors = []
    itms = []
    if "items" in document:
        itms = document.get("items")
        if not isinstance(itms, list):
            itms = cycle([itms])
    add_itm = document.get("additionalItems", True)
    itms = chain(itms, cycle([add_itm]))
    if itms:
        for i, (subdoc, subval) in enumerate(zip(itms, value)):
            value[i], errs = validate(subdoc, subval)
            errors.append((i, errs))
    return maybe(value, errors)


@apply_to("array", order=1000)
def validate_unevaluated_items(document, value):
    if "unevaluatedItems" in document:
        raise NotImplementedError
    return ok(value)


@apply_to("array")
def validate_contains(document, value):
    errors = []
    if "contains" in document:
        validates = 0
        subdoc = document.get("contains")
        for i, subval in enumerate(value):
            value[i], errs = validate(subdoc, subval)
            if not errs:
                validates += 1
            else:
                errors.extend((i, errs))
        if validates:
            errors.clear()
        else:
            errors.append("Does not contains")
        if other := document.get("maxContains"):
            if validates > other:
                errors.append(f"Cannot contains more than {other}")
        if other := document.get("minContains"):
            if validates < other:
                errors.append(f"Cannot contains less than {other}")
    return maybe(value, errors)


@apply_to("array")
def validate_max_items(document, value) -> Validation:
    if "maxItems" in document:
        other = document["maxItems"]
        if len(value) > other:
            return fail(value, f"No more than {other} items allowed")
    return ok(value)


@apply_to("array")
def validate_min_items(document, value) -> Validation:
    if "minItems" in document:
        other = document["minItems"]
        if len(value) < other:
            return fail(value, f"No less than {other} items allowed")
    return ok(value)


@apply_to("array")
def validate_unique_items(document, value) -> Validation:
    if document.get("uniqueItems"):
        items = {(get_type(item), json.dumps(item)) for item in value}
        if len(value) > len(items):
            return fail(value, "Unique items required")
    return ok(value)


@apply_to("string")
def validate_content(document, value) -> Validation:
    if mediatype := document.get("contentMediaType"):
        logger.info("Current implementation cannot validate %s contents for now", mediatype)
        if encoding := document.get("contentEncoding", "utf-8"):
            logger.info("Current implementation cannot decode %s for now", encoding)
        # if schema := document.get("contentSchema"):
        #     pass
    return ok(value)


def ok(value) -> Validation:
    return value, []


def fail(value, err) -> Validation:
    if not err:
        return value, []
    if isinstance(err, list):
        return value, err
    if isinstance(err, tuple) and err and not err[-1]:
        # Discard empty sets
        return value, []
    return value, [err]


def maybe(value, errors) -> Validation:
    if not errors:
        return value, []
    if isinstance(errors, str):
        return value, [errors]
    if isinstance(errors, tuple):
        if errors and not errors[-1]:
            # Discard empty sets
            return value, []
        return value, [errors]
    if isinstance(errors, list):
        errs = []
        for err in errors:
            if isinstance(err, tuple) and err and not err[-1]:
                continue
            errs.append(err)
        return value, errs
    raise TypeError


@singledispatch
def clean(errs):
    return errs


@clean.register
def _(errs: list):
    output = []
    for e in errs:
        e = clean(e)
        if e not in output:
            output.append(e)
    return sorted(output)
