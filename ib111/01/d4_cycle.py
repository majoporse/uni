# Uvažujme posloupnost definovanou jako ⟦a₁ = 1, aₙ₊₁ = aₙ ⋄ n⟧, kde
# ⟦⋄⟧ se cyklicky vybírá z ⟦+, ⋅, -⟧. Prvních 5 prvků této
# posloupnosti (zařazené v OEIS jako A047908) je:
#
# ⟦ a₁ = 1
#   a₂ = a₁ + 1 = 2
#   a₃ = a₂ ⋅ 2 = 4
#   a₄ = a₃ - 3 = 1
#   a₅ = a₄ + 4 = 5 ⟧
#
# Naším úkolem bude napsat (čistou) funkci, která vyčíslí ‹n›-tý
# prvek této posloupnosti:

def cycle(n):

    # Protože budeme chtít použít cyklus ‹while›, musíme si
    # indexovou proměnnou explicitně zavést:

    i = 1

    # K výpočtu ⟦aᵢ⟧ potřebujeme znát hodnotu ⟦aᵢ₋₁⟧, proto si
    # aktuální hodnotu ⟦aᵢ⟧ uložíme do proměnné ‹a_i› (podobně
    # jako jsme k výpočtu Fibonacciho posloupnosti potřebovali
    # poslední dva prvky). V další iteraci (poté, co se zvýší
    # indexová proměnná ‹i›) budeme mít v ‹a_i› chvíli hodnotu
    # ⟦aᵢ₋₁⟧, kterou využijeme pro výpočet (nové) hodnoty ⟦aᵢ⟧.

    a_i = 1

    # Cyklus ‹while›, jak jistě víte z přednášky, provádí své tělo
    # tak dlouho, dokud platí podmínka cyklu. V tomto případě tedy
    # budeme cyklus opakovat dokud platí ‹i < n›:

    while i < n:

        # Nyní se musíme rozhodnout, který operátor použít pro
        # výpočet další hodnoty ‹a_i›. Protože cyklicky vybíráme ze
        # 3 možností, můžeme se rozhodnout dle zbytku po dělení
        # indexu ‹i› třemi: v první, čtvrté, sedmé atd. iteraci
        # použijeme operátor ‹+›, v druhé, páté, ... operátor ‹*› a
        # konečně ve třetí, šesté, ... operátor ‹-›:

        if i % 3 == 1:
            a_i = a_i + i
        elif i % 3 == 2:
            a_i = a_i * i
        else:  # i % 3 == 0
            a_i = a_i - i

        i += 1

    # V každé iteraci cyklu zvyšujeme indexovou proměnnou ‹i›
    # o jedna, a před cyklem platilo ‹i ≤ n›. Po cyklu musí tedy
    # nutně platit ‹i == n›, a protože zároveň po každé iteraci
    # platí, že ‹a_i› obsahuje hodnotu ⟦aᵢ⟧, musí také platit, že po
    # ukončení cyklu je v proměnné ‹a_i› uložena hodnota ⟦aₙ⟧.

    return a_i


def main():  # demo
    assert cycle(1) == 1
    assert cycle(2) == 2
    assert cycle(3) == 4
    assert cycle(4) == 1
    assert cycle(5) == 5
    assert cycle(6) == 25
    assert cycle(7) == 19
    assert cycle(8) == 26


if __name__ == '__main__':
    main()
