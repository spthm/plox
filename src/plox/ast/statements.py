from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from plox.tokens import Token

from .expressions import Expr


@dataclass(frozen=True)
class Expression:
    expression: Expr


@dataclass(frozen=True)
class Print:
    expression: Expr


@dataclass(frozen=True)
class Var:
    name: Token
    initializer: Expr


Stmt = Union[Expression, Print, Var]
