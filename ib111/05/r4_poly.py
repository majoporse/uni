from typing import List
from fractions import Fraction


# † V tomto příkladu se budeme zabývat «polynomy», které
# pravděpodobně znáte ze střední školy. Jestli ne, stačí Vám v tuto
# chvíli vědět, že se jedná o výrazy tvaru
#
#  ⟦  P(x) = aₙxⁿ + … + a₂x² + a₁x + a₀ = ∑₀ⁿ aᵢxⁱ ⟧
#
# Hodnotám ⟦aᵢ⟧ říkáme koeficienty. Koeficienty budeme reprezentovat
# pomocí zlomků (zlomky proto, že je chceme dělit a násobit, aniž
# bychom se dopouštěli nepřesnosti spojené s hodnotami typu
# ‹float›). V Pythonu k tomu můžeme použít typ ‹Fraction›, který je
# součástí standardní knihovny.
#
# Polynom jako celek budeme reprezentovat jako seznam koeficientů:
# na ⟦(n-i)⟧-tém indexu bude uložena hodnota ⟦aᵢ⟧. Z tohoto indexu je
# také zřejmé, k jaké mocnině ⟦x⟧ se koeficient váže (je to ⟦xⁱ⟧).

Polynomial = List[Fraction]


# Vaším úkolem bude implementovat 2 operace: derivaci (angl.
# differentiation) a integraci. Derivací polynomu ⟦P(x) = ∑₀ⁿ aᵢxⁱ⟧
# je polynom ⟦P'(x) = ∑₀ⁿ⁻¹ bᵢxⁱ⟧ kde koeficienty ⟦bᵢ⟧ získáme ze
# vztahu ⟦bᵢ = (i + 1)aᵢ₊₁⟧ (pomyslný nulový koeficient ⟦bₙ⟧ do
# seznamu ukládat nebudeme).

def differentiate(poly: Polynomial) -> Polynomial:
    pass


# Integrace je opačná operace k derivaci: opět uvažujme ⟦P(x) = ∑₀ⁿ
# aₙ₋ᵢxⁱ⟧, pak integrál ⟦∫P(x) = ∑₀ⁿ⁺¹ cᵢxⁱ⟧ bude mít koeficienty
# ⟦c₀ = C⟧, ⟦cᵢ = aᵢ₋₁/i)⟧ kde C je libovolná konstanta. Pro
# jednoduchost budeme uvažovat ⟦C = 0⟧.

def integrate(poly: Polynomial) -> Polynomial:
    pass


# Příklad:
#
#  ⟦ ∫P(x) = 2x⁴ +  x³ +  2x² +  x + C
#    P(x)  =   0 + 8x³ +  3x² + 4x + 1
#    P'(x) =   0 +   0 + 24x² + 6x + 4 ⟧
#
# Totéž se symbolickými koeficienty:
#
#  ⟦ ∫P(x) = c₄x⁴ + c₃x³ + c₂x² + c₁x + c₀
#    P(x)  =    0 + a₃x³ + a₂x² + a₁x + a₀
#    P'(x) =    0 +    0 + b₂x² + b₁x + b₀ ⟧


# Poslední úlohou je ověřit, že operace jsou skutečně vzájemně
# inverzní. Napište funkci, která toto ověří. Protože derivace
# „zapomíná“ hodnotu ⟦a₀⟧ (při výpočtu nových koeficientů se vůbec
# nepoužije), ověřit můžeme pouze jedno pořadí složení obou operací.
# Rozmyslete si které to je. Opačný směr ověřte tak dobře, jak to
# lze.

def check_inverse(poly: Polynomial) -> bool:
    pass


def main() -> None:
    assert differentiate(to_fraction_lst([1])) \
           == to_fraction_lst([0])
    assert differentiate(to_fraction_lst([0])) == \
           to_fraction_lst([0])
    assert differentiate(to_fraction_lst([1, 0])) == \
           to_fraction_lst([1])
    assert differentiate(to_fraction_lst([3, 2, 1])) == \
           to_fraction_lst([6, 2])
    assert differentiate(to_fraction_lst(
        [1, 5, 12, -4, -2, 0, 1])) == \
        to_fraction_lst([6, 25, 48, -12, -4, 0])
    assert differentiate(to_fraction_lst(
        [-4, 0, 0, 2, 0, -1, 0, 0, 0])) == \
        to_fraction_lst([-32, 0, 0, 10, 0, -3, 0, 0])

    assert integrate(to_fraction_lst([1])) == to_fraction_lst([1, 0])
    assert integrate(to_fraction_lst([2, 0])) == \
           to_fraction_lst([1, 0, 0])
    assert integrate(to_fraction_lst([0])) == to_fraction_lst([0])
    assert integrate(to_fraction_lst([5, 4, 3, 2, 1])) == \
           to_fraction_lst([1, 1, 1, 1, 1, 0])
    assert integrate(to_fraction_lst([9, 4, 5])) == \
           to_fraction_lst([3, 2, 5, 0])
    assert integrate(to_fraction_lst([-9, 4, -5])) == \
           to_fraction_lst([-3, 2, -5, 0])

    assert check_inverse(to_fraction_lst([1]))
    assert check_inverse(to_fraction_lst([0]))
    assert check_inverse(to_fraction_lst([1, 0]))
    assert check_inverse(to_fraction_lst([1, 2, 3, 4, 5]))
    assert check_inverse(to_fraction_lst([-12, 4, 8, 2]))
    assert check_inverse(to_fraction_lst([1, -1, 25, -3]))


def to_fraction_lst(int_list: List[int]) -> List[Fraction]:
    res: List[Fraction] = []
    for num in int_list:
        res.append(Fraction(num))
    return res


if __name__ == '__main__':
    main()
