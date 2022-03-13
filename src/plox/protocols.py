from typing import Protocol, runtime_checkable


@runtime_checkable
class SupportsCall(Protocol):
    def arity(self) -> int:
        ...

    def call(self, arguments: list[object]) -> object:
        ...
