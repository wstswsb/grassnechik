import binascii
import os

import pytest

from grassnechik.grassnechik import Grassnechik
from grassnechik.key import Key, RoundKey


def test_key_expand() -> None:
    # Arrange
    key_hex = "8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef"
    key = Key.from_hex(key_hex)

    # Act
    cypher = Grassnechik(key)

    # Assert
    assert cypher._round_keys == (
        RoundKey.from_hex("8899aabbccddeeff0011223344556677"),
        RoundKey.from_hex("fedcba98765432100123456789abcdef"),
        RoundKey.from_hex("db31485315694343228d6aef8cc78c44"),
        RoundKey.from_hex("3d4553d8e9cfec6815ebadc40a9ffd04"),
        RoundKey.from_hex("57646468c44a5e28d3e59246f429f1ac"),
        RoundKey.from_hex("bd079435165c6432b532e82834da581b"),
        RoundKey.from_hex("51e640757e8745de705727265a0098b1"),
        RoundKey.from_hex("5a7925017b9fdd3ed72a91a22286f984"),
        RoundKey.from_hex("bb44e25378c73123a5f32f73cdb6e517"),
        RoundKey.from_hex("72e9dd7416bcf45b755dbaa88e4a4043"),
    )


def test_encrypt() -> None:
    # Arrange
    message = tuple(binascii.unhexlify("1122334455667700ffeeddccbbaa9988"))
    key_hex = "8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef"
    key = Key.from_hex(key_hex)
    sut = Grassnechik(key)

    # Act
    result = sut.encrypt(message)

    # Assert
    assert result == tuple(binascii.unhexlify("7f679d90bebc24305a468d42b9d4edcd"))


def test_decrypt() -> None:
    # Arrange
    cypher = tuple(binascii.unhexlify("7f679d90bebc24305a468d42b9d4edcd"))
    key_hex = "8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef"
    key = Key.from_hex(key_hex)
    sut = Grassnechik(key)

    # Act
    result = sut.decrypt(cypher)

    # Assert
    assert result == tuple(binascii.unhexlify("1122334455667700ffeeddccbbaa9988"))


@pytest.mark.parametrize(
    "input_vector_hex, expected_result_hex",
    [
        ("ffeeddccbbaa99881122334455667700", "b66cd8887d38e8d77765aeea0c9a7efc"),
        ("b66cd8887d38e8d77765aeea0c9a7efc", "559d8dd7bd06cbfe7e7b262523280d39"),
        ("559d8dd7bd06cbfe7e7b262523280d39", "0c3322fed531e4630d80ef5c5a81c50b"),
        ("0c3322fed531e4630d80ef5c5a81c50b", "23ae65633f842d29c5df529c13f5acda"),
    ],
)
def test_substitute_based_on_pi(
    input_vector_hex: str,
    expected_result_hex: str,
) -> None:
    # Arrange
    sut = Grassnechik(Key.from_iterable(os.urandom(32)))
    input_vector = binascii.unhexlify(input_vector_hex)
    expected_result_vector = tuple(binascii.unhexlify(expected_result_hex))

    # Act
    result = sut._substitute_based_on_pi(input_vector)

    # Assert
    assert result == expected_result_vector


@pytest.mark.parametrize(
    "input_vector_hex, expected_result_hex",
    [
        ("00000000000000000000000000000100", "94000000000000000000000000000001"),
        ("94000000000000000000000000000001", "a5940000000000000000000000000000"),
        ("a5940000000000000000000000000000", "64a59400000000000000000000000000"),
        ("64a59400000000000000000000000000", "0d64a594000000000000000000000000"),
    ],
)
def test_r_transformation(
    input_vector_hex: str,
    expected_result_hex: str,
) -> None:
    # Arrange
    sut = Grassnechik(Key.from_iterable(os.urandom(32)))
    input_vector = binascii.unhexlify(input_vector_hex)
    expected_result_vector = tuple(binascii.unhexlify(expected_result_hex))

    # Act
    result = sut._r_transformation(input_vector)

    # Assert
    assert result == expected_result_vector


@pytest.mark.parametrize(
    "input_vector_hex, expected_result_hex",
    [
        ("64a59400000000000000000000000000", "d456584dd0e3e84cc3166e4b7fa2890d"),
        ("d456584dd0e3e84cc3166e4b7fa2890d", "79d26221b87b584cd42fbc4ffea5de9a"),
        ("79d26221b87b584cd42fbc4ffea5de9a", "0e93691a0cfc60408b7b68f66b513c13"),
        ("0e93691a0cfc60408b7b68f66b513c13", "e6a8094fee0aa204fd97bcb0b44b8580"),
    ],
)
def test_l_transformation(
    input_vector_hex: str,
    expected_result_hex: str,
) -> None:
    # Arrange
    sut = Grassnechik(Key.from_iterable(os.urandom(32)))
    input_vector = binascii.unhexlify(input_vector_hex)
    expected_result_vector = tuple(binascii.unhexlify(expected_result_hex))

    # Act
    result = sut._l_transformation(input_vector)

    # Assert
    assert result == expected_result_vector
