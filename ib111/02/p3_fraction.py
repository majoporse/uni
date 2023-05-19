# V této úloze bude Vaším úkolem získat hodnotu ‹index›-tého
# koeficientu řetězového zlomku pro racionální číslo s čitatelem
# ‹nom› a jmenovatelem ‹denom›.

# Řetězový zlomek je forma reprezentace čísla jako součet celého
# čísla ⟦a₀⟧ a převrácené hodnoty jiného čísla, které opět
# reprezentujeme součtem celého čísla ⟦a₁⟧ a další převrácené
# hodnoty. Celá čísla ⟦aₙ⟧ postupně tvoří řadu koeficientů
# řetězového zlomku.

# Například řetězový zlomek ⟦4 + (1 / (2 + 1 / (6 + (1/7))))⟧
# reprezentuje číslo ⟦415/93⟧ a jeho koeficienty jsou 4, 2, 6 a 7.

# Koeficienty řetězového zlomku pro číslo ⟦n⟧ můžete získat
# iterativním postupem:
#
#  1. Rozdělte číslo ⟦n⟧ na jeho celočíselnou část ⟦p⟧ a zlomkovou
#     část ⟦q⟧. Číslo ⟦p⟧ přímo udává první koeficient posloupnosti,
#     tzn. ⟦a₀⟧, zbytek koeficientů je odvozen od ⟦q⟧ (viz další krok).
#     Posloupnost má tedy tvar: ⟦p; a₁, a₂, a₃,…⟧.
#
#  2. Pro získání dalšího koeficientu opakujte 1. krok s převrácenou
#     hodnotou zlomkové části ⟦(1/q)⟧.

def continued_fraction(nom, denom, index):
    x=0
    for i in range(index+1):
        number = nom // denom
        nom, denom = denom, nom-number*denom
        if i == index:
            return number


def main():
    assert continued_fraction(2, 1, 0) == 2
    assert continued_fraction(415, 93, 0) == 4
    assert continued_fraction(415, 93, 1) == 2
    assert continued_fraction(415, 93, 2) == 6
    assert continued_fraction(415, 93, 3) == 7
    assert continued_fraction(649, 200, 1) == 4
    assert continued_fraction(649, 200, 2) == 12
    assert continued_fraction(649, 200, 3) == 4
    assert continued_fraction(649, 200, 0) == 3
    assert continued_fraction(649, 200, 1) == 4
    assert continued_fraction(649, 200, 2) == 12
    assert continued_fraction(649, 200, 3) == 4
    assert continued_fraction(9, 4, 1) == 4
    assert continued_fraction(688, 219, 0) == 3
    assert continued_fraction(688, 219, 1) == 7
    assert continued_fraction(688, 219, 2) == 15
    assert continued_fraction(688, 219, 3) == 2


if __name__ == "__main__":
    main()
