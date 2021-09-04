# TODO

## Reference `Lox`

### `Scanner`

- Keep scanning after we `raise ScannerError`, and report all errors at the end.
See `Scanner._scan_token` and `Scanner._string`.
Provide an error handler to `Scanner.__init__`, define a free function to print errors, or define a `TokenType.ERROR` for invalid tokens.
- Re-implement `_scan_token` so it functions more like a `switch` `case`, e.g. via a lookup; a chain of `if` `elif` is (probably) slower.
- Implement `Scanner.scan_tokens` as a free function.
Instances of `Scanner` are never re-used - all invocations will be `Scanner(source).scan_tokens()`, which consumes the input `source` - so it should not be a `class`.

### `Parser`

- Implement `Parser.parse` as a free function.
- Internally `raise ParserError` if the provided list of tokens does not end with a `TokenType.EOF` token.
Currently, this results in a hard crash with an `IndexError` from `parse()`.

### `ast_str`

- `ast_str` should be the `__str__` method of an `AST` class.

### `evaluate`

- We return `False` for equality comparison of `NaN`, but should return `True`.
- `(x / 0)` is a valid Lox expression (returning `Nan` or `+/-Inf`); we raise a `ZeroDivisionError`.

## Challenges

### 6: Parsing Expressions

2. Implement support for the ternary operator.
To [match C](https://en.cppreference.com/w/cpp/language/operator_precedence), the grammar (as of Chapter 6) is `conditional-expression → ( equality '?' expression ':' conditional-expression ) | equality ;`.
Note also that there are other [ternary operators](https://en.wikipedia.org/wiki/Ternary_operation).

3. Add error productions for binary operators without a left-hand operand.
The grammar (as of Chapter 6) becomes `unary → ( ( "!" | "-" | "+" | "*" | "/" | "==" | "!=" | "<" | "<=" | ">" | ">=" ) unary ) | primary ;` but, after parsing the full `Unary` expression, `Parser._unary` raises a `ParserError` if the `op` is not in `{ "!", "-" }`.

## Non-reference `Lox`

### `Lox`

- Distinguish between `int` and `float` numeric types; printing of floats should include a trailing `.0`.
- Require `++` for string concatenation (I think this is a neat idea).
- Do not return `True` for equality comparison of `NaN` values.

### `Scanner`

- Support `1.` and `.1` syntax for literal numbers.
- Support scientific notation for literal numbers.
