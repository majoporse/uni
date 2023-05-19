from typing import Set


# Napište čistou funkci ‹highly_composite›, která dostane na vstupu
# množinu přirozených čísel a vrátí množinu těch z nich, která jsou
# vysoce složená. Přirozené číslo je vysoce složené, má-li striktně
# víc dělitelů, než libovolné menší přirozené číslo.

def highly_composite(numbers: Set[int]) -> Set[int]:
    pass


def main() -> None:
    assert highly_composite({1, 3, 7, 12}) == {1, 12}
    assert highly_composite(set(range(1, 50))) == \
        {1, 2, 4, 6, 12, 24, 36, 48}

    big1 = {7**i * 10099**j for i in range(1, 6) for j in range(4)}
    big2 = big1 | {2 * x for x in big1} | {3 * x for x in big1}
    big3 = {7**i * 10099**j for i in range(1, 6) for j in range(8)}
    assert highly_composite(big1 | {12, 60}) == {12, 60}
    assert highly_composite(big2 | {360}) == {360}
    assert highly_composite(big3 | {360, 840}) == {360, 840}


if __name__ == '__main__':
    main()
