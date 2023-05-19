from math import sqrt, sin, cos, radians, acos, pi, isclose


# V této ukázce si napíšeme program, který bude počítat obvod
# trojúhelníka, který ale může být zadaný různými způsoby: tři
# strany, 2 strany a sevřený úhel, dva úhly a libovolná strana.
# Strany budeme značit ⟦a, b, c⟧; úhel mezi ⟦a⟧ a ⟦b⟧ bude ⟦γ⟧
# (‹gamma›), mezi ⟦b⟧ a ⟦c⟧ bude ⟦α⟧ (‹alpha›) a konečně mezi ⟦c⟧ a
# ⟦a⟧ je úhel ⟦β⟧ (‹beta›):
#
#           ● A
#          ╱ ╲
#         ╱ α ╲
#        ╱     ╲
#     c ╱       ╲ b
#      ╱         ╲
#     ╱           ╲
#    ╱ β         γ ╲
# B ●───────────────● C
#           a
#
# Nejjednodušší je samozřejmě výpočet obvodu pro trojúhelník zadaný
# třemi stranami:

def perimeter_sss(a, b, c):
    return a + b + c


# Následuje trojúhelník zadaný dvěma stranami a sevřeným úhlem, kdy
# získáme délku třetí strany použitím kosinové věty.

def perimeter_sas(a, gamma, b):
    c = sqrt(a ** 2 + b ** 2 - 2 * a * b * cos(radians(gamma)))
    return perimeter_sss(a, b, c)


# Dále vyřešíme případ jedné strany a dvou jí přilehlých úhlů, kdy
# použijeme naopak větu sinovou.

def perimeter_asa(alpha, c, beta):
    gamma = radians(180 - alpha - beta)
    alpha = radians(alpha)
    beta = radians(beta)
    a = c * sin(alpha) / sin(gamma)
    b = c * sin(beta) / sin(gamma)
    return perimeter_sss(a, b, c)


# Poslední případ, který budeme řešit, jsou dva úhly a strana
# přilehlá pouze druhému z nich. Tento případ lehce převedeme na
# předchozí.

def perimeter_aas(alpha, gamma, c):
    return perimeter_asa(alpha, c, 180 - alpha - gamma)


# Tím končí samotná implementace, nyní přistoupíme k jejímu
# testování. Asi si uvědomujete, že v předchozím byl relativně velký
# prostor k překlepům a záměnám stran nebo úhlů. Proto budeme
# testovat důkladněji, než bylo dosud obvyklé – budeme postupovat
# podobně, jako v předchozí ukázce. Nejprve si implementujeme 2
# pomocné funkce, které z popisu pomocí 3 délek stran vypočtou dva
# různé úhly:

def get_alpha(a, b, c):
    return acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180 / pi


def get_beta(a, b, c):
    return acos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c)) * 180 / pi


# Pro samotnou kontrolu funkcí z rodiny ‹perimeter_*› si definujeme
# pomocnou proceduru, která pracuje s obecným trojúhelníkem, zadaným
# délkami stran.

def check_triangle(a, b, c):
    alpha = get_alpha(a, b, c)
    beta = get_beta(a, b, c)
    gamma = 180 - alpha - beta

    # Na tomto místě si všimněte, že na číslech s plovoucí
    # desetinnou čárkou (typ ‹float›) «nepoužíváme» běžnou rovnost
    # ‹==›. Problém je, že výpočty tohoto typu mají «omezenou
    # přesnost»: vypočteme-li stejnou hodnotu (v matematickém
    # smyslu) dvěma různými postupy (označme výsledky jako ‹x› a
    # ‹y›), může sice platit ‹x == y›, ale stejně dobře může také
    # nastat ‹x != y›. To, co by mělo platit pokaždé je, že hodnoty
    # ‹x› a ‹y› jsou si „blízko“ – tzn. že, až na chybu způsobenou
    # nepřesností, jsou stejné. Žel, co přesně znamená „blízko“ není
    # přesně definované a záleží od konkrétního výpočtu. Nám bude
    # stačit výchozí definice funkce ‹isclose› z modulu ‹math›,
    # která funguje dobře ve většině situací.

    assert isclose(perimeter_sss(a, b, c), a + b + c)
    assert isclose(perimeter_sas(a, gamma, b), a + b + c)
    assert isclose(perimeter_sas(b, alpha, c), a + b + c)
    assert isclose(perimeter_sas(c, beta, a), a + b + c)
    assert isclose(perimeter_asa(alpha, b, gamma), a + b + c)
    assert isclose(perimeter_asa(beta, a, gamma), a + b + c)
    assert isclose(perimeter_asa(alpha, c, beta), a + b + c)


# Zbývá proceduru ‹check_triangle› zavolat na vhodně zvolené
# trojúhelníky. Strany ‹a› a ‹b› můžeme volit libovolně:

def main():  # demo
    for a in range(1, 6):
        for b in range(1, 6):

            # stranu ‹c› pak ale musíme zvolit tak, aby byla splněna
            # trojúhelníková nerovnost (jinak budou funkce
            # ‹perimeter_*› zcela oprávněně počítat nesmysly):

            for c in range(max(abs(a - b) + 1, 1), a + b):
                check_triangle(a, b, c)

    # Na závěr si ještě demonstrujeme případ, kdy je řešení
    # trojúhelníku skutečně nepřesné, totiž že výsledek, který
    # obdržíme různými způsoby, může být skutečně různý.

    alpha = get_alpha(3, 4, 5)
    beta = get_beta(3, 4, 5)
    assert isclose(perimeter_asa(alpha, 5, beta), 12)
    assert perimeter_asa(alpha, 5, beta) != 12
    assert perimeter_sas(3, 90, 4) == 12


if __name__ == '__main__':
    main()
