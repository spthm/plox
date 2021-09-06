from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from .expressions import Expr


@dataclass(frozen=True)
class Expression:
    expression: Expr


@dataclass(frozen=True)
class Print:
    expression: Expr


Stmt = Union[Expression, Print]
