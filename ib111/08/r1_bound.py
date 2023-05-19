from typing import List, Optional


# Implementujte funkci ‹left_bound›, která ve vzestupně seřazeném
# seznamu ‹values› co nejefektivněji najde index prvního výskytu
# hodnoty ‹target›. Pokud se hodnota v seznamu nenachází, vrátí
# ‹None›.

def left_bound(values: List[int], target: int) -> Optional[int]:
    if values[0] > target:
        return None

    if values[-1] < target:
        return None
    upper = len(values)
    lower = 0
    current = lower + (upper - lower) //2
    while not (values[current] == target and values[current] > values[current - 1]):

        if values[current] >= target:
            upper = current

        else:
            lower = current + 1

        if upper == lower:
            if values[current] == target:
                return current
            return None
        current = lower + (upper - lower) //2
    return current
        


def main() -> None:
    assert left_bound([1, 2, 3, 4, 5], 2) == 1
    assert left_bound([1, 2, 2, 2, 2], 2) == 1
    assert left_bound([2, 2, 2, 2, 2], 2) == 0
    assert left_bound([2, 2, 2, 2, 3], 2) == 0
    assert left_bound([1, 2, 3, 4, 5], 7) is None


if __name__ == "__main__":
    main()
