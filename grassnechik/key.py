import binascii
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Self

from grassnechik.types import Tuple16Int, Tuple32Int


@dataclass(frozen=True, slots=True)
class RoundKey:
    vector: Tuple16Int

    def __post_init__(self) -> None:
        if len(self.vector) != 16:
            raise ValueError(
                f"round key len must be 16 bytes, but given {len(self.vector)}"
            )

    @classmethod
    def from_hex(cls, hex_view: str) -> Self:
        vector = binascii.unhexlify(hex_view)
        return cls(tuple(vector))


@dataclass(frozen=True, slots=True)
class Key:
    vector: Tuple32Int

    def __post_init__(self) -> None:
        if len(self.vector) != 32:
            raise ValueError(f"key len must be 32 bytes, but given {len(self.vector)}")

    @classmethod
    def from_iterable(cls, vector: Iterable[int]) -> Self:
        return cls(tuple(vector))

    @classmethod
    def from_hex(cls, hex_view: str) -> Self:
        vector = binascii.unhexlify(hex_view)
        return cls(tuple(vector))

    @property
    def halves(self) -> tuple[RoundKey, RoundKey]:
        return RoundKey(self.vector[:16]), RoundKey(self.vector[16:])
