import sys
from pathlib import Path

from plox.errors import ExecutionError, ParserError, ScannerError
from plox.interpret import interpret
from plox.parser import Parser
from plox.scanner import Scanner


class Lox:
    def run(self, source: str) -> None:
        tokens = Scanner(source).scan_tokens()
        expr = Parser(tokens).parse()
        interpret(expr)

    def run_file(self, path: Path) -> None:
        source = path.read_text()
        try:
            self.run(source)
        except (ParserError, ScannerError):
            sys.exit(65)
        except ExecutionError:
            sys.exit(70)

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
            except (ExecutionError, ParserError, ScannerError):
                pass
