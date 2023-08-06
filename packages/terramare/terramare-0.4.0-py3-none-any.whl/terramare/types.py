"""Common types and re-exports."""

from typing import Any, Callable, Generic, Type, TypeVar, Union

import attr
from typing_extensions import Literal

TypedDictMetas = set()

# pylint: disable=unused-import
try:  # pragma: no cover
    from typing import _TypedDictMeta  # type: ignore[attr-defined]

    TypedDictMetas.add(_TypedDictMeta)

except ImportError:  # pragma: no cover
    pass

# pylint: disable=unused-import
try:  # pragma: no cover
    from typing_extensions import (  # type: ignore[attr-defined]  # noqa: F401
        _TypedDictMeta,
    )

    TypedDictMetas.add(_TypedDictMeta)
except ImportError:  # pragma: no cover
    pass

try:
    from typing_extensions import _Literal  # type: ignore[attr-defined]

    LiteralMeta = _Literal
except ImportError:  # pragma: no cover
    LiteralMeta = Literal

T = TypeVar("T")


NotNonePrimitive = Union[str, int, float, dict, list, bool]
Primitive = Union[NotNonePrimitive, None]

DeserializableType = Union[Type[Any], Callable[..., Any]]


class TerramareError(Exception):
    """Base class for exceptions raised by terramare."""


@attr.s(auto_attribs=True, frozen=True)
class Tag(Generic[T]):
    """Tag type to satisfy the type checker."""

    t: DeserializableType
