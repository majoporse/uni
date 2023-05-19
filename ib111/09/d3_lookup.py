from typing import Optional, Tuple


# V této ukázce budeme pokračovat v práci s binárními stromy.
# Definice stromu tedy zůstává od předchozí ukázky nezměněna.

class Tree:
    def __init__(self, value: int, left: Optional['Tree'] = None,
                 right: Optional['Tree'] = None):
        self.value = value
        self.left = left
        self.right = right


# Analogií k seřazenému seznamu je takzvaný «vyhledávací strom».
# Tento má tu vlastnost, že všechny hodnoty uložené v levém
# podstromě jsou menší nebo rovny hodnotě uložené v zkoumaném uzlu,
# a naopak, hodnoty v pravém podstromě jsou větší nebo rovny.
# Podobně jako v uspořádaném seznamu, lze ve vyhledávacím stromě
# test na přítomnost hodnoty provést výrazně rychleji, než ve stromě
# obecném.

def lookup(tree: Optional[Tree], value: int) -> bool:

    # Jednoduché případy jsou zcela stejné, jako při hledání
    # v obecném stromě.

    if tree is None:
        return False
    if value == tree.value:
        return True

    # Zajímavá změna se objeví v rekurzivním případě: podobně jako
    # při hledání půlením intervalu můžeme srovnáním hledané hodnoty
    # a hodnoty v aktuálním uzlu rozhodnout, ve kterém podstromě se
    # hledaná hodnota musí nacházet (je-li přítomna). Je-li hledaná
    # hodnota menší, než ta v aktuálním uzlu, víme jistě, že se
    # v pravém podstromě určitě nemůže objevit. Stačí nám tedy
    # vyřešit jediný podproblém, a to test na přítomnost hodnoty
    # v levém podstromě. Protože máme jediný podproblém, nabízí se
    # možnost použít koncovou rekurzi: musí ale navíc platit, že
    # řešení podproblému je přímo i řešením problému. Rozmyslete si,
    # že tomu tak skutečně je!

    if value < tree.value:
        return lookup(tree.left, value)

    # Opačný případ je zcela analogický: můžeme-li vyloučit
    # přítomnost hodnoty v levém podstromě, zbývá jediný podproblém,
    # který je navíc menší než ten aktuální (podstrom je jednodušší
    # než celý strom). Opět postupujeme koncovou rekurzí.

    if value > tree.value:
        return lookup(tree.right, value)

    # Mělo by být zřejmé, že jsme vyčerpali všechny možnosti,
    # program se do tohoto místa tedy nemůže dostat. Tuto skutečnost
    # opět deklarujeme tvrzením ‹False›.

    assert False


# Krom predikátu ‹lookup› zadefinujeme ještě jeden predikát: takový,
# který zjistí, je-li nějaký strom korektním vyhledávacím stromem.
# Predikát ale pro rozklad na podproblémy stačit nebude: lze
# sestavit strom ze dvou korektních vyhledávacích stromů takový, že
# výsledek nebude korektním vyhledávacím stromem, ale lokálně (jen
# z jednoho vrcholu a jeho přímých následníků) to nebude lze poznat.
# Třeba tento: ‹Tree(5, Tree(2, Tree(1), Tree(10)), Tree(8))›.

# Musíme vyřešit «silnější problém»: takový, který nám umožní složit
# správné řešení z vyřešených podproblémů. Jaké jsou lokální
# vlastnosti korektního vyhledávacího stromu? Jsou to:
#
#  • maximum levého podstromu je ≤ hodnota aktuálního uzlu,
#  • minimum pravého podstromu je ≥ hodnota aktuálního uzlu,
#  • levý i pravý podstrom jsou korektní.
#
# Potřebujeme tedy funkci, která zjistí korektnost, minimum a
# maximum daného (pod)stromu: víme už, že z těchto informací umíme
# zjistit korektnost celého stromu. Na to, abychom mohli použít
# rekurzi, musíme ještě zjistit minimum a maximum: za předpokladu,
# že je strom korektní, platí:
#
#  • minimum levého podstromu je zároveň minimum celého stromu,
#  • maximum pravého podstromu je zároveň maximum stromu.
#
# Všechny informace tedy umíme spočítat lokálně, z informacích
# získaných řešením podproblémů. Můžeme tedy přistoupit
# k rekurzivnímu řešení problému.
#
# Abychom si trochu zjednodušili život, přidáme si umělý parametr:
# příhodnou mez, kterou použijeme jako minimum i maximum, je-li
# zadaný strom prázdný (takový strom totiž žádné přirozené meze
# nemá). Tento postup nám oproti variantě s ‹None› ušetří spoustu
# psaní.

def is_correct_rec(tree: Optional[Tree], bound: int) \
        -> Tuple[bool, int, int]:

    # Jako vždy, nejprve vyřešíme jednoduché případy: prázdný strom
    # je korektní (splňuje všechny požadavky). Zároveň nemá žádné
    # přirozené meze, proto použijeme tu, kterou nám volající předal
    # jako výchozí.

    if tree is None:
        return (True, bound, bound)

    # Je-li strom neprázdný, získáme vlastnosti levého i pravého
    # podstromu rekurzivním voláním.

    l_ok, l_min, l_max = is_correct_rec(tree.left, tree.value)
    r_ok, r_min, r_max = is_correct_rec(tree.right, tree.value)

    # Podle kritérií uvedených výše vypočteme, je-li strom jako
    # celek korektní.

    this_ok = l_ok and r_ok and l_max <= tree.value <= r_min

    # Nyní nám stačí sestavit návratovou hodnotu. Není-li strom
    # korektní, nemusíme se správností mezí zabývat: žádný strom,
    # který má nekorektní podstrom, nemůže být korektní, bez ohledu
    # na meze svých podstromů.

    return (this_ok, l_min, r_max)


# Protože jsme potřebovali formulovat silnější problém, má funkce
# ‹is_correct_rec› nesprávné rozhraní: zejména to není predikát
# (výsledkem je n-tice, nikoliv ‹bool›), navíc má nežádoucí parametr
# ‹bound›. Původně zamýšlený predikát ale už pomocí ‹is_correct_rec›
# lehce zapíšeme:

def is_correct(tree: Tree) -> bool:
    ok, _, _ = is_correct_rec(tree, 0)
    return ok


def main() -> None:  # demo
    t1 = Tree(7, Tree(4, Tree(1), Tree(5)), Tree(8))
    assert is_correct(t1)
    assert lookup(t1, 7)
    assert lookup(t1, 5)
    assert lookup(t1, 1)
    assert lookup(t1, 4)
    assert lookup(t1, 8)
    assert not lookup(t1, 9)
    assert not lookup(t1, 2)
    assert not lookup(t1, 6)

    t2 = Tree(5, Tree(2, Tree(1), Tree(10)), Tree(8))
    assert not is_correct(t2)


if __name__ == '__main__':
    main()
