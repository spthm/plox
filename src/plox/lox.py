import sys
from pathlib import Path

from plox.ast_printer import ast_str
from plox.errors import _report
from plox.parser import Parser
from plox.scanner import Scanner


class Lox:
    def run(self, source: str) -> None:
        tokens = Scanner(source).scan_tokens()
        expr = Parser(tokens).parse()
        if expr is None:
            return

        print(ast_str(expr))

    def run_file(self, path: Path) -> None:
        source = path.read_text()
        try:
            self.run(source)
        except Exception as e:
            _report(-1, "", str(e))
            sys.exit(65)

    def run_prompt(self) -> None:
        while True:
            try:
                source_line = input("> ")
            except EOFError:
                break
            except KeyboardInterrupt:
                source_line = ""

            if not source_line:
                continue

            try:
                self.run(source_line)
            except Exception as e:
                _report(-1, "", str(e))
