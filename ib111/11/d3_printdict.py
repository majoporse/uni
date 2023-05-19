from typing import Union, Dict

# Tato ukázka je variací na předchozí: budeme opět zapisovat
# rekurzivní datovou strukturu do souboru, tentokrát na to ale
# použijeme zápis bez rekurze. Nejprve si zadefinujeme potřebné
# typy, zejména třídu ‹NestedDict›. Tato reprezentuje zanořený
# slovník, kde klíče jsou řetězce a hodnoty jsou buď řetězce, nebo
# vnořené slovníky.

NestedDictItem = Union['NestedDict', str]


class NestedDict:
    def __init__(self, items: Dict[str, NestedDictItem]):
        self.items = items


# Výpis slovníku provede procedura ‹print_nested›. Formát výpisu
# bude následovný:
#
#  • je-li ke klíči asociovaná hodnota typu řetězec, klíč a hodnota
#    se vypíšou na jeden řádek, oddělené dvojtečkou, patřičně
#    odsazené dle úrovně zanoření,
#  • je-li hodnota zanořený slovník, klíč se vypíše na samostatný
#    řádek ukončený dvojtečkou a obsah slovníku se vypíše pod něj,
#    odsazený o jednu mezeru navíc.
#
# Klíče seznamu budou seřazeny abecedně. Příklad:
#
#     klíč 1:
#      abecedně první klíč vnořeného slovníku: řetězec
#      další klíč vnořeného slovníku: jiný řetězec
#      třetí klíč:
#       více zanořený klíč: další řetězec
#     klíč 2: řetězec v hlavním slovníku

# Z kapitoly 6 si jistě pamatujete základní datové struktury:
# k procházení rekurzivní struktury bez použití rekurze se bude
# hodit zásobník, který budeme realizovat seznamem a jeho metodami
# ‹append› (vloží prvek na vrchol zásobníku) a ‹pop› (odebere prvek
# z vrcholu).

def print_nested(records: NestedDict, path: str) -> None:

    # Začneme tím, že si otevřeme soubor ‹path› pro zápis a výsledek
    # si poznačíme do proměnné ‹out›.

    with open(path, 'w') as out:

        # Dále si nachystáme zásobník, ve kterém budeme uchovávat
        # rozpracované podúlohy. Tyto budeme reprezentovat jako
        # dvojice:
        #
        #  • jednak si musíme pamatovat, který zanořený slovník na
        #    dané úrovni zanoření právě zpracováváme (toto bude
        #    první složka),
        #  • dále pak u každého rozpracovaného slovníku potřebujeme
        #    vědět, které klíče je ještě potřeba zpracovat (resp.
        #    které jsme již vypsali).
        #
        # Pro začátek na zásobník vložíme „hlavní“ slovník (ten,
        # který jsme dostali jako parametr) a poznačíme si, že
        # musíme zpracovat všechny jeho klíče. Protože klíče ke
        # zpracování budeme odebírat z konce seznamu (kvůli
        # efektivitě), vložíme je do seznamu v opačném abecedním
        # pořadí.

        stack = []
        stack.append((records.items,
                     list(sorted(records.items.keys(),
                                 reverse=True))))

        # Tím máme nachystaný počáteční stav a dále budeme
        # zpracovávat jednotlivé podúlohy, a každou, kterou
        # dokončíme ze zásobníku odstraníme. Podúlohy budeme
        # zpracovávat až do chvíle, kdy se zásobník zcela vyprázdní.
        # Narazíme-li během zpracování některé podúlohy na další
        # (vnořený slovník), podobně je vložíme do zásobníku.

        while stack:

            # Pracujeme vždy s podúlohou na vrcholu zásobníku, tzn.
            # tou „nejnovější“ (vzpomeňte si, že zásobník je „last
            # in, first out“).

            items, keys = stack[-1]

            # Dojdou-li nám v daném slovníku (podúloze) klíče ke
            # zpracování, jsme hotovi: podúlohu odstraníme ze
            # zásobníku a pokračujeme ve výpočtu s další podúlohou
            # (která se tímto dostala na vrchol).

            if not keys:
                stack.pop()
                continue

            # Množina klíčů ke zpracování nebyla prázdná – stojíme
            # tedy před nedokončenou podúlohou. Ze seznamu
            # nezpracovaných klíčů jeden vybereme a zpracujeme
            # (k tomu budeme potřebovat i odpovídající hodnotu).

            key = keys.pop()
            value = items[key]

            # Pro účely výpisu si spočteme řetězec s mezerami, které
            # je potřeba umístit na začátek řádku – protože „hlavní“
            # slovník je odsazen o 0 mezer, počet mezer je o jedna
            # menší než současná hloubka zásobníku.

            prefix = ' ' * (len(stack) - 1)

            # Nyní se musíme rozhodnout, jakého typu je hodnota,
            # kterou máme zpracovat: je-li to řetězec, vypíšeme jej
            # přímo ke klíči. Naopak, je-li to zanořený slovník,
            # vypíšeme pouze klíč a podslovník zařadíme mezi
            # podúkoly, které je potřeba zpracovat, a to tak, že jej
            # (opět se všemi klíči) vložíme na vrchol zásobníku.

            if isinstance(value, str):
                print(prefix + key + ': ' + value, file=out)
            else:
                print(prefix + key + ':', file=out)
                stack.append((value.items,
                              list(sorted(value.items.keys(),
                                          reverse=True))))


# Proceduru ‹print_nested› si na jednoduchém vstupu ještě
# otestujeme.

def main() -> None:  # demo
    path = 'zt.print_dict.txt'
    d1 = NestedDict({'y': 'foo', 'x': 'bar'})
    d11 = NestedDict({'x': 'baz'})
    d2 = NestedDict({'dictionary 1.1': d11, 'string': 'quux'})
    d = NestedDict({'dictionary 1': d1, 'dictionary 2': d2,
                    'string 1': 'str'})
    print_nested(d, path)
    assert open(path).read() == ('dictionary 1:\n'
                                 ' x: bar\n'
                                 ' y: foo\n'
                                 'dictionary 2:\n'
                                 ' dictionary 1.1:\n'
                                 '  x: baz\n'
                                 ' string: quux\n'
                                 'string 1: str\n')


if __name__ == '__main__':
    main()
