from typing import List, Tuple
from itertools import permutations, combinations_with_replacement


# † Implementujte algoritmus řazení haldou. Základní myšlenka
# algoritmu je podobná algoritmu řazení výběrem:
#
#  • vstupní seznam rozdělíme na dvě pomyslné části, neseřazenou
#    (na začátku) a seřazenou (na konci);
#  • v každé iteraci najdeme největší prvek v neseřazené části,
#    přesuneme ho na její konec, a pomyslnou dělící čáru posuneme
#    o jeden prvek doleva.
#
# To, čím se algoritmus od řazení výběrem liší je metoda „hledání“
# onoho největšího prvku. Seznam totiž před samotným začátkem řazení
# přeuspořádáme do formy tzv. haldy, která má tyto vlastnosti:
#
#  • největší prvek je na nulté pozici,
#  • pro prvek na pozici ⟦i⟧ platí, že je větší než prvky na
#    pozicích ⟦2i + 1⟧ a ⟦2i + 2⟧ (existují-li).
#
# Je zřejmé, že nahrazením největšího prvku tuto vlastnost můžeme
# lehce pokazit. Klíčové pozorování je, že její obnovení je snadné
# (a zejména rychlé). Začneme od indexu ‹i = 0› a opakovaně (tak
# dlouho, dokud index ‹i› ukazuje dovnitř neuspořádané části pole):
#
#  • vybereme index největšího prvku z možností ‹i›, ‹2*i + 1› nebo
#    ‹2*i + 2› – pokud jsme vybrali ‹i›, jsme hotovi;
#  • v opačném případě vyměníme vybraný prvek s tím na indexu ‹i›
#    a ‹i› nastavíme na index vybraný v předchozím kroku.
#
# Mělo by být vidět, že za předpokladu, že před výměnou největšího
# prvku měl seznam vlastnosti haldy, uvedenou procedurou je opět
# získá (její obvyklý název je ‹sift_down›). Zbývá tedy zajistit,
# aby mělo vstupní pole tyto vlastnosti i před samotným začátkem
# řazení.
#
# Toho dosáhneme například tak, že budeme opakovaně spouštět
# proceduru ‹sift_down› s počáteční hodnotou ‹i› nastavenou postupně
# na hodnoty ⟦n/2, n/2 - 1, …, 0⟧ kde ⟦n⟧ je délka vstupního
# seznamu. Proč tato procedura funguje se dozvíte například v článku
# „Heapsort“ v anglické wikipedii.

def heapsort(records: List[int]) -> None:
    pass


def test_parameters() -> List[Tuple[int, int, int]]:
    result = []
    for high in range(10):
        for low in range(high):
            for count in range(1, 5):
                result.append((low, high, count))
    return result


def main() -> None:
    heapsort([])  # should not crash
    for low, high, count in test_parameters():
        values = range(low, high)
        lists = combinations_with_replacement(values, count)
        for combination in lists:
            for permutation in permutations(combination):
                records = list(permutation)
                expected = list(combination)
                heapsort(records)
                assert records == expected


if __name__ == "__main__":
    main()
