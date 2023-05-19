# Napište čistou funkci ‹least_squares›, která dostane na vstupu dva
# stejně dlouhé seznamy čísel. Hodnoty na odpovídajících pozicích
# v těchto seznamech udávají souřadnice jednoho vstupního bodu.
#
# Výsledkem funkce nechť je trojice ⟦(α, β, r)⟧ kde ⟦y = α + βx⟧
# udává přímku, která nejlépe aproximuje zadané body, a ⟦r⟧ je seznam
# tzv. residuí (vertikálních vzdáleností jednotlivých bodů od
# vypočtené přímky). Označíme-li souřadnice jednotlivých bodů ⟦(xᵢ,
# yᵢ)⟧ a ⟦x̄⟧, ⟦ȳ⟧ aritmetické průměry příslušných seznamů,
# hledané koeficienty získáte použitím těchto vzorců:

# ⟦ βₛ = ∑ ( xᵢ - x̄ )( yᵢ - ȳ )
#   βₓ = ∑ ( xᵢ - x̄ )²
#   β  = βₛ / βₓ
#   α  = ȳ - βx̄ ⟧

# V případě, že body leží na vertikální přímce (a tedy ⟦β⟧ není
# definovaná), vraťte místo trojice hodnotu ‹None›.

def least_squares(x, y):
    pass


def main():
    assert check([1, 2], [3, 4], (2, 1, [0, 0]))
    assert check([1, 2, 3], [3, 4, 5], (2, 1, [0, 0, 0]))
    assert least_squares([1, 1, 1], [3, 4, 5]) is None
    assert check([1, 2, 3], [2, 2, 2], (2, 0, [0, 0, 0]))
    assert check([1, 2, 3], [1, 4, 1], (2, 0, [1, 2, 1]))
    assert check([1, 2, 3], [1, 2, 4],
                 (-2 / 3, 3 / 2, [1 / 6, 1 / 3, 1 / 6]))


def check(x, y, expect):
    from math import isclose
    (alpha1, beta1, r1) = least_squares(x, y)
    (alpha2, beta2, r2) = expect
    if not isclose(alpha1, alpha2) or not isclose(beta1, beta2):
        return False
    for a, b in zip(r1, r2):
        if not isclose(a, b):
            return False
    return True


if __name__ == "__main__":
    main()
