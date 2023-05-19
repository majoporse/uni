# Napište (čistou) funkci ‹sequence›, která spočítá hodnotu člena
# ⟦aₙ⟧ níže popsané posloupnosti, kde ‹n› je první parametr této funkce.

# První člen posloupnosti, ⟦a₀⟧, je zadán parametrem ‹initial›,
# každý další člen je pak určen sumou ⟦aⱼ = ∑ᵢ₌₁ᵏ (-1)ⁱ · i · aⱼ₋₁⟧,
# kde ‹k› je druhým parametrem funkce ‹sequence›.  Například pro
# parametry ‹k = 3› a ‹initial = 2› jsou první 3 členy posloupnosti:

# ⟦ a₀ = 2
#   a₁ = ∑ᵢ₌₁³ (-1)ⁱ · i · a₀ = -a₀ + 2a₀ - 3a₀ = -2 + 4 - 6 = -4
#   a₂ = ∑ᵢ₌₁³ (-1)ⁱ · i · a₁ = -a₁ + 2a₁ - 3a₁ = 4 - 8 + 12 = 8 ⟧

# Očekávaný výsledek pro volání ‹sequence(2, 3, 2)› je tedy ‹8›.

def sequence(n, k, initial):
    sum1 = 0
    sum2 = initial
    for i in range(n):
        for j in range(k):
            sum1 += (1**k)*((-1)**(j+1))*(j+1)*sum2
        sum2 = sum1
        sum1 = 0
    return sum2


def main():
    assert sequence(2, 3, 2) == 8
    assert sequence(0, 1, 7) == 7
    assert sequence(1, 1, 7) == -7
    assert sequence(1, 2, 7) == 7
    assert sequence(1, 3, 7) == -14
    assert sequence(3, 1, 1) == -1
    assert sequence(2, 2, 2) == 2
    assert sequence(5, 5, 2) == -486
    assert sequence(3, 10, 1) == 125
    assert sequence(4, 10, 1) == 625
    assert sequence(4, 4, 4) == 64


if __name__ == "__main__":
    main()
