from typing import List, Set, Optional


# Mějme následující problém: na vstupu je zadaný seznam čísel a
# počáteční index. V každém kroku k aktuálnímu indexu přičteme
# hodnotu na tomto indexu uloženou. Mohou nastat tyto možnosti:
#
#  1. index po konečném počtu iterací „vypadne“ z rozsahu seznamu,
#  2. výpočet se zacyklí a bude navštěvovat nějakou množinu indexů
#     „donekonečna“.
#
# Zajímá nás která možnost nastane, a v případě 2 také délka cyklu,
# který se bude opakovat (t.j. velikost množiny indexů, které se
# budou v cyklu navštěvovány).
#
# V této ukázce naprogramujeme čistou funkci ‹cycle›, která tento
# problém řeší. Problém rozdělíme na dvě části: nejprve zjistíme,
# která z možností nastala. Poté, je-li to možnost 2, zjistíme délku
# cyklu. Jako cvičení si můžete zkusit implementovat verzi, která
# problém vyřeší na jeden průchod, za cenu uložení dodatečné
# informace.

# Použijeme koncovou rekurzi, ale tato bude mít trochu jiný
# charakter, než v předchozích ukázkách: problém, který řešíme, nemá
# žádnou jasnou (statickou) strukturu podproblémů, a nemůžeme tedy
# použít jednoduchou strukturální rekurzi.

# Hlavní myšlenka rekurze nicméně zůstane zachována: nejprve
# vyřešíme elementární případy, kdy je odpověď na první pohled
# jasná. Ty zbývající musíme nějakým vhodným způsobem převést na
# jednodušší instance: to, v čem se tento příklad liší od těch
# předchozích je, že nemáme k dispozici jasného kandidáta na vhodnou
# jednodušší instanci (chybí nám již zmiňovaná struktura
# podproblémů).

# Jak tedy měřit jednoduchost? Neexistuje žel žádná univerzální
# odpověď ani univerzální postup, a „uvidět“ vhodné řešení vyžaduje
# určitý cvik.

# Zaměřme se tedy na funkci ‹cycle_detect›, která bude zjišťovat,
# jestli se výpočet zacyklí nebo nikoliv. V tomto případě se jako
# vhodné měřítko jednoduchosti jeví kritérium „kolik indexů jsme
# ještě během výpočtu nenavštívili?“. Jednou z indicií je i to, že
# když je tento počet 0, stojíme před elementárním případem – index
# je buď platný (a tedy navštívený: našli jsme cyklus) nebo
# neplatný. Pro žádný složitější případ nezbývá prostor. Máme tedy
# jakousi záruku, že dokážeme-li postupně toto číslo snižovat, dříve
# nebo později narazíme na elementární problém. To je dobře.

# Z praktického hlediska je ale lepší pamatovat si množinu použitých
# indexů, nikoliv těch nepoužitých: to ale není problém, protože
# tyto množiny jsou ve velmi jednoduchém vztahu (jsou vzájemnými
# doplňky v množině všech platných indexů). Přidáme-li index do
# množiny navštívených indexů, je to totéž, jako bychom jej odebrali
# z množiny indexů nenavštívených.

# Funkce ‹cycle_detect› tedy bude mít 3 parametry: samotný seznam
# čísel, aktuální index a množinu již navštívených indexů. Výsledkem
# pak bude libovolný index, který se během výpočtu zopakoval
# (existuje-li, jinak ‹None›).

