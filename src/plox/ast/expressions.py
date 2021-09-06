from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from plox.tokens import Token


@dataclass(frozen=True)
class Binary:
    left: Expr
    operator: Token
    right: Expr


@dataclass(frozen=True)
class Grouping:
    expression: Expr


@dataclass(frozen=True)
class Literal:
    value: object


@dataclass(frozen=True)
class Unary:
    operator: Token
    right: Expr


Expr = Union[Binary, Grouping, Literal, Unary]
