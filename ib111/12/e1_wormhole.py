from typing import List, Set


# Do červí díry spadne seznam kladných celých čísel ‹nums› a množina
# cifer (celá čísla od 0 po 9) ‹allowed›. Na druhém konci vypadnou
# pouze ta čísla, jejichž všechny cifry jsou v množině ‹allowed›.

# Napište čistou funkci ‹wormhole›, která vrátí seznam všech čísel
# ze seznamu ‹nums›, která projdou červí dírou (pořadí zachovejte
# podle vstupního seznamu).

def wormhole(nums: List[int], allowed: Set[int]) -> List[int]:
    pass


def main() -> None:
    assert wormhole([12, 20], {0, 1, 2}) == [12, 20]
    assert wormhole([84, 28, 48, 82], {8, 2}) == [28, 82]
    assert wormhole([100, 1000, 10007, 101], {0, 1}) == [100, 1000, 101]


if __name__ == "__main__":
    main()
