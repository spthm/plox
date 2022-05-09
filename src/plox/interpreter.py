from plox.ast import Stmt, execute, resolve_statements
from plox.builtins import Clock
from plox.environment import Environment
from plox.errors import ExecutionError, report


class Interpreter:
    def __init__(self) -> None:
        self._env = Environment.from_globals({"clock": Clock()})

    def interpret(self, statements: list[Stmt]) -> None:
        bindings = resolve_statements(statements)
        self._env.resolve(bindings)
        for statement in statements:
            try:
                execute(statement, self._env)
            except ExecutionError as e:
                report(e.token.lno, "", e.message)
                raise
