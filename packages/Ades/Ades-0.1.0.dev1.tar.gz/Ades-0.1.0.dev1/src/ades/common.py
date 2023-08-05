import enum
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cached_property
from typing import Generic, Iterator, List, Mapping, NoReturn, Protocol, Sequence, TypeVar, Union
from urllib.parse import unquote_plus
from abc import abstractmethod

T = TypeVar("T")
U = TypeVar("U")

Schema = Union[bool, Mapping]


class Location(enum.Enum):
    PATH = "path"
    QUERY = "query"
    HEADER = "header"
    COOKIE = "cookie"
    BODY = "body"


class Value(enum.Enum):
    MISSING = 0
    EMPTY = 1
    DISCARDED = 2


class Request(Protocol):
    content_type: str
    headers: Mapping[str, str]
    uri: str
    query_string: str
    method: str
    cookies: Mapping[str, str]

    @abstractmethod
    def read(self) -> bytes:
        """Returns body content
        """
        ...


@dataclass
class SimpleRequest:
    headers: Mapping[str, str]
    body: bytes = None
    uri: str = "/"
    query_string: str = ""
    method: str = "GET"
    cookies: Mapping[str, str] = field(default_factory=dict)

    @cached_property
    def content_type(self):
        if content_type := self.headers.get("Content-Type"):
            return content_type.partition(";")[0].strip()

    def read(self):
        return self.body or b""


class MultiValuesDict(Mapping, Generic[T, U]):
    def __init__(self, data: Mapping[T, List[U]]):
        self.data = dict(data)

    @classmethod
    def from_sequence(cls, seq):
        data = defaultdict(list)
        for field, value in seq:
            data[field].append(value)
        return cls(data)

    def pop(self, key, default=Value.MISSING) -> U:
        value = self.data.pop(key, default)
        value = single_value(value)
        return value

    def poplist(self, key, default=Value.MISSING) -> List[U]:
        value = self.data.pop(key, [])
        return value or default

    def append(self, key: T, value: U) -> NoReturn:
        self.data.setdefault(key, []).append(value)

    def extend(self, key: T, value: Sequence[U]) -> NoReturn:
        self.data.setdefault(key, []).extend(value)

    def __getitem__(self, key: T) -> U:
        value = self.data[key]
        value = single_value(value)
        return value

    def __iter__(self) -> Iterator[T]:
        return iter(self.data)

    def __len__(self) -> Iterator[T]:
        return len(self.data)

    def __repr__(self):
        return repr(self.data)

    def __eq__(self, other):
        if isinstance(other, MultiValuesDict):
            return self.data == other.data
        elif isinstance(other, dict):
            return self.data == other
        return NotImplemented

    def copy(self):
        return self.__class__(dict(self.data))


def single_value(payload: List[T]) -> T:
    if isinstance(payload, list):
        return payload[0] if payload else Value.MISSING
    return payload


def multivalues_factory(query: str) -> MultiValuesDict:
    variables = {}
    if query:
        for part in query.split("&"):
            a, b, c = part.partition("=")
            if b == "=":
                variables.setdefault(a, []).append(unquote_plus(c))
            else:
                variables[a] = Value.EMPTY
    return MultiValuesDict(variables)
