from math import pi, sin, cos, sqrt, isclose

# V tomto příkladu budeme počítat základní vlastnosti geometrických
# objektů, které budeme popisovat n-ticemi (zejména čísel). Příklad
# slouží k seznámení s typovou anotací parametrů a návratových
# hodnot podprogramů (funkcí).

# Jak již víte z přednášky, anotace základních typů (‹int›, ‹float›,
# ‹str›, atp.) se zapisuje přímo názvem typu, zatímco anotace
# složených typů vyžaduje definice typů z modulu ‹typing›. Jedná se
# zejména o seznamy (v anotacích zapisujeme jako ‹List[element]›,
# kde ‹element› je typová anotace platná pro každý prvek seznamu) a
# n-tice (zapisujeme jako ‹Tuple[x, y, z]› – tento zápis značí
# trojici, kde ‹x›, ‹y› a ‹z› jsou postupně typové anotace pro
# první, druhou a třetí složku n-tice). Konečně případy, kdy
# potřebujeme otypovat hodnotu, která je typu ‹type›, ale nemusí
# nutně existovat (může být v některých případech ‹None›), použijeme
# anotaci ‹Optional[type]›.

from typing import List, Tuple, Optional


# Jako první si definujeme čistou funkci pro výpočet obsahu kruhu
# (anglicky disc), která má jediný parametr typu ‹float› a jejíž
# výsledkem je opět číslo typu ‹float›. Tím, že tyto skutečnosti
# zapíšeme do programu jako anotace de-facto deklarujeme vstupní a
# výstupní podmínky funkce: vstupní podmínkou je, že skutečná
# hodnota předávaného parametru je typu ‹float›, zatímco výstupní
# je, že návratová hodnota je též typu ‹float›. Pro jistotu
# připomínáme, že za splnění «vstupní» podmínky zodpovídá
# «volající», zatímco za splnění «výstupní» podmínky zodpovídá
# «volaná» funkce.

# Program ‹mypy› nám pro takto anotovanou funkci zaručí dvě věci:
# jednak, že omylem funkci nezavoláme se špatným typem parametru
# (neporušíme vstupní podmínku na typy), třeba s hodnotou typu
# řetězec. Dále pak kontroluje, že v těle funkce neporušujeme
# výstupní podmínku – návratová hodnota je číslo typu ‹float›
# (nevrátíme omylem v žádném příkazu ‹return› ve funkci třeba
# řetězec, nebo ‹None›). K provedení této kontroly není potřeba
# program spouštět.

def disc_area(radius: float) -> float:
    return pi * radius ** 2


# Zatímco pro popis kruhu nám stačí jediné číslo, pro popis
# obdélníku již potřebujeme čísla dvě, výšku a šířku. Máme dvě
# možnosti: můžeme potřebné hodnoty předat jako dva samostatné
# parametry, nebo můžeme obě hodnoty zabalit do n-tice (dvojice).
# Druhý přístup je lepší v případě, kdybychom potřeboval vytvořit
# třeba seznam obdélníků (to bude i náš případ). Proto zvolíme
# přístup s dvojicí čísel. Někdy má smysl složitější typy
# «pojmenovat», a protože s obdélníky budeme pracovat na více
# místech, zavedeme si pro typ dvojice čísel jméno ‹Rectangle›:

Rectangle = Tuple[float, float]


# Nyní již můžeme přistoupit k samotné definici (opět čisté) funkce
# pro výpočet plochy obdélníku. Výsledkem bude opět číslo.

def rectangle_area(dimensions: Rectangle) -> float:
    width, height = dimensions
    return width * height


# Elipsa reprezentuje podobný případ, kdy potřebujeme k jejímu
# popisu dvě čísla, tentokrát délky jejích dvou poloos. Všimněte si,
# že typ popisující elipsu je identický s typem pro obdélník. S tím
# jsou spojeny určité problémy, které si objasníme níže. Protože
# elipsami se nebudeme dále zabývat, nebudeme tentokrát typ
# pojmenovávat.

def ellipse_area(semiaxes: Tuple[float, float]) -> float:
    major, minor = semiaxes
    return pi * major * minor


# Abychom demonstrovali i nehomogenní n-tice (tj. takové, které mají
# složky různých typů), zadefinujeme si ještě pravidelný n-úhelník,
# který zadáme hlavním poloměrem (tzn. vzdáleností vrcholu od
# středu) a počtem vrcholů (který je na rozdíl od poloměru
# celočíselný).

def polygon_area(polygon: Tuple[float, int]) -> float:
    radius, vertices = polygon
    half_angle = pi / vertices
    half_side = sin(half_angle) * radius
    minor_radius = cos(half_angle) * radius
    return vertices * minor_radius * half_side


# Nyní si definujeme funkci, která budou pracovat s trochu
# složitějšími typy: vstupem bude seznam barevných obdélníků a jedna
# vybraná barva, výsledkem bude celková plocha dané barvy. Pro barvu
# (reprezentovanou řetězcem) si zavedeme typové synonymum: to je
# typicky vhodné v případech, kdy se příslušný typ objevuje jako
# složka n-tice. Uvažte rozdíl mezi čitelností typové anotace
# ‹Tuple[Tuple[int, int], str]› vs. ‹Tuple[Rectangle, Colour]›.

Colour = str


