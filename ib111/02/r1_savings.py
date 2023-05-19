# Vaším úkolem bude spočítat, kolik následujících let Vám vydrží
# úspory o hodnotě ‹savings› v bance. Na konci každého roku Vám
# banka úročí obnos na účtu úrokovou sazbou ‹interest_rate› (zadanou
# v procentech). Dále, abyste pokryli své životní náklady, na
# začátku každého roku vyberete z účtu obnos ‹withdraw›, který se
# každým rokem zvyšuje o inflaci ‹inflation› (opět zadanou
# v procentech). Vybíraný obnos se po započítání inflace
# zaokrouhluje dolů na celá čísla. Úroková sazba a inflace jsou
# konstantní a meziročně se nemění. Po zúročení banka celkovou
# částku zaokrouhluje dolů na celá čísla.

# Příklad: při počátečním obnosu 100000 korun, ročních výdajích
# 42000 korun, úrokové sazbě 3,2 % a inflaci 1,5 % bude po prvním
# roce na účtu ⟦(100000 - 42000)⋅1.032 = 59856⟧. Další rok se výdaje
# zvýší o inflaci na ⟦42000⋅1.015⟧ = 42630.

def savings_years(savings, interest_rate, inflation, withdraw):
    pass


def main():
    assert savings_years(1000, 0, 0, 100) == 10
    assert savings_years(1000, 5, 0, 100) == 13
    assert savings_years(1000, 6, 2, 100) == 12
    assert savings_years(100000, 3.2, 1.5, 42000) == 2
    assert savings_years(500000, 0.5, 3.7, 12000) == 26
    assert savings_years(2000000, 5.2, 2.5, 57000) == 88


if __name__ == "__main__":
    main()
