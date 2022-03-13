from time import time

# pylint: disable=no-self-use


class Clock:
    def arity(self) -> int:
        return 0

    def call(self, _args: list[object]) -> float:
        return time()

    def __str__(self) -> str:
        return "<native fn>"
