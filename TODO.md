# TODO

## Reference `Lox`

### `Scanner`

- Keep scanning after we `raise SyntaxError`, and report all errors at the end.
See `Scanner._scan_token` and `Scanner._string`.
Provide an error handler to `Scanner.__init__`, define a free function to print errors, or define a `TokenType.ERROR` for invalid tokens.
- Re-implement `_scan_token` so it functions more like a `switch` `case`, e.g. via a lookup; a chain of `if` `elif` is (probably) slower.
- Implement `Scanner.scan_tokens` as a free function.
Instances of `Scanner` are never re-used - all invocations will be `Scanner(source).scan_tokens()`, which consumes the input `source` - so it should not be a `class`.

### `Parser`

- Implement `Parser.parse` as a free function.

### `ast_str`

- `ast_str` should be the `__str__` method of an `AST` class.

## Non-reference `Lox`

### `Lox`

- Distinguish between `int` and `float` numeric types.

### `Scanner`

- Support `1.` and `.1` syntax for literal numbers.
- Support scientific notation for literal numbers.
