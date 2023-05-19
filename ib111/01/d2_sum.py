# Uvažme posloupnost ⟦aₙ = nⁿ⟧, a posloupnost jejích částečných
# součtů ⟦sₙ = ∑ᵢ₌₁ⁿ aᵢ = ∑ᵢ₌₁ⁿ iⁱ⟧. Ujistěte se, že těmto definicím
# rozumíte: neznáte-li například definici operátoru ∑ (suma), můžete
# se s výhodou obrátit na Wikipedii. Pro jistotu uvádíme několik
# členů obou těchto posloupností:

# ⟦ a₁ = 1¹ = 1
#   a₂ = 2² = 4
#   a₃ = 3³ = 27 ⟧

# ⟦ s₁ = ∑ᵢ₌₁¹ iⁱ = 1¹           = 1          = 1
#   s₂ = ∑ᵢ₌₁² iⁱ = 1¹ + 2²      = 1 + 4      = 5
#   s₃ = ∑ᵢ₌₁³ iⁱ = 1¹ + 2² + 3³ = 1 + 4 + 27 = 32 ⟧

# Naším úkolem bude nyní naprogramovat v Pythonu (čistou) funkci
# ‹nth_element(n)›, která počítá příslušné ⟦aₙ⟧, a (opět čistou)
# funkci ‹partial_sum(n)›, která počítá příslušné ⟦sₙ⟧. První funkce
# je přímočará, stačí nám znát zabudovaný operátor mocnění ‹**› a
# zápis definice funkce:

def nth_element(n):
    return n ** n


# Výpočet ‹partial_sum(n)› bude nicméně o něco složitější: operátor
# suma sčítá řadu čísel, jejichž počet je dán rozdílem mezi jeho
# horním a dolním indexem. Objeví-li se v některém indexu proměnná,
# počet sečtených členů bude typicky záviset na hodnotě této
# proměnné.

# Jak již jistě víte z přednášky, v situaci, kdy potřebujeme
# opakovaně provádět příkazy (a zejména není-li počet opakování
# konstanta) použijeme «cyklus». Nejjednodušší formou cyklu je
# příkaz „opakuj ‹n›-krát“, který v Pythonu zapisujeme ‹for i in
# range(n)›.

# Krom hodnoty ‹n› je zde důležitá ještě proměnná ‹i›: obecně se
# jedná o tzv. «proměnnou cyklu». Tato proměnná má k tělu cyklu
# podobný vztah, jako má parametr funkce k tělu funkce: před každým
# provedením těla (tzv. «iterací») se do ‹i› přiřadí nová hodnota
# (jaká přesně hodnota to bude záleží na konkrétní formě cyklu).

# V tomto případě – cyklus tvaru ‹for i in range(n)› – se do ‹i›
# přiřadí «pořadové číslo iterace», a samotnou proměnnou ‹i› pak
# nazýváme «indexovou proměnnou». Ve většině programovacích jazyků
# (a Python není výjimkou) se «indexuje od 0», tzn. v první iteraci
# je ‹i = 0›, ve druhé ‹i = 1›, atd., konečně v poslední iteraci je
# ‹i = n - 1›. Nyní můžeme konečně přistoupit k definici funkce
# ‹partial_sum(n)›:

def partial_sum(n):

    # Jako první krok si zavedeme proměnnou, do které budeme
    # postupně přičítat jednotlivé hodnoty ⟦aᵢ⟧ – takové proměnné
    # říkáme «střadač» nebo «akumulátor» (angl. accumulator).

    result = 0

    # Následuje samotný cyklus, který v každé iteraci do akumulátoru
    # ‹result› přičte příslušnou hodnotu ⟦aᵢ⟧. Protože indexová
    # proměnná ‹i› je číslována od 0, ale hodnoty ⟦aᵢ⟧ jsou
    # číslovány od 1, vypočteme hodnotu ⟦aᵢ⟧ jako ‹nth_element(i +
    # 1)›:

    for i in range(n):
        result += nth_element(i + 1)

    # Po skončení cyklu je v akumulátoru požadovaná suma ⟦sₙ = ∑
    # ᵢ₌₁ⁿ aᵢ⟧. Pro každé ‹i› v rozmezí ‹0› až ‹n - 1› (včetně) bylo
    # provedeno tělo cyklu, a v ‹result› je tedy uložen součet
    # ‹nth_element(0 + 1) + nth_element(1 + 1) + ... + nth_element(n
    # - 1 + 1)›, neboli ‹nth_element(1) + nth_element(2) + ... +
    # nth_element(n)›.

    return result


def main():  # demo
    assert partial_sum(1) == 1
    assert partial_sum(2) == 5
    assert partial_sum(3) == 32
    assert partial_sum(4) == 288
    assert partial_sum(7) == 873612
    assert partial_sum(15) == 449317984130199828


if __name__ == "__main__":
    main()
