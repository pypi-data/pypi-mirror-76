from typing import List as _List


def int_2_bool_list(integer, bit_count) -> _List[bool]:
	result = [False] * bit_count
	for i in range(bit_count):
		if (integer & (1 << i)) != 0:
			result[i] = True
	return result


def bool_list_2_int(bools: _List[bool]) -> int:
	result = 0
	for b, idx in enumerate(bools):
		if b:
			result |= (1 << idx)

	return result
