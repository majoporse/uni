# Tato ukázka demonstruje velice jednoduchý program pro tvorbu
# dvourozměrného (obdélníkového) seznamu. Čistá funkce ‹power_table›
# vytvoří tabulku přirozených (kladných) mocnin nezáporných čísel,
# kde vždy v jednom řádku bude tatáž mocnina různých čísel, a
# v daném sloupci budou různé mocniny stejného čísla.

# Tabulka by měla vypadat zhruba takto (tabulka je zobrazena tak, že
# vnitřní seznamy jsou řádky – v prvním sloupci jsou indexy vnějšího
# a v záhlaví indexy vnitřního seznamu).
#
# │ index │ 0 │ 1 │  2 │  3 │   4 │   5 │
# ├◅─────▻│──▻┼──▻┼───▻┼───▻┼────▻┼────▻│
# │   0   │ 1 │ 1 │  1 │  1 │   1 │   1 │
# │   1   │ 1 │ 2 │  3 │  4 │   5 │   6 │
# │   2   │ 1 │ 4 │  9 │ 16 │  25 │  36 │
# │   3   │ 1 │ 8 │ 27 │ 64 │ 125 │ 216 │

def power_table(max_pow, max_num):

    # Pro zjednodušení cyklu, který bude tabulku vyplňovat, si dopředu
    # vytvoříme obdélníkový seznam a vyplníme jej nulami. Tzv. «intensionální»
    # zápis seznamů znáte z přednášky: na prvním místě je popis hodnoty,
    # která bude do seznamu vložena, poté následuje specifikace opakování,
    # která používá syntaxi odvozenou od ‹for› cyklu. Celý vnitřní seznam je
    # pro ten vnější onou specifikací hodnoty.

    result = [[0 for i in range(max_num)] for j in range(max_pow + 1)]

    # Nyní stačí tabulku vyplnit jednoduchým vnořeným for cyklem. Nesmíme
    # zapomenout na posuv mezi přirozenými čísly (první je 1) a indexy (první
    # je 0).

    for row in range(max_pow + 1):
        for col in range(max_num):
            result[row][col] = (col + 1) ** row
    return result


# Není-li výpočet jednotlivé buňky příliš složitý, můžeme celý seznam zapsat
# intensionálně přímo:

def power_table_alt(max_pow, max_num):
    return [[(col + 1) ** row
            for col in range(max_num)]
            for row in range(max_pow + 1)]


# Následují pomocné funkce pro testování a samotné testy.

def check_size(tab, rows, cols):
    assert len(tab) == rows
    for row in tab:
        assert len(row) == cols


def check_power_table(tabulate):
    check_size(tabulate(1, 1), 2, 1)
    check_size(tabulate(3, 2), 4, 2)
    assert tabulate(1, 1)[0][0] == 1
    assert tabulate(1, 1)[1][0] == 1
    assert tabulate(3, 3)[3][2] == 27
    assert tabulate(4, 3)[4][2] == 81


def main():
    check_power_table(power_table)
    check_power_table(power_table_alt)


if __name__ == '__main__':
    main()