def cycle_detect(numbers: List[int], index: int,
                 visited: Set[int]) -> Optional[int]:

    # Podobně jako v předchozím, nejprve vyřešíme jednoduché
    # případy: je-li ‹index› mimo meze seznamu ‹numbers›, není co
    # řešit: vracíme ‹None›.

    if index < 0 or index >= len(numbers):
        return None

    # Naopak, je-li ‹index› přítomen v množině ‹visited›, víme, že
    # se během výpočtu zopakoval a můžeme jej tedy vrátit.

    if index in visited:
        return index

    # Ve zbývajících případech nemůžeme přímo rozhodnout. Můžeme ale
    # aktuální index označit za navštívený, provést krok výpočtu, a
    # novou instanci problému prohlásit za jednodušší: díky tomu
    # můžeme zbytek práce bezpečně delegovat na rekurzivní volání
    # ‹cycle_detect›.

    # Vzhledem k předchozímu víme, že ‹index› dosud nebyl
    # navštívený, tedy jeho přidáním se množina ‹visited› zvětší o
    # 1, a tedy počet nenavštívených indexů o 1 klesne. Víme tedy,
    # že takto formulovaná nová instance je blíže elementárnímu
    # případu než ta stávající.

    jump_to = index + numbers[index]
    return cycle_detect(numbers, jump_to, visited | {index})


# Funkce ‹cycle_length› je ještě o něco zapeklitější. Nejlepší míra
# „jednoduchosti“ je zde počet kroků, které musíme provést, abychom
# se z indexu ‹index› dostali na index ‹start›. Tato informace ale
# není vůbec nikde ve funkci přítomna, a není ani jasné, že je tento
# počet konečný. Skutečně, vhodnou volbou parametrů můžeme způsobit,
# že funkce ‹cycle_length› nikdy neskončí (například ‹numbers = [1,
# 0], start = 0, index = 1›).

# Z pátého týdne ale víme, že funkce mohou mít «vstupní podmínku»:
# toho zde s výhodou využijeme. Aby funkce ‹cycle_length› smysluplně
# fungovala, musí platit, že index ‹start› je z indexu ‹index›
# dosažitelný konečným počtem kroků výpočtu – toto kritérium tedy
# zvolíme jako vstupní podmínku.

def cycle_length(numbers: List[int], index: int,
                 start: int, count: int) -> int:

    # Protože budeme začínat v situaci, kdy platí ‹index == start›,
    # ale ještě jsme žádný krok výpočtu neprovedli (‹count› je 0),
    # musíme si elementární případ pohlídat: ten totiž nastane pouze
    # je-li ‹count› alespoň 1.

    if count and index == start:
        return count

    # Nyní zbývá vyřešit rekurzivní volání. Ze vstupní podmínky
    # víme, že z ‹index› do ‹start› se dostaneme konečným počtem
    # kroků výpočtu. Provedeme-li tedy krok výpočtu z indexu
    # ‹index›, tato vzdálenost se o jedna zmenší. Protože byla na
    # začátku konečná (byla splněna vstupní podmínka), bude jistě
    # konečná i po provedení kroku výpočtu: vstupní podmínka funkce
    # ‹cycle_length› je i v nové situaci splněna (toto je velmi
    # důležité ověřit!) a můžeme tedy provést rekurzivní volání.
    # Zároveň víme, že se jedná o „jednodušší“ instanci (vzdálenost
    # se nutně zmenšila).

    jump_to = index + numbers[index]
    return cycle_length(numbers, jump_to, start, count + 1)


# Nyní už je jednoduché funkce zkombinovat do funkce ‹cycle›.
# Všimněte si, že výstupní podmínka funkce ‹cycle_detect› nám
# zaručuje splnění vstupní podmínky funkce ‹cycle_length›.

def cycle(numbers: List[int], start: int) -> int:
    cycle_start = cycle_detect(numbers, start, set())

    if cycle_start is None:
        return 0

    return cycle_length(numbers, cycle_start, cycle_start, 0)


# Na závěr pár jednoduchých testů:

def main() -> None:  # demo
    assert cycle([0], 0) == 1
    assert cycle([1], 0) == 0
    assert cycle([1, -1], 0) == 2
    assert cycle([2, 0, -2], 0) == 2
    assert cycle([2, 0, -2], 1) == 1
    assert cycle([2, 0, -2], 2) == 2
    assert cycle([1, 1, 1], 0) == 0
    assert cycle([1, 1, -1], 0) == 2


if __name__ == '__main__':
    main()
