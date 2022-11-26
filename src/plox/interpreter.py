from plox.ast import Stmt, execute, resolve_statements
from plox.builtins import Clock
from plox.environment import Environment
from plox.errors import ExecutionError, report


class Interpreter:
    def __init__(self) -> None:
        self._env = Environment.as_root({"clock": Clock()})

    def interpret(self, statements: list[Stmt]) -> None:
        try:
            bindings = resolve_statements(statements, self._env.local_scope())
            self._env.resolve(bindings)
            for statement in statements:
                execute(statement, self._env)
        except ExecutionError as e:
            report(e.token.lno, "", e.message)
            raise
