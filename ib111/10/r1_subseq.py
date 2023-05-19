from typing import List

# Na vstupu dostanete neprázdný seznam čísel. Vaším úkolem je vrátit
# množinu všech seznamů, které:
#
#  1. jsou vlastními podposloupnostmi vstupního seznamu, tzn.
#     vzniknou ze vstupního seznamu vynecháním alespoň jednoho
#     prvku,
#  2. jsou neklesající, tzn. pro seznam ‹out› a celá čísla ‹i›, ‹j›
#     platí ‹i < j› → ‹out[i] ≤ out[j]›.
#
# Protože datový typ ‹set› neumožňuje ukládat seznamy jako prvky,
# výstup uložte do seznamu (na pořadí jednotlivých posloupností v
# tomto seznamu nezáleží).


def subseq(seq: List[int]) -> List[List[int]]:
    pass


def main() -> None:
    subseq_test([1], [[]])
    subseq_test([1, 2], [[], [1], [2]])
    subseq_test([2, 1], [[], [1], [2]])
    subseq_test([2, 2, 2], [[], [2], [2, 2]])
    subseq_test([2, 1, 2], [[], [1], [2], [2, 2], [1, 2]])
    subseq_test([-1, 0, 1], [[], [-1], [0], [1],
                             [-1, 0], [-1, 1], [0, 1]])
    subseq_test([1, -12, 0, 55], [[], [1], [-12],
                                  [0], [55], [1, 55],
                                  [-12, 0], [-12, 0, 55],
                                  [-12, 55], [0, 55]])
    subseq_test([3, 2, 1], [[], [3], [2], [1]])


def subseq_test(input_seq: List[int],
                expected: List[List[int]]) -> None:
    original_seq = input_seq.copy()
    result = subseq(input_seq)

    assert input_seq == original_seq

    result.sort()
    expected.sort()
    assert result == expected, (result, expected)


if __name__ == '__main__':
    main()
