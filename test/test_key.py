import pytest

from src.key import Key


def test_init() -> None:
    # Act
    result = Key(tuple(range(32)))

    # Assert
    assert result.vector == tuple(range(32))


@pytest.mark.parametrize("length", (1, 33))
def test_init__invalid_key_length(length: int) -> None:
    # Act/Assert
    with pytest.raises(ValueError):
        Key(tuple(range(length)))


def test_halves() -> None:
    # Arrange
    key = Key(tuple(range(32)))

    # Act
    result = key.halves

    # Assert
    assert result == (
        tuple(range(0, 16)),
        tuple(range(16, 32)),
    )
