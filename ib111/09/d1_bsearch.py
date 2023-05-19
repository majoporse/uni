from typing import List, Tuple
from itertools import combinations_with_replacement


# Minulý týden jsme si, mimo jiné, ukázali algoritmus pro efektivní
# hledání hodnoty v seřazeném seznamu, a to metodou «půlení
# intervalu». Dnes si ukážeme jinou implementaci téhož algoritmu:
# místo cyklu použijeme koncovou rekurzi. Takto zapsaný algoritmus
# nám poskytne trochu jinou perspektivu na známý problém a zároveň
# připomene základní myšlenku rekurze, kterou již znáte z přednášky.
# Při studiu této ukázky Vám doporučujeme otevřít si také ukázku
# ‹08/bin_tree.py› a oba přístupy (iterativní z minulého týdne a
# rekurzivní v tomto souboru) průběžně srovnávat.

# Protože rekurzivní implementace bude potřebovat dodatečné
# parametry, rozdělíme si ji na dva predikáty: ‹bin_search_rec›,
# která provede samotné rekurzivní hledání, a ‹bin_search›, která
# rekurzi pouze nastartuje (a slouží tak zejména jako příjemnější
# rozhraní pro volání funkce ‹bin_search_rec›).

# Chceme-li použít rekurzi, musíme problém formulovat tak, aby měl
# jasně určené podproblémy (nebo podproblém), který je v nějakém
# smyslu menší, než původní problém. Dále pak budeme chtít, aby bylo
# jednoduché odpovědi na podproblémy zkombinovat tak, abychom
# dostali odpověď na původní problém. V případě, kdy je podproblém
# pouze jeden, je často možné použít navíc «koncovou rekurzi»:
# výsledek (vhodně zvoleného) podproblému je přímo i výsledkem
# celého problému. Koncová rekurze má proti té obecné dvě základní
# výhody:
#
#  • takto zapsaný výpočet lze provádět «efektivně» (bez použití
#    dodatečné paměti),
#  • o koncové rekurzi se lépe uvažuje, protože má zvlášť
#    jednoduchou strukturu.

# Na to, abychom „objevili“ v algoritmu vhodné podproblémy, trochu
# si jej zobecníme: místo hledání v seznamu si jej zadefinujeme,
# jako hledání v nějakém souvislém úseku daného seznamu: konkrétně
# v polouzavřeném intervalu ⟦⟨l, h)⟧ kde ⟦l⟧ je dané parametrem
# ‹low› a ⟦h⟧ je dané parametrem ‹high›. Toto by nám již mělo
# nápadně připomínat implementaci z minulého týdne.

# Pro úplnost, predikát ‹bin_search_rec› odpovídá na otázku „je
# hodnota ‹value› přítomna v seznamu ‹records› na některém indexu
# z intervalu ⟦⟨l, h)⟧?“

def bin_search_rec(records: List[int], value: int,
                   low: int, high: int) -> bool:

    # V řešení jednotlivých případů začneme od toho nejjednoduššího:
    # je-li vstupní interval prázdný, hodnota ‹value› se v něm jistě
    # nenachází. Tato podmínka je analogická ukončovací podmínce
    # cyklu ‹while› z iterativní verze. Vrátíme tedy hodnotu ‹False›
    # a jsme hotovi.

    if low == high:
        return False

    # Řešení ostatních případů záleží na tom, ve které části seznamu
    # se musí hodnota nacházet (je-li přítomna). Tyto případy jsou
    # analogické k případům, které iterativní verze ošetřovala
    # v těle cyklu. Nejprve si vybereme vhodný dělící bod ⟦m⟧
    # (zhruba uprostřed intervalu). Zejména platí, že ⟦m⟧
    # (v programu reprezentované proměnnou ‹mid›) vždy spadá do
    # intervalu ⟦⟨l, h)⟧.

    mid = low + (high - low) // 2

    # Je-li tedy hledaná hodnota přímo na indexu ‹mid›, je určitě
    # v intervalu ⟦⟨l, h)⟧ a tedy můžeme odpovědět ‹True›. Argument
    # proč to stačí je analogický k iterativní verzi.

    if records[mid] == value:
        return True

    # Jednoduché případy máme vyřešeny, nyní zbývají ty složitější:
    # totiž ty, které vedou na nějaký podproblém. Je-li hodnota na
    # indexu ⟦m⟧ („uprostřed“ seznamu) menší než ‹value›, znamená
    # to, že je-li hodnota ‹value› v seznamu někde přítomna, musí to
    # být v horní části.
    #
    # Kýžený podproblém je tedy „je hodnota ‹value› přítomna
    # v seznamu ‹records› na indexech z intervalu ⟦⟨m + 1, h)⟧?“ Je
    # zde dobře vidět i struktura koncové rekurze: odpověď na novou
    # otázku je zároveň odpovědí na tu původní (totiž „je ‹value›
    # přítomno v intervalu indexů ⟦⟨l, h)⟧“). Výsledek řešení
    # podproblému můžeme přímo, bez jakýchkoliv dalších úprav,
    # vrátit.

    if records[mid] < value:
        return bin_search_rec(records, value, mid + 1, high)

    # Zbývá poslední možnost: hodnota musí být v spodní části
    # prohledávaného intervalu, a tedy podproblém, který musíme
    # vyřešit, je „je hodnota ‹value› přítomna v intervalu indexů
    # ⟦⟨l, m)⟧?“

    if records[mid] > value:
        return bin_search_rec(records, value, low, mid)

    # Protože jsme pokryli všechny možnosti, do tohoto místa se již
    # program nemůže dostat. Toto naznačíme tvrzením ‹False›.

    assert False


# Samotný predikát ‹bin_search› se již pomocí ‹bin_search_rec›
# vyjádří velice snadno: stačí zvolit interval ⟦⟨l, h)⟧ tak, že
# pokrývá právě všechny platné indexy seznamu ‹records›.

def bin_search(records: List[int], value: int) -> bool:
    return bin_search_rec(records, value, 0, len(records))


# Protože řešený problém je identický jako minulý týden, budou i
# testy identické.

def main() -> None:  # demo
    for low, high, count in test_parameters():
        values = range(low, high)
        lists = combinations_with_replacement(values, count)
        for combination in lists:
            records = list(combination)
            for v in range(low - 1, high + 1):
                assert bin_search(records, v) == (v in records)


def test_parameters() -> List[Tuple[int, int, int]]:
    result = []
    for high in range(10):
        for low in range(high):
            for count in range(0, 8):
                result.append((low, high, count))
    return result


if __name__ == '__main__':
    main()
