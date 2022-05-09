import pytest

from plox.ast import Bindings, Variable
from plox.environment import Environment
from plox.errors import ExecutionError
from plox.tokens import Token, TokenType


@pytest.fixture(name="outer_foo")
def outer_foo_():
    return Variable(Token(TokenType.IDENTIFIER, "foo", None, 1, 1))


@pytest.fixture(name="inner_foo")
def inner_foo_():
    # The environment and resolver rely on *different* expressions/tokens
    # having *different* hash() values (cf. how inner_foo and outer_foo
    # are both keys to the Bindings dict below). Since we use dataclasses,
    # we therefore require that inner_foo cannot be value-equal to outer_foo.
    return Variable(Token(TokenType.IDENTIFIER, "foo", None, 1, 2))


def test_get_defined(outer_foo):
    env = Environment()
    env.resolve(Bindings.from_dict({outer_foo: 0}))
    env.define(outer_foo.name, "foo")

    assert env[outer_foo] == "foo"


def test_set_defined(outer_foo):
    env = Environment()
    env.resolve(Bindings.from_dict({outer_foo: 0}))
    env.define(outer_foo.name, "foo")

    env[outer_foo] = "foobar"
    assert env[outer_foo] == "foobar"


def test_get_undefined_raises(outer_foo):
    env = Environment()
    env.resolve(Bindings.from_dict({outer_foo: 0}))

    with pytest.raises(ExecutionError, match="Undefined variable 'foo'"):
        _ = env[outer_foo]


def test_set_undefined_raises(outer_foo):
    env = Environment()
    env.resolve(Bindings.from_dict({outer_foo: 0}))

    with pytest.raises(ExecutionError, match="Undefined variable 'foo'"):
        env[outer_foo] = "foo"


def test_get_with_enclosing(outer_foo, inner_foo):
    enclosing = Environment()
    # 'foo' is defined in the outer environment ('enclosing') but
    # accessed from the inner environment ('env').
    enclosing.resolve(Bindings.from_dict({outer_foo: 0, inner_foo: 1}))
    enclosing.define(outer_foo.name, "foo")

    env = Environment(enclosing=enclosing)

    assert env[inner_foo] == "foo"


def test_set_with_enclosing(outer_foo, inner_foo):
    enclosing = Environment()
    # 'foo' is defined in the outer environment ('enclosing') but
    # modified from the inner environment ('env').
    enclosing.resolve(Bindings.from_dict({outer_foo: 0, inner_foo: 1}))
    enclosing.define(outer_foo.name, "foo")

    env = Environment(enclosing=enclosing)
    env[inner_foo] = "foobar"

    assert enclosing[outer_foo] == "foobar"
    assert env[inner_foo] == "foobar"


def test_define_with_enclosing(outer_foo, inner_foo):
    enclosing = Environment()
    # A variable named 'foo' is defined in the top-most environment ('enclosing'),
    # and a different variable, also named 'foo', is defined in the inner
    # environment ('env').
    enclosing.resolve(Bindings.from_dict({outer_foo: 0, inner_foo: 0}))
    enclosing.define(outer_foo.name, "foo")

    env = Environment(enclosing=enclosing)
    env.define(inner_foo.name, "foobar")

    assert enclosing[outer_foo] == "foo"
    assert env[inner_foo] == "foobar"
