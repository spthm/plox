from time import time


class Clock:
    def arity(self) -> int:
        return 0

    def call(self, _args: list[object]) -> float:
        return time()

    def __str__(self) -> str:
        return "<native fn>"
