import pytest

from plox.environment import Environment
from plox.errors import ExecutionError
from plox.tokens import Token, TokenType


@pytest.fixture(name="foo")
def foo_():
    return Token(TokenType.IDENTIFIER, "foo", None, 1)


def test_get_defined(foo):
    env = Environment()
    env.define(foo, "foo")

    assert env[foo] == "foo"


def test_set_defined(foo):
    env = Environment()
    env.define(foo, "foo")

    env[foo] = "foobar"
    assert env[foo] == "foobar"


def test_get_undefined_raises(foo):
    env = Environment()

    with pytest.raises(ExecutionError, match="Undefined variable 'foo'"):
        _ = env[foo]


def test_set_undefined_raises(foo):
    env = Environment()

    with pytest.raises(ExecutionError, match="Undefined variable 'foo'"):
        env[foo] = "foo"


def test_get_with_enclosing(foo):
    enclosing = Environment()
    enclosing.define(foo, "foo")

    env = Environment(enclosing=enclosing)

    assert enclosing[foo] == "foo"
    assert env[foo] == "foo"


def test_set_with_enclosing(foo):
    enclosing = Environment()
    enclosing.define(foo, "foo")

    env = Environment(enclosing=enclosing)
    env[foo] = "foobar"

    assert enclosing[foo] == "foobar"
    assert env[foo] == "foobar"


def test_define_with_enclosing(foo):
    enclosing = Environment()
    enclosing.define(foo, "foo")

    env = Environment(enclosing=enclosing)
    env.define(foo, "foobar")

    assert enclosing[foo] == "foo"
    assert env[foo] == "foobar"
