from math import sqrt

# Uspořádané n-tice jsou v Pythonu velmi podobné seznamům: lze je
# indexovat a iterovat, ptát se na jejich délku funkcí ‹len›, ale
# také například vytvářet (n+m)-tice spojením n-tice s m-ticí. Jak
# jsme již zmiňovali v úvodu, zásadní rozdíl je, že n-tice nemá
# vnitřní přiřazení a nelze ji tedy po vytvoření měnit.

# Ve skutečnosti ale n-tice používáme v programech výrazně jinak
# než seznamy, přestože mají velmi podobnou strukturu a operace.
# V typickém použití obsahuje seznam pouze jeden typ hodnot, ale
# počet hodnot je variabilní. N-tice se chovají opačně: je běžné, že
# obsahují hodnoty různých typů (ale všechny n-tice daného určení
# mají na stejném indexu stejný typ) a mají fixní počet položek.

# Tento princip si demonstrujeme na příkladu, kde budeme pracovat
# s barevnými body v rovině. Body budeme reprezentovat jako trojice
# (souřadnice x, souřadnice y, barva). Každá n-tice, která
# reprezentuje bod, bude mít právě tuto strukturu, a bude mít vždy
# 3 složky (budeme tedy mluvit o trojicích). Navíc bude platit, že
# první dvě složky budou vždy čísla, a třetí složka bude vždy
# řetězec.

# V principu můžeme k těmto složkám přistupovat indexací, ale
# existuje i mnohem lepší zápis – «rozbalení» n-tice do proměnných.
# Srovnejte si zápis ‹x, y, colour = point›, kde dále pracujeme se
# jmény ‹x›, ‹y› a ‹colour›, oproti ‹point[0]› a ‹point[1]› pro
# souřadnice a ‹point[2]› pro barvu. Pro srovnání si můžete v tomto
# příkladu přepsat všechny rozbalení trojic na indexaci a zvážit, co
# se Vám lépe čte.


# Jako první si definujeme jednoduchou (čistou) funkci, která spočte
# Euklidovskou vzdálenost dvou bodů (která samozřejmě nezávisí na
# jejich barvě).
#
# Poznámka: použití ‹_› jako názvu proměnné není z pohledu Pythonu
# ničím zvláštním, jedná se o identifikátor jako kterýkoliv jiný.
# Nicméně jeho použitím indikujeme budoucím čtenářům, že hodnotu
# této proměnné nehodláme používat, a domluvou se tedy jedná
# o zástupný symbol.

def distance(a, b):
    a_x, a_y, _ = a
    b_x, b_y, _ = b
    return sqrt((a_x - b_x) ** 2 + (a_y - b_y) ** 2)


# Dále si definujeme funkci, která v neprázdném seznamu najde barvu
# „nejlevějšího“ bodu (takového, který má nejmenší x-ovou
# souřadnici).

def leftmost_colour(points):
    x_min, _, result = points[0]

    for x, _, colour in points:
        if x < x_min:
            x_min = x
            result = colour

    return result


# Dále si definujeme čistou funkci, která dostane jako parametry
# seznam bodů ‹points› a barvu ‹colour›, a jejím výsledkem bude bod,
# který se nachází v «těžišti» soustavy bodů dané barvy (a který
# bude stejné barvy). Vstupní podmínkou je, že ‹points› obsahuje
# aspoň jeden bod barvy ‹colour›.

def center_of_gravity(points, colour):
    total_x = 0
    total_y = 0
    count = 0
    for p_x, p_y, p_colour in points:
        if colour == p_colour:
            total_x += p_x
            total_y += p_y
            count += 1

    return (total_x / count, total_y / count, colour)


# Jako poslední si definujeme (opět čistou) funkci, která spočítá
# průměrnou vzdálenost bodů různé barvy. Vstupní podmínkou je, že
# seznam ‹points› musí obsahovat aspoň dva různobarevné body.

def average_nonmatching_distance(points):
    total = 0
    pairs = 0

    for i in range(len(points)):
        for j in range(i):
            _, _, i_colour = points[i]
            _, _, j_colour = points[j]
            if i_colour != j_colour:
                total += distance(points[i], points[j])
                pairs += 1

    return total / pairs


# Testy jsou tentokrát rozsáhlejší, protože jsme definovali větší
# počet funkcí. Pro úsporu horizontálního místa některé testy
# používají lokální aliasy pro funkce, např. ‹dist =
# average_nonmatching_distance› – takové přiřazení znamená, že
# ‹dist› je (lokální) synonymum pro ‹average_nonmatching_distance›.

def main():  # demo
    test_distance()
    test_leftmost_colour()
    test_center_of_gravity()
    test_average_nonmatching_distance()


def test_average_nonmatching_distance():
    r00 = (0, 0, "red")
    r10 = (1, 0, "red")
    b20 = (2, 0, "blue")
    b10 = (1, 0, "blue")
    g30 = (3, 0, "green")
    y20 = (2, 0, "yellow")
    w40 = (4, 0, "white")
    dist = average_nonmatching_distance

    assert dist([r00, b20]) == 2
    assert dist([b10, r00, b20]) == 1.5
    assert dist([r00, b20, b10, g30]) == 1.8
    assert dist([r00, b20, g30]) == 2
    assert dist([r00, b20, b10, r10]) == 1
    assert dist([r00, b10, g30, y20, w40]) == 2


def test_center_of_gravity():
    r00 = (0, 0, "red")
    r22 = (2, 2, "red")
    b20 = (2, 0, "blue")
    b02 = (0, 2, "blue")
    cog = center_of_gravity

    assert cog([r00], "red") == (0, 0, "red")
    assert cog([r00, r22], "red") == (1, 1, "red")
    assert cog([b20, b02], "blue") == (1, 1, "blue")
    assert cog([r00, b02, b20, r22], "red") == (1, 1, "red")
    assert cog([r00, b02, b20, r22], "blue") == (1, 1, "blue")

    g68 = (6, 8, "green")
    g00 = (0, 0, "green")
    g64 = (6, 4, "green")
    g86 = (8, 6, "green")
    green = [g68, g00, g64, g86]

    assert cog([g68, g00, g64], "green") == (4, 4, "green")
    assert cog(green, "green") == (5, 4.5, "green")
    assert cog([r22, b20] + green, "green") == (5, 4.5, "green")


def test_leftmost_colour():
    p1 = (0, 0, "white")
    p2 = (-2, 15, "red")
    p3 = (13, -15, "yellow")
    p4 = (0, 1, "black")

    assert leftmost_colour([p1]) == "white"
    assert leftmost_colour([p3]) == "yellow"
    assert leftmost_colour([p1, p3]) == "white"
    assert leftmost_colour([p1, p3, p4, p2]) == "red"
    assert leftmost_colour([p1, p4]) == "white"
    assert leftmost_colour([p3, p4]) == "black"


def test_distance():
    p1 = (0, 0, "white")
    p2 = (1, 0, "red")

    assert distance(p1, (0, -1, "red")) == 1
    assert distance(p2, p1) == 1
    assert distance(p1, p2) == 1
    assert distance(p1, (2, 0, "black")) == 2
    assert distance(p1, (3, 4, "black")) == 5
    assert distance((-3, -4, "black"), p1) == 5


if __name__ == '__main__':
    main()
