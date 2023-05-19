from typing import List


# Implementujte predikát ‹is_cyclically_sorted›, který je pravdivý,
# je-li seznam cyklicky seřazený. Seznam je cyklicky seřazený,
# existuje-li rotace, po které bude seřazený vzestupně.

def is_cyclically_sorted(records: List[int]) -> bool:
    first = 0
    for i in range(len(records)-1):
        if records[i] > records[i+1]:
            first = i+1
    for i in range(first, first + len(records) - 1):
        if records[i % len(records)] > records[(i+1) % len(records)]:
            return False
    return True


def main() -> None:
    assert is_cyclically_sorted([1, 2, 3, 4, 5])
    assert is_cyclically_sorted([5, 1, 2, 3, 4])
    assert is_cyclically_sorted([3, 4, 5, 1, 2])
    assert is_cyclically_sorted([3, 4, 5, 1, 2])
    assert is_cyclically_sorted([2, 3, 4, 5, 1])
    assert not is_cyclically_sorted([2, 3, 4, 5, 3])
    assert not is_cyclically_sorted([4, 2, 3, 1, 5])
    assert not is_cyclically_sorted([4, 3, 2, 1, 2])
    assert not is_cyclically_sorted([5, 4, 3, 2, 1])


if __name__ == "__main__":
    main()
