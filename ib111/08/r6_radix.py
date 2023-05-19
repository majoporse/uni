from typing import List, Tuple
from itertools import permutations, combinations_with_replacement


# † Posledním řadicím algoritmem, který v této kapitole prozkoumáme,
# je řazení po číslicích: obvyklé jméno pro tento algoritmus je
# „radix sort“, případně „bucket sort“. Algoritmy, které jsme viděli
# dosud, pracují všechny (krom ‹distribution_sort›) na principu
# srovnávání dvojic prvků. Tento princip je velmi obecný, ale často
# také omezující.
#
# V této úloze se vrátíme k myšlence funkce ‹distribution_sort› a
# místo porovnávání prvků je budeme počítat, zvolíme si ale jiné
# kritérium. Naším cílem bude seřadit seznam čísel, a využijeme
# k tomu skutečnosti, že čísla lze rozložit na jednotlivé cifry
# (v nějaké poziční soustavě). Pro jednoduchost si zvolme soustavu
# desítkovou (algoritmus ve skutečnosti ale na konkrétní volbě
# soustavy nezávisí).
#
# Základním stavebním kamenem bude procedura ‹sort_by_digit›, která:
#
#  1. přeuspořádá vstupní seznam tak, aby byl uspořádaný podle
#     ⟦i⟧-té číslice,
#  2. a to tak, aby přitom nezměnila relativní pořadí prvků, které
#     mají na ⟦i⟧-té pozici stejnou číslici.
#
# Protože číslic je málo, ale hodnot v seznamu potenciálně hodně,
# hodí se na toto přeuspořádání právě funkce ‹distribution_sort›:
#
#  1. spočítáme, kolik vstupních čísel padne do kterého „kyblíčku“
#     (rozsahu prvků se stejnou ⟦i⟧-tou cifrou),
#  2. pro každý kyblíček spočítáme, na jakých indexech se bude ve
#     výsledném seznamu nacházet,
#  3. vstupní seznam v jednom průchodu do takto nachystaných
#     kyblíčků rozřadíme (kyblíčky zaplňujeme ve stejném pořadí,
#     v jakém iterujeme vstupní seznam).
#
# Vyzbrojeni procedurou ‹sort_by_digit› už lehce seznam seřadíme:
# začneme od poslední cifry, a postupujeme doleva. Lehce se
# o správnosti tohoto postupu přesvědčíme indukcí:
#
#  1. po první iteraci je seznam seřazen podle první (nejpravější)
#     cifry,
#  2. předpokládejme, že po ⟦i⟧-té iteraci je seznam seřazen podle
#     cifer ⟦i, i - 1, …, 0⟧; v iteraci ⟦i + 1⟧ bude procedurou
#     ‹sort_by_digit› seřazen podle cifry ⟦i + 1⟧, ale ta nezměnila
#     pořadí prvků, které jsou na pozici ⟦i + 1⟧ stejné: proto je
#     po iteraci ⟦i + 1⟧ seznam seřazen podle cifer ⟦i + 1, i, i -
#     1, …, 0⟧.
#
# Následující seznam je již seřazen podle nejnižší cifry. Ukažme si
# na něm zbytek algoritmu:
#
#  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
#  │ 121 │ 111 │ 311 │ 332 │ 132 │ 133 │ 313 │ 223 │ 333 │
#  └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘
#
#  Spočítáme počty cifer na prostřední pozici a dostaneme: 3× 1, 2×
#  2, 4× 3. Nachystáme si příslušné kyblíčky a vyplňujeme je
#  (například) zleva doprava:
#
#  ┌─────┬─────┬─────┐ ┌─────┬─────┐ ┌─────┬─────┬─────┬─────┐
#  │     │     │     │ │ 121 │     │ │     │     │     │     │
#  └─────┴─────┴─────┘ └─────┴─────┘ └─────┴─────┴─────┴─────┘
#  ┌─────┬─────┬─────┐ ┌─────┬─────┐ ┌─────┬─────┬─────┬─────┐
#  │ 111 │     │     │ │ 121 │     │ │     │     │     │     │
#  └─────┴─────┴─────┘ └─────┴─────┘ └─────┴─────┴─────┴─────┘
#  ┌─────┬─────┬─────┐ ┌─────┬─────┐ ┌─────┬─────┬─────┬─────┐
#  │ 111 │ 311 │     │ │ 121 │     │ │ 332 │ 132 │     │     │
#  └─────┴─────┴─────┘ └─────┴─────┘ └─────┴─────┴─────┴─────┘
#  ┌─────┬─────┬─────┐ ┌─────┬─────┐ ┌─────┬─────┬─────┬─────┐
#  │ 111 │ 311 │ 313 │ │ 121 │ 223 │ │ 332 │ 132 │ 133 │ 333 │
#  └─────┴─────┴─────┘ └─────┴─────┘ └─────┴─────┴─────┴─────┘
#
# Postup opakujeme na nejlevější pozici: 4× 1, 1× 2, 4× 3
#
#  ┌─────┬─────┬─────┬─────┐ ┌─────┐ ┌─────┬─────┬─────┬─────┐
#  │ 111 │     │     │     │ │     │ │     │     │     │     │
#  └─────┴─────┴─────┴─────┘ └─────┘ └─────┴─────┴─────┴─────┘
#  ┌─────┬─────┬─────┬─────┐ ┌─────┐ ┌─────┬─────┬─────┬─────┐
#  │ 111 │     │     │     │ │     │ │ 311 │     │     │     │
#  └─────┴─────┴─────┴─────┘ └─────┘ └─────┴─────┴─────┴─────┘
#  ┌─────┬─────┬─────┬─────┐ ┌─────┐ ┌─────┬─────┬─────┬─────┐
#  │ 111 │ 121 │     │     │ │ 223 │ │ 311 │ 313 │     │     │
#  └─────┴─────┴─────┴─────┘ └─────┘ └─────┴─────┴─────┴─────┘
#  ┌─────┬─────┬─────┬─────┐ ┌─────┐ ┌─────┬─────┬─────┬─────┐
#  │ 111 │ 121 │ 132 │ 133 │ │ 223 │ │ 311 │ 313 │ 332 │ 333 │
#  └─────┴─────┴─────┴─────┘ └─────┘ └─────┴─────┴─────┴─────┘

def radixsort(to_sort: List[int]) -> List[int]:
    pass


def main() -> None:
    radixsort_test([])
    radixsort_test([1])
    radixsort_test([1, 2, 3, 4])
    radixsort_test([2310, 3300, 1320, 1001])
    radixsort_test([2, 100, 25, 0, 14])
    radixsort_test([12, 4, 3, 1, 25, 100, 14, 32, 100,
                    0, 0, 4, 2, 3, 1, 1, 125, 135])
    radixsort_test([654565365, 65655868865, 1223545, 21555555, 10])

    for low, high, count in test_parameters():
        values = range(low, high)
        lists = combinations_with_replacement(values, count)
        for combination in lists:
            for permutation in permutations(combination):
                records = list(permutation)
                expected = list(combination)
                assert radixsort(records) == expected


def test_parameters() -> List[Tuple[int, int, int]]:
    result = []
    for high in range(10):
        for low in range(high):
            for count in range(1, 5):
                result.append((low, high, count))
    return result


def radixsort_test(test_list: List[int]) -> bool:
    return radixsort(test_list) == sorted(test_list)


if __name__ == "__main__":
    main()
