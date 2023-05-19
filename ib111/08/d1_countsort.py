from typing import List, Tuple
from itertools import permutations, combinations, combinations_with_replacement

# V této ukázce se budeme zabývat dvěma velmi jednoduchými řadicími
# algoritmy založenými na počítání.


# První algoritmus funguje pro seznamy, ve kterých se žádná hodnota
# neopakuje. Pracuje na velmi jednoduchém principu:

#  • uvažme libovolný prvek ⟦Rᵢ⟧ vstupního seznamu,
#  • spočítejme kolik se v seznamu nachází celkem prvků, které jsou
#    menší než ⟦Rᵢ⟧; tuto hodnotu označme ⟦cᵢ⟧,
#  • v seřazeném seznamu se musí ⟦Rᵢ⟧ objevit na indexu ⟦cᵢ⟧: index
#    (je-li počítán od nuly) je právě počet prvků, které dané
#    hodnotě v seznamu předchází.

# Spočítáme-li tedy hodnotu ⟦cᵢ⟧ pro každý vstupní prvek, můžeme již
# přímočaře sestavit výstupní seznam: ke každému prvku známe index,
# na který ho chceme uložit. Čistá funkce ‹count_sort› tuto myšlenku
# realizuje:

def count_sort(records: List[int]) -> List[int]:

    # Protože budeme často iterovat sekvencí indexů seznamu
    # ‹records›, uložíme si tuto sekvenci do pomocné proměnné.

    indices = range(len(records))

    # Dále si nachystáme dva seznamy: v jednom budeme počítat
    # hodnoty ⟦cᵢ⟧, do toho druhého potom vstupní prvky uložíme
    # vzestupně seřazené.

    counts = [0 for _ in indices]
    result = [0 for _ in indices]

    # Hlavní cyklus vypočte do seznamu ‹counts› jednotlivé hodnoty
    # ⟦cᵢ⟧. Nejjednodušeji získáme ⟦cᵢ⟧ tak, že spočítáme všechna
    # ⟦Rⱼ⟧ taková, že platí ⟦Rⱼ < Rᵢ⟧.
    #
    # Abychom si ale ušetřili práci, uvědomíme si, že není potřeba
    # nejprve při výpočtu ⟦cᵢ⟧ vyhodnotit ⟦Rⱼ < Rᵢ⟧ a později při
    # výpočtu ⟦cⱼ⟧ vyhodnotit ⟦Rᵢ < Rⱼ⟧.
    #
    # Protože beztak předpokládáme, že se prvky neopakují, platí pro
    # ⟦i ≠ j⟧ právě jedna z těchto dvou možností. Platí-li tedy ⟦Rⱼ
    # < Rᵢ⟧, můžeme srovnání započítat do ⟦cᵢ⟧ (našli jsme prvek
    # menší než ⟦Rᵢ⟧) a naopak, platí-li ⟦Rᵢ < Rⱼ⟧, srovnání rovnou
    # započteme do ⟦cⱼ⟧.

    for i in indices:
        for j in range(i):
            if records[j] < records[i]:
                counts[i] += 1
            else:
                counts[j] += 1

    # Zbývá tedy už jen sestavit výsledný seznam. Připomínáme, že
    # hodnota ⟦Rᵢ⟧ je v programu k dispozici jako ‹records[i]› a
    # odpovídající hodnotu ⟦cᵢ⟧ máme uloženou v ‹counts[i]›.

    for i in indices:
        result[counts[i]] = records[i]

    # Protože hodnoty se na vstupu neopakují, je v ‹counts› uložena
    # permutace indexů seznamu ‹records›: máme tedy zaručeno, že
    # zapíšeme na každý index seznamu ‹result›, a zároveň, že žádnou
    # hodnotu ze seznamu ‹records› neztratíme (nepřepíšeme). To, že
    # výsledný seznam ‹result› bude vzestupně seřazený, je pak již
    # zřejmé z předchozího.

    return result


# Druhý algoritmus je v jistém smyslu „opačný“ než ten první: bude
# pracovat se seznamy, které obsahují pouze hodnoty z předem daného,
# nepříliš velkého rozsahu ⟦⟨l, h⟩⟧. Protože hodnot je málo, budou
# se v delších seznamech často opakovat. Algoritmus je také velmi
# jednoduchý:
#
#  1. pro každou hodnotu z rozsahu ⟦v ∈ ⟨l, h⟩⟧ spočítáme, kolikrát
#     se ve vstupním seznamu nachází; tento počet označíme ⟦cᵢ⟧ kde
#     ⟦i = v - l⟧,
#  2. s použitím této informace sestavíme výsledný seznam tak, že
#     pro každou hodnotu ⟦v ∈ ⟨l, h⟩⟧ do něj vložíme ⟦cᵢ⟧ kopií
#     hodnoty ⟦v⟧ (zde opět ⟦i = v - l⟧).
#
# Tento algoritmus je realizován čistou funkcí ‹distribution_sort›:

def distribution_sort(records: List[int], low: int,
                      high: int) -> List[int]:

    # Sekvenci všech hodnot, které se na vstupu mohou objevit si, ve
    # vzestupném pořadí, uložíme do proměnné ‹values›. Zároveň si
    # nachystáme seznam ‹counts›, ve kterém budeme počítat hodnoty
    # ⟦cᵢ⟧.

    values = range(low, high)
    counts = [0 for _ in values]

    # Nyní zjistíme počet výskytů každé hodnoty z ‹values› ve
    # vstupním seznamu ‹records›:

    for record in records:
        counts[record - low] += 1

    # A sestavíme výsledný seznam.

    result = []
    for value in values:
        for _ in range(counts[value - low]):
            result.append(value)

    return result


# Přestože řadicí algoritmy, které jsme implementovali, jsou velmi
# jednoduché, není těžké v nich udělat chybu. A to navíc třeba
# takovou, že se bude projevovat jen vzácně. Proto tyto algoritmy
# otestujeme obzvlášť důkladně. Funkce definovaná níže popisuje
# parametry seznamů, které budeme testovat: rozsah hodnot (hodnoty
# budou spadat do rozsahu ‹low <= value < high›) a počet prvků. Poté
# vygenerujeme všechny vzestupně seřazené seznamy tak, aby splnily
# vstupní podmínky (v případě funkce ‹count_sort› se hodnoty nesmí
# opakovat) a pro každou permutaci každého seznamu ověříme, že ji
# příslušný algoritmus seřadí správně.

def main() -> None:  # demo

    for low, high, count in test_parameters():
        if count > high - low:
            continue
        lists1 = combinations(range(low, high), count)
        for combination in lists1:
            for permutation in permutations(combination):
                result = count_sort(list(permutation))
                assert result == list(combination)

    for low, high, count in test_parameters():
        values = range(low, high)
        lists2 = combinations_with_replacement(values, count)
        for combination in lists2:
            for permutation in permutations(combination):
                records = list(permutation)
                result = distribution_sort(records, low, high)
                assert result == list(combination)


def test_parameters() -> List[Tuple[int, int, int]]:
    result = []
    for high in range(10):
        for low in range(high):
            for count in range(1, 5):
                result.append((low, high, count))
    return result


if __name__ == '__main__':
    main()
