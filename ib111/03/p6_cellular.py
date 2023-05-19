# Napište (čistou) funkci, která simuluje jeden krok výpočtu
# jednorozměrného buněčného automatu (cellular automaton). My se
# omezíme na «binární» (buňky nabývají hodnot 0 a 1) «jednorozměrný»
# automat s «konečným stavem»: stav takového automatu je seznam
# jedniček a nul, například:
#
#   ┌───┬───┬───┬───┬───┬───┬───┐
#   │ 0 │ 1 │ 1 │ 1 │ 0 │ 0 │ 1 │
#   └───┴───┴───┴───┴───┴───┴───┘
#
# Protože obecný automat tohoto typu je stále relativně složitý,
# budeme implementovat automat s fixní sadou pravidel:
#
# │‹old[i - 1]›│‹old[i]›│‹old[i + 1]›│‹new[i]›│
# ├┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄│┄┄┄┄┄┄┄┄│
# │     0      │    0   │      1     │    1   │
# │     1      │    0   │      0     │    1   │
# │     1      │    0   │      1     │    1   │
# │     1      │    1   │      0     │    0   │
# │     1      │    1   │      1     │    0   │
#
# Pravidla určují, jakou hodnotu bude mít buňka v následujícím
# stavu, v závislosti na několika okolních buňkách stavu nynějšího
# (konkrétní indexy viz tabulka). Neexistuje-li pro danou vstupní
# kombinaci pravidlo, do nového stavu přepíšeme stávající hodnotu
# buňky. Na krajích stavu interpretujeme chybějící políčko vždy
# jako nulu.
#
# Výpočet s touto sadou pravidel tedy funguje takto:
#
#   ┌───┬───┬───┬───┬───┬───┐ 001 → 1 ┌───┬───┬───┬───┬───┬───┐
#   │░0░│░1░│ 1 │ 0 │ 0 │ 1 │────────▶│░1 │   │   │   │   │   │
#   └───┴───┴───┴───┴───┴───┘         └───┴───┴───┴───┴───┴───┘
#   ┌───┬───┬───┬───┬───┬───┐ 011 → ? ┌───┬───┬───┬───┬───┬───┐
#   │░0░│░1░│░1░│ 0 │ 0 │ 1 │────────▶│ 1 │░1 │   │   │   │   │
#   └───┴───┴───┴───┴───┴───┘         └───┴───┴───┴───┴───┴───┘
#   ┌───┬───┬───┬───┬───┬───┐ 110 → 0 ┌───┬───┬───┬───┬───┬───┐
#   │ 0 │░1░│░1░│░0░│ 0 │ 1 │────────▶│ 1 │ 1 │░0░│   │   │   │
#   └───┴───┴───┴───┴───┴───┘         └───┴───┴───┴───┴───┴───┘
#   ┌───┬───┬───┬───┬───┬───┐ 100 → 1 ┌───┬───┬───┬───┬───┬───┐
#   │ 0 │ 1 │░1░│░0░│░0░│ 1 │────────▶│ 1 │ 1 │ 0 │░1░│   │   │
#   └───┴───┴───┴───┴───┴───┘         └───┴───┴───┴───┴───┴───┘
#   ┌───┬───┬───┬───┬───┬───┐ 001 → 1 ┌───┬───┬───┬───┬───┬───┐
#   │ 0 │ 1 │ 1 │░0░│░0░│░1░│────────▶│ 1 │ 1 │ 0 │ 1 │░1░│   │
#   └───┴───┴───┴───┴───┴───┘         └───┴───┴───┴───┴───┴───┘
#   ┌───┬───┬───┬───┬───┬───┐ 010 → ? ┌───┬───┬───┬───┬───┬───┐
#   │ 0 │ 1 │ 1 │ 0 │░0░│░1░│────────▶│ 1 │ 1 │ 0 │ 1 │ 1 │░1░│
#   └───┴───┴───┴───┴───┴───┘         └───┴───┴───┴───┴───┴───┘
#
# Na vstupu dostanete stav (konfiguraci) ‹state›, výstupem funkce je
# nový seznam, který obsahuje stav vzniklý aplikací výše uvedených
# pravidel na ‹state›.

def cellular_step(state):
    pass


def main():
    assert cellular_step([0, 1, 0]) == [1, 1, 1]
    assert cellular_step([0, 0, 1]) == [0, 1, 1]
    assert cellular_step([1, 0, 1]) == [1, 1, 1]
    assert cellular_step([1, 1, 1]) == [1, 0, 0]
    assert cellular_step([1, 0, 1, 1, 0, 1, 1]) == [1, 1, 1, 0, 1, 1, 0]
    assert cellular_step([1, 1, 1, 0, 1]) == [1, 0, 0, 1, 1]
    assert cellular_step([0, 0, 1, 1, 1, 0, 1]) == [0, 1, 1, 0, 0, 1, 1]


if __name__ == "__main__":
    main()
