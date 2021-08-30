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

Before pushing, or opening a PR, run the full set of linters and tests,

```
poetry run tox
```

To update dependencies,

```
make update
```

[poetry]: https://python-poetry.org/