def coloured_area(rectangles: List[Tuple[Rectangle, Colour]],
                  selected_colour: Colour) -> float:

    # Na tomto místě musíme ‹mypy› trochu pomoct, protože literál
    # ‹0› lze interpretovat jako celé i jako desetinné číslo,
    # přičemž výchozí interpretace je celočíselná. V podstatě máme
    # dvě možnosti: můžeme literál zapsat jako ‹0.0›, čím
    # nejednoznačnost odstraníme, nebo přidáme typovou anotaci i
    # proměnné (střadači) ‹area›. Taková anotace se zapisuje na
    # levou stranu přiřazení a syntakticky je stejná jako anotace
    # parametru.

    area: float = 0

    # Cyklus pro sečtení ploch se už od zápisu, na který jsme
    # zvyklí, nijak neliší. Stojí nicméně za zmínku, že ‹mypy› za
    # nás kontroluje krom správného volání funkce ‹rectangle_area›
    # také to, že srovnáváme hodnoty stejných (obecněji
    # kompatibilních) typů – kdybychom omylem srovnali třeba řetězec
    # (barvu) a obdélník (třeba proto, že jsme zaměnili pořadí
    # ‹rect› a ‹colour› při rozbalování hodnoty typu
    # ‹Tuple[Rectangle, Colour]›), ‹mypy› by nás na tuto chybu
    # upozornilo.

    for rect, colour in rectangles:
        if colour == selected_colour:
            area += rectangle_area(rect)
    return area


# Dále napíšeme funkci, která ze seznamu obdélníků vybere ten
# s největší plochou, existuje-li takový právě jeden. Je zde vidět,
# že návratový typ může být, podobně jako typy parametrů, složitější
# – připomínáme, že ‹Optional[type]› znamená, že hodnota může být
# buď typu ‹type› nebo ‹None› (vzpomeňte si také, že ‹Rectangle› je
# synonymum pro ‹Tuple[float, float]›).

def largest_rectangle(rectangles: List[Rectangle]) \
        -> Optional[Rectangle]:

    if len(rectangles) == 0:
        return None

    largest = rectangles[0]
    count = 0

    for r in rectangles:
        if isclose(rectangle_area(r), rectangle_area(largest)):
            count += 1
        elif rectangle_area(r) > rectangle_area(largest):
            count = 1
            largest = r

    return largest if count == 1 else None


# Konečně napíšeme funkci, která ze seznamu obdélníků vybere ty,
# které mají plochu stejnou nebo větší, než je průměrná plocha
# celého vstupního seznamu (který musí být neprázdný).

def large_rectangles(rectangles: List[Rectangle]) \
        -> List[Rectangle]:
    total = sum([rectangle_area(r) for r in rectangles])
    average = total / len(rectangles)
    result = []
    for r in rectangles:
        if rectangle_area(r) >= average:
            result.append(r)
    return result


# Nyní zbývá pouze popsané funkce otestovat:

def main() -> None:  # demo
    unit_rectangle = (1, 1)
    assert isclose(rectangle_area(unit_rectangle), 1)
    assert isclose(rectangle_area((2, 2)), 4)
    assert isclose(polygon_area((sqrt(2), 4)), 4)
    assert isclose(polygon_area((1, 6)), 2.5980762113533)
    assert isclose(ellipse_area((1, 1)), 3.1415926535898)
    assert isclose(ellipse_area((2, 6)), 37.699111843078)
    assert isclose(ellipse_area((12.532, 8.4444)), 332.4597362298)

    # Na začátku jsme zmiňovali, že elipsu a obdélník reprezentujeme
    # stejným typem, a že by to mohlo vést k určitým problémům.
    # Samozřejmě, nemůže se stát nic horšího, než co by se stalo,
    # kdybychom anotace nepoužili vůbec, nicméně musíme si zároveň
    # uvědomit, že typové anotace nejsou všemožné, a ani před něčím,
    # co napohled vypadá jako typová chyba, nás nemusí ochránit.
    # Uvažte následující (zakomentovaný) příkaz – protože
    # ‹unit_rectangle› je typu ‹Tuple[float, float]› a funkce
    # ‹ellipse_area› očekává parametr téhož typu, je z pohledu
    # ‹mypy› takové volání v pořádku. Přesto je zřejmé, že takovéto
    # použití nebylo zamýšleno, a téměř s jistotou povede k chybě
    # v programu. Tuto konkrétní situaci lze lépe řešit použitím
    # «složených datových typů», které si ukážeme přespříští týden.

    pass  # assert ellipse_area(unit_rectangle) == 1

    red, green, blue = "red", "green", "blue"
    red_1 = ((1, 1), red)
    red_2 = ((5, 6), red)
    green_1 = ((1, 1), green)
    green_2 = ((5, 6), green)
    blue_1 = ((2, 3), blue)
    assert isclose(coloured_area([red_1, green_1], red), 1)
    assert isclose(coloured_area([red_1, red_2], red), 31)
    assert isclose(coloured_area([red_1, green_2, blue_1], blue), 6)
    assert isclose(coloured_area([red_1, green_1], blue), 0)
    assert largest_rectangle([]) is None
    assert largest_rectangle([(1, 1), (4, 3), (6, 2)]) is None
    assert largest_rectangle([(5, 5), (4, 3), (1, 1)]) == (5, 5)
    assert largest_rectangle([(12, 2), (10.2, 1.5)]) == (12, 2)
    r_1, r_2, r_3 = (1, 3), (5, 5), (7, 2)
    assert large_rectangles([r_1, r_2, r_3]) == [r_2, r_3]
    assert large_rectangles([r_1, r_2]) == [r_2]
    assert large_rectangles([r_1, r_1]) == [r_1, r_1]


if __name__ == '__main__':
    main()
