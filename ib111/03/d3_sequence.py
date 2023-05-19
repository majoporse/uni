# V předchozích dvou ukázkách byl seznam vstupem nebo výstupem
# funkce. Nyní se podíváme na funkci, která má na vstupu i výstupu
# pouze jediné číslo, ale seznam využije pro svůj výpočet. Vrátíme
# se k výpočtu n-tého prvku posloupnosti, podobně jak tomu bylo
# v příkladech z první části. Vyčíslovat budeme posloupnost, se
# kterou jsme se setkali v úvodu:
#
# ⟦ a₁ = 1
#   aₙ = ∑ₖ₌₁ⁿ⁻¹ d(k,n)⋅aₖ ⟧
#
# kde ⟦d(k,n) = k⟧ když ⟦k⟧ dělí ⟦n⟧ a 0 jinak. Implementace bude
# formou čisté funkce.

def sequence(position):

    # Podobně jako při výpočtu ‹fib› v předchozí ukázce si vytvoříme
    # proměnnou, ve které budeme mít uložen dosud vypočtený prefix
    # posloupnosti. V tomto případě to ale není proto, abychom jej
    # mohli použít jako návratovou hodnotu, ale čistě pro naše
    # interní účely.

    seq = [1]

    # Do seznamu ‹seq› budeme v cyklu přidávat nové prvky
    # posloupnosti, v každé iteraci jeden. Potřebujeme provést ‹n -
    # 1› iterací (jeden prvek už v seznamu máme). Nabízí se dvě
    # možnosti: ‹for› cyklus, podobně jako v předchozím, nebo
    # ‹while› cyklus. Protože potřebujeme indexovat od 1, není ‹for›
    # cyklus příliš pohodlný, navíc u ‹while› cyklu je na pohled
    # zřejmé, že má správný počet iterací, přikloníme se k této
    # variantě:

    while len(seq) < position:

        # Do proměnné ‹n› si uložíme index právě počítaného prvku
        # (číslováno od 1).

        n = len(seq) + 1

        # Nyní potřebujeme vypočítat hodnotu, kterou přidáme na
        # konec seznamu. Nachystáme si střadač ‹total›, ve kterém
        # budeme počítat definiční sumu, a indexovou proměnnou ‹k›
        # (která bude indexovat už vypočtené hodnoty počínaje první
        # s indexem 1).

        total = 0
        k = 1

        # Samotný výpočet sumy provedeme opět v cyklu.

        while k < n:
            if n % k == 0:
                total += k * seq[k - 1]
            k += 1

        # V proměnné ‹total› máme nyní další prvek posloupnosti, který
        # si přidáme do seznamu ‹seq› a pokračujeme další iterací.

        seq.append(total)

    # Seznam ‹seq› byl čistě pomocný – umožnil nám provést výpočet.
    # Výsledkem funkce je ale jediné číslo, totiž ‹position›-tý
    # prvek posloupnosti. Ten nalezneme na indexu ‹position - 1›
    # (seznamy indexujeme od nuly, první prvek je tedy na indexu 0,
    # atd.).

    return seq[position - 1]


# Hodnoty pro testy pochází z databáze OEIS.

def main():  # demo
    from_oeis = [1, 1, 1, 3, 1, 6, 1, 15, 4, 8, 1, 54, 1, 10, 9,
                 135, 1, 78, 1, 100, 11, 14, 1, 822, 6, 16, 40]
    for i in range(len(from_oeis)):
        assert sequence(i + 1) == from_oeis[i]


if __name__ == '__main__':
    main()
