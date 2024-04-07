from collections.abc import Iterable
from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True, slots=True)
class Key:
    vector: tuple[int, ...]

    def __post_init__(self) -> None:
        if len(self.vector) != 32:
            raise ValueError(f"key len must be 32 bytes, but given {len(self.vector)}")

    @classmethod
    def from_iterable(cls, vector: Iterable[int]) -> Self:
        return cls(tuple(vector))

    @property
    def halves(self) -> tuple[tuple[int, ...], tuple[int, ...]]:
        return self.vector[:16], self.vector[16:]
