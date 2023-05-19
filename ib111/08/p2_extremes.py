from typing import List, Tuple

# Napište čistou funkci ‹local_extremes›, která dostane na vstupu
# seznam ‹values› čísel a vrátí dvojici seznamů ‹min_indices,
# max_indices›. Každý prvek seznamu ‹values› je unikátní. Seznam
# ‹min_indices› (‹max_indices›) bude obsahovat indexy lokálních
# minim (maxim) seznamu ‹values›. Oba tyto seznamy budou vzestupně
# seřazené.

Minima = List[int]
Maxima = List[int]


def local_extremes(values: List[int]) -> Tuple[Minima, Maxima]:
    maximums = []
    minimums = []
    if len(values) == 1:
        return ([0], [0])

    for i in range(len(values)):
        if i in range(1, len(values) - 1):
            if values[i-1] < values[i] > values[i+1]:
                maximums.append(i)

            elif values[i-1] > values[i] < values[i+1]:
                minimums.append(i)

        else:
            if i == len(values) - 1:
                if values[i - 1] < values[i]:
                    maximums.append(i)
                if values[i - 1] > values[i]:
                    minimums.append(i)

            elif i == 0:
                if values[i] < values[i+1]:
                    minimums.append(i)
                if values[i] > values[i+1]:
                    maximums.append(i)

    return (minimums, maximums)


def main() -> None:
    assert local_extremes([1, 4, 2, 0]) == ([0, 3], [1])
    assert local_extremes([3, 1, 5, 4, 0, 2]) == ([1, 4], [0, 2, 5])
    assert local_extremes([]) == ([], [])
    assert local_extremes([2]) == ([0], [0])
    assert local_extremes([1, 2]) == ([0], [1])


if __name__ == "__main__":
    main()
