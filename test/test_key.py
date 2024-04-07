import pytest

from src.key import Key, RoundKey


def test_round_key_init() -> None:
    # Act
    result = RoundKey(tuple(range(16)))

    # Assert
    assert result.vector == tuple(range(16))


@pytest.mark.parametrize("length", (1, 17))
def test_round_key_init__invalid_key_length(length: int) -> None:
    # Act/Assert
    with pytest.raises(ValueError):
        RoundKey(tuple(range(length)))


def test_key_init() -> None:
    # Act
    result = Key(tuple(range(32)))

    # Assert
    assert result.vector == tuple(range(32))


@pytest.mark.parametrize("length", (1, 33))
def test_key_init__invalid_key_length(length: int) -> None:
    # Act/Assert
    with pytest.raises(ValueError):
        Key(tuple(range(length)))


def test_key_halves() -> None:
    # Arrange
    key = Key(tuple(range(32)))

    # Act
    result = key.halves

    # Assert
    assert result == (
        RoundKey(tuple(range(0, 16))),
        RoundKey(tuple(range(16, 32))),
    )
