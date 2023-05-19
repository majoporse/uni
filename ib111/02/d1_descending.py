# V této ukázce si naprogramujeme jednoduchý algoritmus, který
# pracuje s desítkovým rozvojem celého čísla: konkrétně se budeme
# ptát, zda jsou v desítkovém zápisu daného čísla jednotlivé cifry
# uspořádané sestupně (uvažujeme pořadí od nejvýznamnější, tzn.
# nejlevější, cifry).
#
# Protože chceme pracovat s ciframi, jeví se jako rozumné
# zadefinovat si pomocnou funkci, která nám vrátí konkrétní cifru.
# Desítkový rozvoj přirozeného čísla ⟦n⟧, které má ⟦m⟧ desítkových
# cifer, lze zapsat:
#
# ⟦ n = ∑ᵢ₌₀ᵐ aᵢ⋅10ⁱ ⟧
#
# kde každé pro každé ⟦aᵢ⟧ platí ⟦0 ≤ aᵢ ≤ 9⟧. Za povšimnutí stojí i
# to, že dle zde použité definice má nejméně významná cifra
# („jednotky“) index 0.
#
# Chceme-li nalézt ⟦k⟧-tou cifru, můžeme postupovat následovně:
# nejprve ⟦n⟧ vydělíme číslem ⟦10ᵏ⟧ – pohled na pravou stranu výše
# uvedené rovnosti nám rychle napoví, že členy, u kterých je mocnina
# desítky menší než ⟦k⟧ ze sumy úplně zmizí a člen ⟦aₖ⟧ se stane
# nejnižším (rozmyslete si, jak vypadá člen kde ⟦i = k⟧):
#
# ⟦ n / 10ᵏ = ∑ᵢ₌ₖᵐ⁻ᵏ aᵢ⋅10ⁱ⁻ᵏ ⟧
#
# Zbývá učinit následovné pozorování: protože nás zajímá hodnota
# ⟦aₖ⟧, a protože každé jiné ⟦aᵢ⟧ se v rozvoji ⟦n / 10ᵏ⟧ objevuje
# vynásobeno nějakou kladnou mocninou desítky, můžeme s výhodou
# použít operaci zbytku po dělení (modulo, operátor ‹%›): tímto se
# zbavíme všech ostatních členů (formálněji: zbytek po dělení člena
# ⟦aᵢ⋅10ⁱ⁻ᵏ ⟧ desíti je 0 pro každé ⟦i > k⟧):
#
# ⟦ n / 10ᵏ ≡ aₖ (\mod 10) ⟧
#
# Tímto je vysvětlena na pohled velice jednoduchá funkce
# ‹get_digit›:

def get_digit(number, k):
    return (number // 10 ** k) % 10


# Následující funkce pracuje na stejném principu: každé dělení
# desíti odstraní jednu cifru (jeden člen sumy, která definuje
# desítkový rozvoj). Počet provedených iterací si udržujeme v čítači
# ‹count›.

def count_digits(number):
    count = 0
    while number > 0:
        count += 1
        number = number // 10
    return count


# Funkce ‹get_digit› a ‹count_digits› nám už umožní popsat náš
# původní problém přirozeným způsobem: pro každou dvojici cifer
# ověříme, že jsou ve správném pořadí. Protože cifry jsou při
# procházení zleva očíslovány sestupně, musíme si dát pozor, v jakém
# pořadí ony dvě srovnávané cifry následují.

def is_descending(number):

    # Dvojic cifer je o jednu méně, než cifer samotných: dvojciferné
    # číslo má jednu dvojici cifer, trojciferné dvě, atd., proto
    # musíme od výsledku ‹count_digits› odečíst jedničku.

    for k in range(count_digits(number) - 1):

        # Označme ⟦aᵢ⟧ cifry čísla ‹number›: volání funkce
        # ‹get_digit(number, i)› tedy vrací hodnotu ⟦aᵢ⟧. Cifra
        # s indexem ‹k + 1› je «nalevo» od cifry s indexem ‹k›:
        # mají-li být tedy cifry uspořádány sestupně zleva doprava,
        # musí pro každou dvojici platit ⟦aₖ₊₁ ≥ aₖ⟧. Protože
        # kontrolujeme, že tato podmínka platí pro každou dvojici,
        # jakmile nalezneme nějakou, která ji porušuje (proto
        # v podmínce níže naleznete negaci „chtěné“ vlastnosti),
        # víme, že celkový výsledek je ‹False›, a vykonávání funkce
        # ukončíme příkazem ‹return› (na ostatní dvojice se už není
        # potřeba dívat).

        if get_digit(number, k + 1) < get_digit(number, k):
            return False

    # V cyklu výše jsme zkontrolovali každou dvojici cifer: kdyby
    # některá porušila kýženou vlastnost (cifry jsou uspořádané
    # sestupně), spustil by se příkaz ‹return› a funkce by byla
    # ukončena. Proto, dojdeme-li až sem, víme, že vlastnost platila
    # pro každou dvojici cifer, a tedy platí i pro číslo jako celek.

    return True


# Zbývá pouze ověřit, že jsme v implementaci neudělali chybu.

def main():  # demo
    assert is_descending(7)
    assert is_descending(321)
    assert is_descending(33222111)
    assert is_descending(9999)
    assert is_descending(7741)
    assert not is_descending(123)
    assert not is_descending(332233)
    assert not is_descending(774101)


if __name__ == "__main__":
    main()
