import sys
from pathlib import Path

from plox.scanner import scan_tokens


class Interpreter:
    def run(self, source: str):
        tokens = scan_tokens(source)
        for t in tokens:
            print(t)

    def run_file(self, path: Path):
        source = path.read_text()
        try:
            self.run(source)
        except Exception as e:
            self._report(-1, "", str(e))
            sys.exit(65)

    def run_prompt(self):
        while True:
            try:
                source_line = input("> ")
            except EOFError:
                break

            try:
                self.run(source_line)
            except Exception as e:
                self._report(-1, "", str(e))

    def _report(self, lno: int, where: str, msg: str):
        print(f"[line {lno}] Error{where}: {msg}", file=sys.stderr)
