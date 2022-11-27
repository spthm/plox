from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union

from plox.tokens import Token

from .expressions import Expr


@dataclass(frozen=True)
class Block:
    statements: list[Stmt]


@dataclass(frozen=True)
class Expression:
    expression: Expr


@dataclass(frozen=True)
class Function:
    name: Token
    parameters: list[Var]
    body: Block


@dataclass(frozen=True)
class If:
    condition: Expr
    then_branch: Stmt
    else_branch: Optional[Stmt]


@dataclass(frozen=True)
class Print:
    expression: Expr


@dataclass(frozen=True)
class Return:
    keyword: Token
    expression: Expr


@dataclass(frozen=True)
class Var:
    name: Token
    initializer: Expr


@dataclass(frozen=True)
class While:
    condition: Expr
    body: Stmt


Stmt = Union[Block, Expression, Function, If, Print, Return, Var, While]
