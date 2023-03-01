from functools import singledispatch
from typing import Any, overload

from plox.environment import Environment

from .evaluation import _truthy, evaluate
from .statements import Block, Expression, Function, If, Print, Return, Stmt, Var, While


def _stringify(value: object) -> str:
    if value is None:
        return "nil"
    if value is True:
        return "true"
    if value is False:
        return "false"

    text = str(value)

    if isinstance(value, float) and text.endswith(".0"):
        text = text[:-2]

    return text


class ReturnException(RuntimeError):
    def __init__(self, value: object):
        super().__init__()
        self.value = value


class LoxFunction:
    def __init__(self, declaration: Function, env: Environment) -> None:
        self._declaration = declaration
        self._closure = env

    def arity(self) -> int:
        return len(self._declaration.parameters)

    def call(self, arguments: list[object]) -> object:
        env = Environment(self._closure)
        for parameter, argument in zip(self._declaration.parameters, arguments):
            env.define(parameter, argument)

        try:
            execute(self._declaration.body, env)
        except ReturnException as ret:
            return ret.value

        return None

    def __str__(self) -> str:
        return f"<fn {self._declaration.name.lexeme}>"


# mypy's @overload is buggy for @singledispatch. Use of the separate _execute here
# is a workaround https://github.com/python/mypy/issues/8356.


@singledispatch
def _execute(stmt: Any, _: Environment) -> None:
    raise TypeError(f"execute does not support {type(stmt)}")


@overload
@_execute.register(Block)
def execute(stmt: Block, env: Environment) -> None:
    env = Environment(enclosing=env)
    for s in stmt.statements:
        execute(s, env)


@overload
@_execute.register(Expression)
def execute(stmt: Expression, env: Environment) -> None:
    evaluate(stmt.expression, env)


@overload
@_execute.register(Function)
def execute(stmt: Function, env: Environment) -> None:
    function = LoxFunction(stmt, env)
    env.define(stmt.name, function)


@overload
@_execute.register(If)
def execute(stmt: If, env: Environment) -> None:
    if _truthy(evaluate(stmt.condition, env)):
        execute(stmt.then_branch, env)
    elif stmt.else_branch is not None:
        execute(stmt.else_branch, env)


@overload
@_execute.register(Print)
def execute(stmt: Print, env: Environment) -> None:
    value = evaluate(stmt.expression, env)
    print(_stringify(value))


@overload
@_execute.register(Return)
def execute(stmt: Return, env: Environment) -> None:
    value = evaluate(stmt.expression, env)
    raise ReturnException(value)


@overload
@_execute.register(Var)
def execute(stmt: Var, env: Environment) -> None:
    value = evaluate(stmt.initializer, env)
    env.define(stmt.name, value)


@overload
@_execute.register(While)
def execute(stmt: While, env: Environment) -> None:
    while _truthy(evaluate(stmt.condition, env)):
        execute(stmt.body, env)


def execute(stmt: Stmt, env: Environment) -> None:
    return _execute(stmt, env)
