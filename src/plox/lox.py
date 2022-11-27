import sys
from itertools import count
from pathlib import Path
from typing import Optional

from plox.errors import ExecutionError, ParserError, ScannerError
from plox.interpreter import Interpreter
from plox.parser import Parser
from plox.scanner import Scanner


class Lox:
    def __init__(self) -> None:
        self._interpreter = Interpreter()

    def run(self, source: str, start_lno: Optional[int] = None) -> None:
        tokens = Scanner(source, start_lno).scan_tokens()
        statements = Parser(tokens).parse()
        self._interpreter.interpret(statements)

    def run_file(self, path: Path) -> None:
        source = path.read_text()
        try:
            self.run(source)
        except (ParserError, ScannerError):
            sys.exit(65)
        except ExecutionError:
            sys.exit(70)

    def run_prompt(self) -> None:
        for lno in count(1):
            try:
                source_line = input("> ")
            except EOFError:
                break
            except KeyboardInterrupt:
                source_line = ""

            if not source_line:
                continue

            try:
                self.run(source_line, lno)
            except (ExecutionError, ParserError, ScannerError):
                pass
