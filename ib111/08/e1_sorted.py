from typing import List


# Napište predikát ‹is_sorted›, který rozhodne, je-li vstupní seznam
# vzestupně seřazený.

def is_sorted(num_list: List[int]) -> bool:
    for i in range (len(num_list) - 1):
        if num_list[i] > num_list[i+1]:
            return False
    return True


def main() -> None:
    assert is_sorted([])
    assert is_sorted([-1])
    assert is_sorted([-1, 0, 1])
    assert is_sorted([0, 1, 1])
    assert is_sorted([-5, -1, -1, 0, 45, 2000])

    assert not is_sorted([1, -1])
    assert not is_sorted([0, -1])
    assert not is_sorted([1, 2, 3, 2, 4, 5])
    assert not is_sorted([5, 1, 2, 3, 4])
    assert not is_sorted([1, 2, 3, 4, 1])


if __name__ == "__main__":
    main()
