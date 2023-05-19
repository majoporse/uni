from typing import List, Tuple
from itertools import combinations_with_replacement


# V poslední ukázce pro tento týden se budeme zabývat «hledáním»
# v seřazeném seznamu. V krátkých seznamech si můžeme dovolit hledat
# „naivně“: srovnáme hledanou hodnotu postupně s každým prvkem.  Je
# zřejmé, že v nejhorším případě musíme provést tolik srovnání,
# kolik prvků je v prohledávaném seznamu.
#
# Je-li ale seznam seřazený, můžeme hledání velmi výrazně urychlit.
# Technika, kterou k tomu použijeme se jmenuje «půlení intervalu».
# Ač to nemusí být na první pohled zřejmé, je velmi důležité, abyste
# princip této techniky pochopili, protože na ní staví řada
# fundamentálních výsledků, které budete v dalších semestrech
# studovat.

# Základní myšlenkou algoritmu je rozdělit si vstupní seznam na dvě
# přibližně stejně dlouhé poloviny. Je-li hodnota v seznamu
# přítomna, musí se nacházet v jedné z těchto dvou částí. Protože
# celý seznam je seřazený, platí to i o každém jeho podseznamu,
# zejména to tedy platí o našich přibližných polovinách.

# Je-li nějaký hodnota ‹value› přítomná v seznamu ‹list›, musí nutně
# platit ‹min(list) <= value <= max(list)›. Je-li ‹list› navíc
# vzestupně seřazený, platí ‹min(list) == list[0]› a ‹max(list) ==
# list[-1]›. Celkem tedy ‹list[0] <= value <= list[-1]›.

# Protože se jedná o podmínku «nutnou», není-li splněna, můžeme
# s jistotou říci, že se hledaná hodnota v daném (pod)seznamu
# nenachází. Zjistíme-li tedy, že tuto nutnou podmínku některý
# z našich podseznamů porušuje, nemusíme se tímto nadále vůbec
# zabývat: stačí nám vyřešit problém pouze pro zbývající polovinu.

def bin_search(records: List[int], value: int) -> bool:

    # Zbývá nám vyřešit konkrétní zápis této myšlenky. Zejména se
    # chceme vyhnout vytváření nových seznamů: tato operace je
    # drahá, a ve výsledku bychom pak oproti naivnímu hledání nic
    # neušetřili. Můžeme si ale pamatovat «rozsah indexů» ve kterém
    # aktuálně hledáme. Indexy si nazveme ⟦l⟧ (‹low›) a ⟦h⟧
    # (‹high›), a budeme je chápat jako «polouzavřený» interval ⟦⟨l,
    # h)⟧: index ⟦l⟧ (‹low›) do rozsahu patří, index ⟦h⟧ (‹high›) už
    # nikoliv.  Zejména to znamená, že interval je prázdný právě
    # když ‹low == high›.

    # Na začátku výpočtu prohledáváme celý seznam, proměnné ‹low› a
    # ‹high› tedy nastavíme na příslušné hodnoty:

    low, high = 0, len(records)

    # Hledání pokračuje dokud je prohledávaný (pod)seznam neprázdný.
    # Najdeme-li hledanou hodnotu, cyklus ukončíme dříve: skončí-li
    # tedy cyklus pro nesplnění podmínky, hledaná hodnota v seznamu
    # nebyla přítomna (za předpokladu, že hodnota v seznamu byla
    # přítomna, musí být přítomna v prázdném seznamu → spor).

    while low < high:

        # Stávající seznam si rozdělíme na ony avizované „přibližně
        # stejně velké“ části (jejich délka se může lišit
        # o jedničku, byl-li seznam liché délky). Dělení provedeme
        # na indexu ⟦m⟧ (‹mid›). První podseznam je tedy ⟦⟨l, m)⟧.
        # Ten druhý by pak měl být ⟦⟨m, h)⟧, nicméně je praktičtější
        # použít ⟦⟨m + 1, h)⟧.

        # Proč jsme vypustili samotné ⟦m⟧ (‹mid›)? Jedná se o právě
        # jeden prvek, se kterým se bude tedy dobře pracovat
        # (nemusíme si hlídat existenci). Navíc nám jeho vyloučení
        # z dalšího hledání zaručuje, že se prohledávaný seznam
        # v každé iteraci zkrátí aspoň o jedničku. Nehrozí nám tak,
        # že se program „zacyklí“ na nějakém okrajovém případu,
        # který jsme neošetřili.

        mid = low + (high - low) // 2

        # Jako první ověříme, zda na indexu ⟦m⟧ není uložena hledaná
        # hodnota: pokud ano, hledání ukončíme. V opačném případě
        # víme, že index ⟦m⟧ můžeme z dalších úvah vypustit.

        # Navíc musíme zdůvodnit, proč musí nutně index ⟦m⟧
        # v některé iteraci ukazovat na hledanou hodnotu, byla-li
        # v seznamu přítomna. Uvědomme si, že struktura algoritmu je
        # taková, že je-li prvek přítomen, je nutně přítomen
        # v rozsahu ⟦⟨l, h)⟧. Zároveň se v každé iteraci interval
        # striktně zmenšuje, a ⟦m⟧ vždy leží v tomto intervalu.

        # Konečně nejmenší neprázdný interval vede na ⟦m = l = h -
        # 1⟧, jediný prvek v tomto intervalu je tudíž na indexu ⟦m⟧,
        # a hledanou hodnotu tedy zaručeně najdeme nejpozději ve
        # chvíli, kdy ⟦l = h - 1⟧.

        if records[mid] == value:
            return True

        # Dále tedy zkontrolujeme podseznam ⟦⟨l, m)⟧: je-li ‹value›
        # v této části seznamu, platí již zmiňovaná nutná podmínka:
        # ‹records[low] <= value <= records[mid]›, zejména pak její
        # druhá část: ‹value <= records[mid]›.

        # Tuto znegujeme na ‹records[mid] < value›: platí-li tato
        # negace, nutná podmínka je porušena a hodnota ‹value› se
        # v této části seznamu nenachází. Proto prohledávaný
        # interval zúžíme na ⟦⟨m + 1, h)⟧ a pokračujeme další
        # iterací.

        if records[mid] < value:
            low = mid + 1

        # Zbývá provést analogickou kontrolu pro rozsah ⟦⟨m, h)⟧.
        # Můžeme-li přítomnost ‹value› v této části vyloučit, budeme
        # se v další iteraci zabývat už pouze podseznamem ⟦⟨l, m)⟧.

        if records[mid] > value:
            high = mid

    # Jak již bylo zmíněno dříve, dojde-li k ukončení cyklu proto,
    # že nám k prohledání zbyl prázdný podseznam, víme, že hledaný
    # prvek v seznamu nebyl přítomen. Vrátíme tedy ‹False›.

    return False


# Tím je implementace hotova. Podobně jako u řadicích algoritmů
# budeme hledání půlením intervalu testovat velmi pečlivě: nejprve
# vygenerujeme každý seřazený seznam v daném rozsahu parametrů. Pro
# každý z nich pak ověříme, že výsledek hledání je správný, a to jak
# pro hodnoty, které jsou v seznamu přítomny, tak i hodnoty, které
# v něm nejsou (buď chybí, nebo jsou mimo rozsah hodnot).

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
