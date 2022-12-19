# plox

A Python implementation of the Lox language

## Developer Quickstart

[`poetry`][poetry] is a dependency.

Install this package and its dependencies,

```
poetry install
poetry run pre-commit install
```

Run the `plox` CLI,

```
poetry run plox
```

Before pushing or opening a PR run the full set of linters and tests,

```
make lint
make test
```

To update dependencies,

```
make update
```

## Differences from Reference Lox

### Global Variables are Locals

In Lox, global variables are treated specially, and can be re-declared.
This, for example, is valid in `jlox`,

```lox
> var foo = "bar";
> var foo = "baz";
> print foo;
baz
> print clock();
1.669477696643E9
> var clock = "foobar";
> print clock();
Can only call functions and classes.
[line 1]
```

In `plox`, globals (both builtins like `clock()` and variables defined at the top level of a script) are locals of the root environment, and cannot be re-declared,

```lox
> var foo = "bar";
> var foo = "baz";
[line 2] Error: Already a variable with this name in this scope.
> print foo;
bar
> print clock();
1669478009.697674
> var clock = "foobar";
[line 5] Error: Already a variable with this name in this scope.
> print clock();
1669478014.63373
```

There are good non-technical reasons for the Lox behaviour; for example, it is convenient in a REPL to be able to re-define variables.
The difference here was mainly for simplicity of implementation: minimal special casing of globals by the environment and resolve.

### Prompt Line Numbering

Error messages from the prompt report the prompt line from which the error originates.
In `jlox`,

```lox
> print "this is line 1";
line 1
> fun sub(a, b) { return a - b; }
> print sub("1", 2);
Operands must be numbers.
[line 1]
```

In `plox`,

```lox
> print "this is line 1";
this is line 1
> fun sub(a, b) { return a - b; }
> print sub("1", 2);
[line 2] Error: Unsupported operands for '-', must both be 'number'.
```

While being (arguably) a usability improvement, this was introduced to work around issues in treating globals as root-scope locals: `plox` makes an internal assertion that resolved variables are never overwritten.
This check relies on the uniqueness of parsed tokens.
For identical tokens appearing on separate lines, uniqueness is guaranteed by tracking the line number in prompt mode, as it would be otherwise.

[poetry]: https://python-poetry.org/
