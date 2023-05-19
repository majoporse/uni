from typing import Set, Optional


# Napište čistou funkci, která najde libovolnou podmnožinu zadané množiny
# kladných celých čísel ‹nums›, součet jejíchž prvků je přesně
# ‹total›. Pokud taková podmnožina neexistuje, funkce vrátí ‹None›.


def subset_sum(nums: Set[int], total: int) -> Optional[Set[int]]:
    pass


def main() -> None:
    assert subset_sum(set(), 5) is None
    assert subset_sum({1, 2, 3}, 7) is None
    assert subset_sum({1}, 1) == {1}
    assert subset_sum({1, 2, 3}, 5) == {2, 3}
    assert subset_sum({5, 10, 12, 13}, 27) == {5, 10, 12}


if __name__ == '__main__':
    main()
