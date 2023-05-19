from typing import List, Set


# V tomto příkladu se vrátíme k problému ‹09/cycle.py› z minulého
# týdne. Připomeňme si základní strukturu:
#
#  • vstupem je seznam čísel, a počáteční index,
#  • v každém kroku výpočtu se číslo na aktuálním indexu k tomuto
#    indexu přičte, čím vznikne nový index.
#
# Tento proces se může, ale nemusí, zacyklit. Ve verzi z minulého
# týdne jsme pouze rozhodovali, která možnost nastane. Tentokrát
# bude problém postaven trochu jinak: všechna čísla v seznamu budou
# kladná, a v každém kroku máme možnost rozhodnout se, budeme-li
# číslo přičítat nebo odečítat.

# Naším cílem bude zjistit, nejen existuje-li nějaký cyklus
# (sekvence rozhodnutí vlevo/vpravo taková, že ji lze donekonečna
# opakovat), ale navíc existuje-li takový, že navštíví všechny
# platné indexy. Není těžké si domyslet, že na počátečním indexu
# vůbec nezáleží, protože hledaný cyklus prochází každým indexem, a
# tedy jej můžeme z formulace problému vypustit.

# Problém budeme řešit jak jinak než rekurzí. Hlavní část řešení
# zastřešuje predikát ‹solve_rec›, s následovnými parametry:
#
#  • ‹numbers› je zadaná „hrací plocha“,
#  • ‹index› je současně zkoumaný index,
#  • ‹goal› je index, ke kterému chceme dojít, a konečně
#  • ‹to_visit› je množina dosud nenavštívených indexů.
#
# Predikát odpovídá na otázku: lze se z indexu ‹index› dostat na
# index ‹goal› tak, že každý index z ‹to_visit› se použije právě
# jednou? Zřejmě si dovedete představit, že jakmile vyřešíme tento
# problém, dokážeme již původní otázku na přítomnost cyklu lehce
# vyjádřit jako jeho instanci (chceme se dostat z nějakého indexu na
# tentýž index a použít k tomu právě všechny platné indexy).

def solve_rec(numbers: List[int], index: int, goal: int,
              to_visit: Set[int]) -> bool:

    # Vyřešíme nejprve jednoduché případy. Vypadneme-li z rozsahu
    # indexů, jistě se nám už k indexu ‹goal› nepodaří dojít a
    # odpovídáme zamítavě.

    if index < 0 or index >= len(numbers):
        return False

    # V případě, že jsme na indexu ‹goal› a množina ‹to_visit› je
    # prázdná, je zřejmé, že odpověď je ‹True› (jsme tam, kde máme
    # být, a máme se tam dostat bez použití jakéhokoliv jiného
    # indexu).

    if index == goal and not to_visit:
        return True

    # Konečně případ, kdy se nacházíme na indexu, který není cílem,
    # a zároveň jej již nelze použít (není přítomen v ‹to_visit›):
    # zamítáme. Speciálním případem této podmínky je i stav, kdy je
    # množina ‹to_visit› prázdná.

    if index not in to_visit:
        return False

    # V ostatních případech nelze přímo rozhodnout. Jednodušší
    # instance sestavíme tak, že aktuální index odebereme
    # z ‹to_visit› a posuneme se buď doleva (‹index_left›) nebo
    # doprava (‹index_right›). Do ‹goal› vede přípustná cesta tehdy,
    # když taková existuje v alespoň jedné z takto sestrojených
    # instancí. Instance jsou jednodušší, protože množina ‹to_visit›
    # se zmenšila, a případ, kdy je prázdná je vždy jednoduchý (viz
    # výše).

    remaining = to_visit - {index}
    index_left = index - numbers[index]
    index_right = index + numbers[index]

    return (solve_rec(numbers, index_left, goal, remaining) or
            solve_rec(numbers, index_right, goal, remaining))


# Jak již bylo naznačeno, původní problém již lehce zapíšeme jako
# instanci problému, který řeší predikát ‹solve_rec›.

def solve(numbers: List[int]) -> bool:
    indices = range(len(numbers))
    return solve_rec(numbers, 0, 0, set(indices))


# Řešení jako obvykle otestujeme na jednoduchých příkladech.

def main() -> None:  # demo
    assert not solve([1])
    assert solve([1, 1])
    assert not solve([1, 0, 1])
    assert not solve([1, 1, 1])
    assert solve([1, 1, 2])
    assert not solve([1, 2, 1])
    assert solve([1, 1, 1, 3])
    assert solve([3, 1, 1, 1])
    assert solve([2, 1, 2, 2, 1])
    assert not solve([2, 2, 2, 2, 2])
    assert not solve([2, 2, 1, 2])


if __name__ == '__main__':
    main()
