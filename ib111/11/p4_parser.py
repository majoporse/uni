from typing import List


# V tomto úkolu budeme ze zadaného souboru číst vnořené odrážkové
# seznamy:
#
#  • každý seznam je uvozený jménem na samostatném řádku,
#  • po jméně následuje samotný seznam, přičemž každá odrážka je
#    opět na samostatném řádku,
#  • zanoření odrážky lze rozeznat podle počtu mezer před odrážkou
#    (znakem ‹-›): 1 mezera značí odrážku první úrovně, 2 mezery
#    odrážku druhé úrovně, atd.,
#  • mezi sousedními řádky se může úroveň zanoření zvýšit nejvýše
#    o jedna, snížit se ale může libovolně.
#
# Příklad zanořeného seznamu (v souboru je takových několik,
# oddělených prázdným řádkem):
#
#    List 1
#     - Item 1
#      - Item 1.1
#      - Item 1.2
#       - Item 1.2.1
#        - Item 1.2.1.1
#      - Item 1.3
#       - Item 1.3.1
#     - Item 2
#
# Seznam budeme na výstupu reprezentovat dvěma třídami:
#
#  • ‹Item› reprezentuje odrážku s textem v atributu ‹text› a
#    případným podseznamem v atributu ‹sublists›,
#  • ‹Itemize› pak reprezentuje seznam jako celek, se jménem
#    ‹name› a odrážkami první úrovně v seznamu ‹items›.

class Item:
    def __init__(self, text: str):
        self.text: str = text
        self.sublists: List[Item] = []


class Itemize:
    def __init__(self, name: str):
        self.name: str = name
        self.items: List[Item] = []


# Implementujte podprogram ‹parse_lists›, který vrátí seznam
# instancí třídy ‹Itemize›, které přečte ze souboru s názvem
# ‹filename›.  Můžete předpokládat, že soubor obsahuje pouze správně
# formátované seznamy a mezi každými dvěma seznamy je jeden prázdný
# řádek.

def parse_lists(filename: str) -> List[Itemize]:
    pass


def main() -> None:
    l1, l2, l3 = parse_lists("zz.list_parser.txt")

    check_l1(l1)
    check_l2(l2)
    check_l3(l3)


def check_l1(itemize: Itemize) -> None:
    assert itemize.name == "first_list"
    i1, i2, i3 = itemize.items
    i21, i22 = i2.sublists

    assert len(i1.sublists) == 0
    assert len(i3.sublists) == 0

    assert i1.text == "Item 1"
    assert i2.text == 'Item 2'
    assert i21.text == "Item 2.1"
    assert i22.text == "Item 2.2"
    assert i3.text == "Item 3"


def check_l2(itemize: Itemize) -> None:
    assert itemize.name == "second_list"
    i1, i2 = itemize.items
    i11, = i1.sublists
    i21, = i2.sublists

    assert i1.text == "Item 1"
    assert i11.text == "Item 1.1"
    assert i2.text == "Item 2"
    assert i21.text == "Item 2.1"


def check_l3(itemize: Itemize) -> None:
    assert itemize.name == "third_list"
    i1, = itemize.items
    i2, = i1.sublists
    i3, = i2.sublists
    i4, = i3.sublists
    assert i4.text == "Item 1.1.1.1"
    assert len(i4.sublists) == 0


if __name__ == '__main__':
    main()
