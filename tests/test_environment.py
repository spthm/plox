import pytest

from plox.ast import Assign, Bindings, Literal, Var, Variable
from plox.ast.resolve import Scope
from plox.environment import Environment
from plox.tokens import Token, TokenType


@pytest.fixture(name="outer_foo")
def outer_foo_():
    return Token(TokenType.IDENTIFIER, "foo", None, 1, 1)


@pytest.fixture(name="inner_foo")
def inner_foo_():
    # The environment and resolver rely on *different* expressions/tokens
    # having *different* hash() values (cf. how inner_foo and outer_foo
    # are both keys to the Bindings dict below). Since we use dataclasses,
    # we therefore require that inner_foo cannot be value-equal to outer_foo.
    return Token(TokenType.IDENTIFIER, "foo", None, 1, 2)


def test_get_defined(outer_foo):
    # var foo = "foo";
    env = Environment()
    var_foo = Var(outer_foo, Literal("foo"))
    env.define(var_foo, "foo")

    # Some access of foo.
    env.resolve(Bindings.from_dict({Variable(outer_foo): 0}))
    assert env[Variable(outer_foo)] == "foo"


def test_set_defined(outer_foo):
    # var foo = "foo";
    env = Environment()
    var_foo = Var(outer_foo, Literal("foo"))
    assign_foo = Assign(outer_foo, Literal("foobar"))
    env.define(var_foo, "foo")

    env.resolve(Bindings.from_dict({Variable(outer_foo): 0, assign_foo: 0}))

    # foo = "foobar";
    env[assign_foo] = "foobar"
    assert env[Variable(outer_foo)] == "foobar"


def test_get_with_enclosing(outer_foo, inner_foo):
    # 'foo' is defined in the outer environment ('enclosing') but
    # accessed from the inner environment ('env').
    enclosing = Environment()
    var_foo = Var(outer_foo, Literal("foo"))
    enclosing.define(var_foo, "foo")

    enclosing.resolve(Bindings.from_dict({Variable(inner_foo): 1}))

    env = Environment(enclosing=enclosing)

    # Some access of foo from an inner scope.
    assert env[Variable(inner_foo)] == "foo"


def test_set_with_enclosing(outer_foo, inner_foo):
    # 'foo' is defined in the outer environment ('enclosing') but
    # modified from the inner environment ('env').
    enclosing = Environment()
    var_foo = Var(outer_foo, Literal("foo"))
    assign_foo = Assign(inner_foo, Literal("foobar"))
    enclosing.define(var_foo, "foo")

    enclosing.resolve(
        Bindings.from_dict(
            {Variable(outer_foo): 0, Variable(inner_foo): 1, assign_foo: 1}
        )
    )

    env = Environment(enclosing=enclosing)
    env[assign_foo] = "foobar"

    # Access of foo from both inner and outer scopes see modified value.
    assert enclosing[Variable(outer_foo)] == "foobar"
    assert env[Variable(inner_foo)] == "foobar"


def test_define_with_enclosing(outer_foo, inner_foo):
    # A variable named 'foo' is defined in the top-most environment ('enclosing'),
    # and a different variable, also named 'foo', is defined in the inner
    # environment ('env').
    enclosing = Environment()
    var_outer_foo = Var(outer_foo, Literal("foo"))
    var_inner_foo = Var(inner_foo, Literal("foobar"))
    enclosing.define(var_outer_foo, "foo")

    env = Environment(enclosing=enclosing)
    env.define(var_inner_foo, "foobar")

    enclosing.resolve(
        Bindings.from_dict({Variable(outer_foo): 0, Variable(inner_foo): 0})
    )

    # Access of foo from both inner and outer scopes see modified value.
    assert enclosing[Variable(outer_foo)] == "foo"
    assert env[Variable(inner_foo)] == "foobar"


def test_root_local_scope():
    root = Environment.as_root({"foo": "foo", "bar": "bar"})
    assert root.local_scope() == Scope({"foo": True, "bar": True})


def test_inner_local_scope(inner_foo):
    root = Environment.as_root({"foo": "foo", "bar": "bar"})

    env = Environment(enclosing=root)
    env.resolve(Bindings.from_dict({inner_foo: 0}))
    env.define(Var(inner_foo, Literal("foo")), "foo")

    assert root.local_scope() == Scope({"foo": True, "bar": True})
    assert env.local_scope() == Scope({"foo": True})
