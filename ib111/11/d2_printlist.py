from typing import List, TextIO


# V této ukázce se zaměříme na rekurzivní procedury pro práci
# s výstupem. Konkrétně se budeme zabývat vnořenými odrážkovými
# seznamy, které budeme v programu reprezentovat jako seznam objektů
# typu ‹Item›. Každá odrážka (instance ‹Item›) v takovém seznamu má
# nějaký vlastní text (atribut ‹text›) a případně seznam pododrážek
# (atribut ‹sublists›).

class Item:
    def __init__(self, text: str):
        self.text: str = text
        self.sublists: List[Item] = []


# Dosud jsme se zabývali prakticky čistě výpočetní rekurzí, nicméně
# to není jediná zajímavá možnost. Zpracování rekurzivních datových
# struktur (jako je třeba i výše popsaná reprezentace vnořených
# odrážkových seznamů) lze často s výhodou zapsat rekurzivně i
# v případě, kdy je účelem nějaký vedlejší efekt, třeba výstup do
# souboru.

# V parametru ‹itemize› budeme proceduře ‹print_itemize_rec›
# předávat relevantní odrážkový seznam, v parametru ‹prefix› budeme
# uchovávat řetězec, který vypíšeme před každou jednotlivou
# odrážkou: tím budeme realizovat zanoření, které by mělo ve výstupu
# vypadat takto:
#
#     - odrážka 1
#      - odrážka druhé úrovně
#      - další odrážka druhé úrovně
#     - odrážka 2
#      - zanořená odrážka
#       - ještě zanořenějši odrážka
#
# Konečně parametr ‹out› je otevřený soubor, do kterého budeme data
# zapisovat. Všimněte si typové anotace (pochází, podobně jako
# ‹List› nebo ‹Tuple› z modulu ‹typing›).
#
# Na této proceduře je zajímavé také to, že bázový případ není
# zmíněn explicitně: pozorný čtenář si ale jistě všimne, že odrážka,
# která již žádné pododrážky nemá, bude mít seznam ‹sublists›
# prázdný. Na prázdném seznamu ale procedura ‹print_itemize_rec›
# neudělá vůbec nic: cyklus v jejím těle se ani jednou neprovede.

def print_itemize_rec(itemize: List[Item], prefix: str,
                      out: TextIO) -> None:
    for i in itemize:
        print(prefix + '- ' + i.text, file=out)
        print_itemize_rec(i.sublists, prefix + ' ', out)


# Procedura ‹print_itemize› uloží seznam do souboru: krom otevření
# souboru pro zápis se stará také o nastartování rekurze.

def print_itemize(itemize: List[Item], path: str) -> None:
    with open(path, 'w') as out:
        print_itemize_rec(itemize, '', out)


# Tím je ukázka kompletní. Program jako obvykle otestujeme na
# jednoduchém vstupu.

def main() -> None:  # demo
    path = 'zt.print_itemize.txt'
    itemize = [Item('foo'), Item('bar'), Item('wibble')]
    itemize[1].sublists.extend([Item('baz'), Item('quux')])
    itemize[1].sublists[0].sublists.append(Item('baz 2'))
    itemize[2].sublists.extend([Item('quuux')])
    print_itemize(itemize, path)
    assert open(path).read() == ('- foo\n'
                                 '- bar\n'
                                 ' - baz\n'
                                 '  - baz 2\n'
                                 ' - quux\n'
                                 '- wibble\n'
                                 ' - quuux\n')


if __name__ == '__main__':
    main()
