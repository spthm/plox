from plox.errors import ExecutionError, report
from plox.evaluate import evaluate
from plox.expressions import Expr


class Interpreter:
    def interpret(self, expr: Expr) -> None:
        try:
            value = evaluate(expr)
            print(_stringify(value))
        except ExecutionError as e:
            report(e.token.lno, "", e.message)
            raise


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
