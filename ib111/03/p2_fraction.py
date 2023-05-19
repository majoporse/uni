# Stejně jako v ‹02/fraction.py› budete v této úloze pracovat s řetězovým
# zlomkem. Tentokrát implementujeme převod opačným směrem, na vstupu bude
# seznam koeficientů řetězového zlomku, a výstupem bude zlomek klasický.
#
# Naprogramujte tedy čistou funkci ‹continued_fraction›, ktorá dostane jako
# parametr seznam koeficientů a vrátí zlomek ve tvaru ‹(numerator,
# denominator)›.

def continued_fraction(coefficients):
    coefficients.reverse()
    nom = 1
    denom = coefficients[0]
    for i in range(1, len(coefficients)-1):
        denom = coefficients[i]*denom + nom
        nom = (denom - nom)/coefficients[i]
    return denom*coefficients[-1]+nom, denom


def main():
    assert continued_fraction([4, 2, 6, 7]) == (415, 93)
    assert continued_fraction([3, 4, 12, 4]) == (649, 200)
    assert continued_fraction([0, 2, 4]) == (4, 9)


if __name__ == "__main__":
    main()
