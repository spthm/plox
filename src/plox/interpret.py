from plox.errors import ExecutionError, _report
from plox.expressions import Expr
from plox.evaluate import evaluate


def interpret(expr: Expr) -> None:
    try:
        value = evaluate(expr)
        print(_stringify(value))
    except ExecutionError as e:
        _report(e.token.lno, "", e.message)
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
