from typing import Optional


# Napište čistou funkci ‹nearest_disjoint›, která pro vstup ⟦n⟧ nalezne
# číslo ⟦m⟧ takové, že:
#
#  • množiny cifer použitých v ⟦m⟧ a ⟦n⟧ jsou disjunktní,
#  • ⟦|m - n|⟧ je nejmenší možné.

def nearest_disjoint(n: int) -> Optional[int]:
    pass


def main() -> None:
    assert nearest_disjoint(0) == 1
    assert nearest_disjoint(1) == 0 or nearest_disjoint(1) == 2
    assert nearest_disjoint(9) == 10 or nearest_disjoint(9) == 8
    assert nearest_disjoint(10) == 9
    assert nearest_disjoint(22) == 19
    assert nearest_disjoint(1234) == 999
    assert nearest_disjoint(1259) == 888
    assert nearest_disjoint(9988) == 10000
    assert nearest_disjoint(500) == 499
    assert nearest_disjoint(87451) == 90000
    assert nearest_disjoint(5555) == 6000
    assert nearest_disjoint(123456789) == 0
    assert nearest_disjoint(1023456789) is None


if __name__ == '__main__':
    main()
