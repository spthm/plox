import sys
from pathlib import Path

from plox.scanner import Scanner


def _report(lno: int, where: str, msg: str) -> None:
    print(f"[line {lno}] Error{where}: {msg}", file=sys.stderr)


class Lox:
    def run(self, source: str) -> None:
        tokens = Scanner(source).scan_tokens()
        for t in tokens:
            print(t)

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

            try:
                self.run(source_line)
            except Exception as e:
                _report(-1, "", str(e))
