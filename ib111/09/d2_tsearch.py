from typing import Optional


# V této ukázce budeme pracovat se «stromy». Strom je datová
# struktura, která se podobá zřetězenému seznamu, s jedním zásadním
# rozdílem: uzly nemají následníka jednoho, ale několik. Podle toho,
# kolik, dělíme stromy na binární (2 následníci), ternární (3
# následníci), atd. Lze také uvažovat stromy s proměnným počtem
# následníků (takovým se většinou říká n-ární). Počátečnímu uzlu
# (tomu, který nemá ve stromě žádné předchůdce) často říkáme kořen.

# Stromy sdílí se zřetězenými seznamy krom podobné struktury i jednu
# velmi důležitou vlastnost: jsou to «rekurzivní datové struktury».
# Co to znamená? U seznamu to, že následník uzlu seznamu tvoří opět
# seznam (navíc striktně menší seznam). A u stromu zase platí, že
# každý následník je podstrom (striktně menší strom).

# Tato struktura velmi dobře koresponduje s naší představou
# o rekurzi: problém rozdělíme na podproblémy (pro každý podstrom
# vznikne jeden) a dílčí výsledky nějak zkombinujeme na výsledek
# celkový. Elementární (bázové) podproblémy pak tvoří stromy
# o jediném uzlu (takové, které nemají žádné podstromy, známé též
# jako «listy»), případně stromy prázdné (je-li to výhodné).

# Strom budeme reprezentovat analogicky k uzlu zřetězeného seznamu.
# Prázdný strom budeme reprezentovat hodnotou ‹None›.

class Tree:
    def __init__(self, value: int, left: Optional['Tree'] = None,
                 right: Optional['Tree'] = None):
        self.value = value
        self.left = left
        self.right = right


# Jako první příklad na práci se stromy si naprogramujeme test na
# přítomnost hodnoty ve stromě. Vstupem je (potenciálně prázdný)
# strom a hledaná hodnota.

def search(tree: Optional[Tree], value: int) -> bool:

    # Aplikujeme nyní již snad dobře známý postup: nejprve vyřešíme
    # bázové (jednoduché) případy: je-li strom prázdný, hledaná
    # hodnota se v něm jistě nenachází (vracíme ‹False›).

    if tree is None:
        return False

    # Naopak, je-li hledaná hodnota uložena v aktuálním uzlu, můžeme
    # rovnou vrátit ‹True›.

    if value == tree.value:
        return True

    # Zbývají případy, které neumíme řešit přímo: víme ale, že je-li
    # hodnota ve stromě přítomna, musí to být v levém nebo v pravém
    # podstromě. Protože podstromy jsou menší (jednodušší) než celý
    # strom, jedná se o podproblémy, které můžeme řešit rekurzí.
    # Aplikujeme tedy predikát ‹search› na oba podstromy: hodnota je
    # ve stromě přítomna, je-li přítomna alespoň v jednom z jeho
    # podstromů.

    return search(tree.left, value) or search(tree.right, value)


# Nezbývá, než predikát ‹search› otestovat na několika jednoduchých
# vstupech.

def main() -> None:  # demo
    t1 = Tree(7, Tree(2), Tree(1, Tree(5), Tree(6)))
    assert search(t1, 7)
    assert search(t1, 2)
    assert search(t1, 1)
    assert search(t1, 5)
    assert search(t1, 6)
    assert not search(t1, 4)
    t2 = Tree(8, t1, Tree(10))
    assert not search(t2, 4)
    assert search(t2, 8)
    assert search(t2, 10)
    assert search(t2, 1)
    assert search(t2, 5)


if __name__ == '__main__':
    main()
