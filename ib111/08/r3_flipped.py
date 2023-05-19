from typing import List


# Implementujte predikát ‹is_almost_sorted›, který je pravdivý,
# je-li v seznamu ‹items› potřeba prohodit právě jednu dvojici
# čísel, aby se stal vzestupně seřazeným.

def is_almost_sorted(items: List[int]) -> bool:
    pass


def main() -> None:
    assert is_almost_sorted([1, 0, 0, 0])
    assert is_almost_sorted([1, 0, 0, 2])
    assert is_almost_sorted([0, 1, 0, 0, 2])
    assert is_almost_sorted([0, 2, 0, 0, 2, 0])
    assert is_almost_sorted([1, 2, 4, 3, 5])
    assert is_almost_sorted([1, 5, 3, 4, 2])
    assert is_almost_sorted([5, 2, 3, 4, 1])
    assert not is_almost_sorted([5, 1, 3, 4, 2])
    assert not is_almost_sorted([5, 4, 3, 2, 1])
    assert not is_almost_sorted([1, 2, 5, 3, 4])


if __name__ == "__main__":
    main()
