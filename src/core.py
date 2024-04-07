from src.constants import L_VECTOR, PI, C
from src.key import Key, RoundKey
from src.types import Tuple16Int


class Grasshopper:
    _pi: tuple[int, ...] = PI
    _c: tuple[Tuple16Int, ...] = C
    _l_vector: Tuple16Int = L_VECTOR

    def __init__(self, key: Key):
        self._round_keys = self._expand_key(key)

    def encrypt(self, block: Tuple16Int) -> Tuple16Int:
        cypher_text = block[:]
        for i in range(9):
            cypher_text = self._xor_vectors(cypher_text, self._round_keys[i].vector)
            cypher_text = self._substitute_based_on_pi(cypher_text)
            cypher_text = self._l_transformation(cypher_text)
        cypher_text = self._xor_vectors(cypher_text, self._round_keys[9].vector)
        return cypher_text

    def _expand_key(self, key: Key) -> tuple[RoundKey, ...]:
        mut_round_keys: list[RoundKey] = []
        round_keys_pair = key.halves
        mut_round_keys.extend(round_keys_pair)

        for round_keys_pair_number in range(4):
            for feistel_round in range(8):
                constant = self._c[8 * round_keys_pair_number + feistel_round]
                round_keys_pair = self.f_transformation(constant, round_keys_pair)
            mut_round_keys.extend(round_keys_pair)
        return tuple(mut_round_keys)

    def f_transformation(
        self, constant: Tuple16Int, round_key_pair: tuple[RoundKey, RoundKey]
    ) -> tuple[RoundKey, RoundKey]:
        old_round_key_first, old_round_key_second = round_key_pair
        xor_result = self._xor_vectors(constant, old_round_key_first.vector)
        pi_substitute_result = self._substitute_based_on_pi(xor_result)
        l_transformation_result = self._l_transformation(pi_substitute_result)
        new_round_key_vector = self._xor_vectors(
            l_transformation_result,
            old_round_key_second.vector,
        )
        return RoundKey(new_round_key_vector), old_round_key_first

    def _xor_vectors(
        self,
        vector_1: Tuple16Int,
        vector_2: Tuple16Int,
    ) -> tuple[int, ...]:
        assert len(vector_1) == len(vector_2) == 16
        return tuple(
            v1_item ^ v2_item
            for v1_item, v2_item
            in zip(vector_1, vector_2)
        )  # fmt: skip

    def _substitute_based_on_pi(self, vector: Tuple16Int) -> Tuple16Int:
        assert len(vector) == 16
        return tuple(self._pi[item] for item in vector)

    def _l_transformation(self, vector: Tuple16Int) -> Tuple16Int:
        assert len(vector) == 16
        for _ in range(len(vector)):
            vector = self._r_transformation(vector)
        return vector

    def _r_transformation(self, vector: Tuple16Int) -> Tuple16Int:
        assert len(vector) == 16
        return self._l_func(vector), *vector[:-1]

    def _l_func(self, vector: Tuple16Int) -> int:
        assert len(vector) == 16
        product = tuple(
            self._mult_field(vector[i], self._l_vector[i]) for i in range(len(vector))
        )
        return self._sum_field(product)

    def _mult_field(self, left: int, right: int) -> int:
        product = 0
        while left:
            if left & 1:
                product ^= right
            if right & 0x80:
                right = (right << 1) ^ 0x1C3
            else:
                right <<= 1
            left >>= 1
        return product

    def _sum_field(self, vector: Tuple16Int) -> int:
        assert len(vector) == 16
        _sum = 0
        for number in vector:
            _sum ^= number
        return _sum
