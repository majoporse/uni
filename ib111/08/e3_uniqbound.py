from typing import List, Optional


# Napište čistou funkci, která najde v zadaném uspořádaném seznamu
# ‹numbers› největší číslo, které není větší než parametr ‹value›.
# Neexistuje-li takové, vraťte ‹None›.
#
# V ostatních případech je tedy výsledkem vždy číslo, které se
# nachází v ‹numbers› a vždy platí ‹lower_bound(numbers, x) ≤ x›.
#
# Předpokládejte, že v seznamu ‹numbers› se čísla neopakují.
# Použijte efektivní algoritmus.

def lower_bound(numbers: List[int], value: int) -> Optional[int]:
    if numbers == []:
        return None
    left = 0
    right = len(numbers) - 1
    current = left + (right - left)//2
    while not (numbers[current] <= value < numbers[current+1]):
        if right == 0:
            return None
        if numbers[current] < value:
            left = current + 1
            if left == len(numbers) -1:
                return numbers[left]
        else:
            right = current

        current = left + (right - left)//2
    return numbers[current]
    
    
    
    
def main() -> None:
    assert lower_bound([1, 2, 3], 2) == 2
    assert lower_bound([1, 3, 5], 2) == 1
    assert lower_bound([1, 2, 3, 4, 5, 6], 6) == 6
    assert lower_bound([], 2) is None
    assert lower_bound([1, 2, 3], -2) is None
    assert lower_bound([-5, -1, 8, 90], 2) == -1
    assert lower_bound([-5, -1, 0], 2) == 0
    assert lower_bound([1, 3], 2) == 1
    assert lower_bound([1, 3], 1) == 1
    assert lower_bound([-5, -1, 0, 2], 2) == 2
    assert lower_bound([-5, -1, 0, 1], 2) == 1


if __name__ == '__main__':
    main()
