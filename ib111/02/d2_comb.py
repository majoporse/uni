from math import factorial


# V této ukázce se zaměříme na ekvivalenci ‹for› a ‹while› cyklů.
# Podíváme se přitom na «kombinační čísla», definovaná jako:
#
# ⟦ (n¦k) = n! / (k! ⋅ (n - k)!) ⟧
#
# kde ⟦k ≤ n⟧. Samozřejmě, mohli bychom počítat kombinační čísla
# přímo z definice, navíc v modulu ‹math› je již k dispozici funkce
# ‹factorial›, takže bychom se v zápisu obešli úplně bez cyklů.
# Nicméně jednoduché pozorování nám (resp. programu, který bude
# výpočet provádět) může ušetřit významné množství práce.  Jak jistě
# víte, faktoriál je definován takto:
#
# ⟦ n! = ∏ᵢ₌₁ⁿi ⟧
#
# A tedy:
#
# ⟦ n! / k! = ∏ᵢ₌₁ⁿ i / ∏ᵢ₌₁ᵏ i = ∏ᵢ₌ₖ₊₁ⁿ i ⟧
#
# Navíc, abychom měli zaručeno, že skutečně práci ušetříme, můžeme
# tento trik aplikovat na větší z ⟦k⟧ nebo ⟦n - k⟧.

def comb_for(n, k):

    # Nejprve zjistíme, které z ⟦k⟧ resp. ⟦n - k⟧ je menší: vzhledem
    # k symetrii definice vůči těmto dvěma hodnotám můžeme případně
    # ⟦k⟧ nahradit hodnotou ⟦n - k⟧, aniž bychom změnili výsledek:
    # platí ⟦(n¦k) = (n¦n-k)⟧.

    if k < n - k:
        k = n - k

    # Dále chceme vynásobit všechna čísla mezi ⟦k⟧ a ⟦n⟧ (nicméně
    # ⟦k⟧ samotné chceme přeskočit, zatímco ⟦n⟧ chceme zahrnout):

    numerator = 1

    for i in range(k + 1, n + 1):
        numerator *= i

    return numerator / factorial(n - k)


# Nyní ekvivalentní definice pomocí cyklu ‹while›:

def comb_while(n, k):

    if k < n - k:
        k = n - k

    numerator = 1
    i = k + 1

    while i <= n:
        numerator *= i
        i += 1

    return numerator / factorial(n - k)


# Kontrolu správnosti tentokrát provedeme trochu jinak: nebudeme
# kontrolovat předem vypočtené hodnoty, které bychom napsali do
# programu jako konstanty, jak jsme to většinou dělali doteď. Místo
# toho ověříme, že naše implementace dává stejný výsledek, jako
# výpočet přímo z definice. Díky tomu můžeme kontrolovat výrazně
# více případů, aniž bychom se takříkajíc upsali k smrti.

def main():  # demo
    for n in range(1, 50):
        for k in range(1, n):
            naive = factorial(n) / (factorial(k) * factorial(n - k))
            assert comb_for(n, k) == naive
            assert comb_while(n, k) == naive


if __name__ == '__main__':
    main()
