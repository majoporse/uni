from typing import Tuple, Dict, Set

# V této ukázce se budeme zabývat datovým typem «množina». Stejně
# jako u seznamů, slovníků a podobně se jedná o složený typ, který
# má prvky. Množina má některé vlastnosti společné jak se seznamem –
# obsahuje pouze prvky, ale nikoliv klíče, tak se slovníkem –
# podobně jako klíče ve slovníku, hodnoty v množině můžou být
# přítomny nejvýše jednou. Od seznamu se liší mimo jiné tím, že
# množinu nelze indexovat (pouze iterovat).

# Krom omezení na výskyt každého prvku nejvýše jednou poskytuje
# množina «efektivní» test na přítomnost prvku (podobně, jako
# slovník poskytuje efektivní test na přítomnost klíče). Chceme-li
# zjistit, objevuje-li se nějaká hodnota v běžném seznamu, strávíme
# tím čas, který je přímo úměrný počtu prvků tohoto seznamu. Naopak
# v množině lze očekávat, že čas potřebný pro zjištění přítomnosti
# na počtu prvků v množině vůbec nezávisí: trvá přibližně stejně
# dlouho nalézt prvek v množině o deseti prvcích i v množině
# o deseti milionech prvků (takto to funguje v Pythonu – tato
# operace má očekávanou «konstantní» složitost; některé jiné jazyky
# poskytují datový typ množina, kde čas potřebný k zjištění
# přítomnosti prvku závisí na tom, kolik «řádů» má číslo popisující
# její velikost – mluvíme pak o tzv. «logaritmické» složitosti).

# Uvažme zobrazení ⟦f: A × A → A⟧ kde ⟦A ⊆ ℤ⟧ a ⟦f⟧ je zadané
# tabulkou (slovníkem, kde klíč je dvojice čísel a hodnota je číslo
# – rozmyslete si, že takový slovník skutečně reprezentuje tabulku,
# budou-li ve slovníku přítomny všechny potřebné dvojice).
# Například logickou spojku ‹and› lze podobnou tabulkou
# reprezentovat takto (budeme-li reprezentovat ‹True› číslem 1 a
# ‹False› číslem 0):

# │   │ 0 │ 1 │
# ├──▻│──▻┼──▻│
# │ 0 │ 0 │ 0 │
# │ 1 │ 0 │ 1 │

# Jako slovník bychom stejnou tabulku zapsali takto:
#
#     {(0, 0): 0, (0, 1): 0,
#      (1, 0): 0, (1, 1): 1}.
#
# Zobrazení ⟦f⟧ budeme říkat «operace» a budeme jej popisovat
# následujícím typem:

Operation = Dict[Tuple[int, int], int]


# Na vstupu tedy dostaneme tabulku, která reprezentuje ⟦f⟧ a množinu
# čísel ⟦B ⊆ A⟧. Naším úkolem bude nalézt nejmenší množinu čísel ⟦C⟧
# takovou, že:
#
#  • ⟦B ⊆ C⟧, tedy C obsahuje všechny zadané prvky,
#  • pro každé ⟦(x, y) ∈ B × B⟧ platí ⟦f(x, y) ∈ B⟧ – říkáme, že
#    množina ⟦C⟧ je «uzavřena» na operaci ⟦f⟧.

def closure(set_b: Set[int], operation_f: Operation) -> Set[int]:

    # Jak budeme postupovat? Množinu ⟦C⟧ budeme budovat postupně:
    # začneme tím, že do ⟦C⟧ vložíme všechny prvky z ⟦B⟧:

    set_c = set_b.copy()

    # Dále budeme procházet všechny dvojice ze součinu ⟦C × C⟧, a
    # nalezneme-li takovou, že její obraz ještě v množině ⟦C⟧ není,
    # přidáme jej tam. Toto ale nemůžeme udělat přímo: přidat prvek
    # do množiny, kterou právě iterujeme, je zakázáno (protože by
    # bylo těžké zaručit, aby byla iterace konzistentní – tzn. aby
    # se nestalo, že v iteraci uvidíme některé, ale ne všechny, nové
    # prvky).

    # Proto si napíšeme pomocnou funkci ‹find_missing›, která najde
    # chybějící prvky a vrátí je jako množinu. Stojíme před dvěma
    # problémy: po přidání nových prvků musíme celou proceduru
    # opakovat, protože vznikly nové dvojice. Tento problém vyřešíme
    # tak, že budeme funkci ‹find_missing› volat opakovaně, tak
    # dlouho, dokud bude nalézat nové prvky.

    # Druhý problém je, že tento postup není příliš efektivní: rádi
    # bychom se vyhnuli procházení dvojic, které jsme již
    # kontrolovali. To sice samozřejmě lze, ale značně by nám to
    # zkomplikovalo kód, proto tentokrát ušetříme práci sobě (a
    # nějakou tím přiděláme počítači).

    to_add = find_missing(set_c, operation_f)

    while len(to_add) != 0:
        for x in to_add:
            set_c.add(x)
        to_add = find_missing(set_c, operation_f)

    return set_c


# Pomocná (čistá) funkce ‹find_missing› je velmi jednoduchá: projde
# všechny dvojice z ⟦C × C⟧ (tedy součinu množiny ‹set_c› se sebou
# samou), a zobrazí-li se tato dvojice na prvek, který v ‹set_c›
# zatím není, přidá ho do své návratové hodnoty.

def find_missing(set_c: Set[int], operation_f: Operation) \
        -> Set[int]:
    result: Set[int] = set()

    for x in set_c:
        for y in set_c:
            to_add = operation_f[(x, y)]
            if to_add not in set_c:
                result.add(to_add)

    return result


# Zbývá otestovat, že funkce ‹closure› se chová, jak čekáme.

def main() -> None:  # demo
    op_and = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 1}
    op_xor = {(0, 0): 0, (1, 0): 1, (0, 1): 1, (1, 1): 0}
    set_false = set([0])
    set_true = set([1])
    set_both = set([0, 1])

    assert closure(set_false, op_and) == set_false
    assert closure(set_true, op_and) == set_true
    assert closure(set_both, op_and) == set_both
    assert closure(set_false, op_xor) == set_false
    assert closure(set_true, op_xor) == set_both

    add_mod4 = {(0, 0): 0, (0, 1): 1, (0, 2): 2, (0, 3): 3,
                (1, 0): 1, (1, 1): 2, (1, 2): 3, (1, 3): 0,
                (2, 0): 2, (2, 1): 3, (2, 2): 0, (2, 3): 1,
                (3, 0): 3, (3, 1): 0, (3, 2): 1, (3, 3): 2}

    assert closure(set([0]), add_mod4) == set([0])
    assert closure(set([1]), add_mod4) == set([0, 1, 2, 3])
    assert closure(set([2]), add_mod4) == set([0, 2])
    assert closure(set([3]), add_mod4) == set([0, 1, 2, 3])
    assert closure(set([0, 2]), add_mod4) == set([0, 2])


if __name__ == '__main__':
    main()
