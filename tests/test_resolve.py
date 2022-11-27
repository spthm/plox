import pytest

from plox.ast.expressions import Assign, Literal, Variable
from plox.ast.resolve import Bindings, Scope, resolve_statements
from plox.ast.statements import Block, Expression, Var
from plox.errors import ExecutionError
from plox.tokens import Token, TokenType


@pytest.fixture(name="var_foo")
def var_foo_():
    return Var(Token(TokenType.IDENTIFIER, "foo", None, 1, 1), Literal(1))


@pytest.fixture(name="variable_foo")
def variable_foo_():
    return Variable(Token(TokenType.IDENTIFIER, "foo", None, 1, 1))


def test_resolve_var(var_foo, variable_foo):
    # Foo defined and accessed in the inner scope of a block.
    statement = Block([var_foo, variable_foo])
    bindings = resolve_statements([statement], Scope())
    assert bindings == Bindings.from_dict({variable_foo: 0})


def test_resolve_variable(variable_foo):
    # Foo accessed in the inner scope of a block.
    statement = Block([Expression(variable_foo)])
    # Fake foo having been defined in the outer scope.
    bindings = resolve_statements([statement], Scope({"foo": True}))
    assert bindings == Bindings.from_dict({variable_foo: 1})


def test_resolve_undefined_raises(variable_foo):
    with pytest.raises(ExecutionError, match="Undefined variable 'foo'"):
        _ = resolve_statements([Expression(variable_foo)])


def test_resolve_assignment_undefined_variable_raises():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/assignment/undefined.lox
    id_a = Token(TokenType.IDENTIFIER, "a", None, 1, 1)
    literal_a = Literal("a")
    # a = "a";
    expr = Assign(id_a, literal_a)

    with pytest.raises(ExecutionError, match="Undefined variable 'a'"):
        resolve_statements([Expression(expr)])
