# † Vaším úkolem je tentokrát naprogramovat tzv. „hru života“ –
# jednoduchý dvourozměrný celulární automat. Simulace běží na
# čtvercové síti, kde každá buňka je mrtvá (hodnota 0) nebo živá
# (hodnota 1). V každém kroku se přepočte hodnota všech buněk, a to
# podle toho, zda byly v předchozím kroku živé a kolik měly živých
# sousedů (z celkem osmi, tzn. včetně úhlopříčných):
#
# │  stav │ živí sousedé │ výsledek │
# ├───────┼──────────────┼──────────┤
# │  živá │          0–1 │    mrtvá │
# │  živá │          2–3 │     živá │
# │  živá │          4–8 │    mrtvá │
# │┄┄┄┄┄┄┄│┄┄┄┄┄┄┄┄┄┄┄┄┄┄│┄┄┄┄┄┄┄┄┄┄│
# │ mrtvá │          0–2 │    mrtvá │
# │ mrtvá │            3 │     živá │
# │ mrtvá │          4-8 │    mrtvá │

# Příklad krátkého výpočtu:
#
#  ┌───┬───┬───┐   ┌───┬───┬───┐   ┌───┬───┬───┐
#  │   │ ○ │ ○ │   │ ○ │   │ ○ │   │   │ ○ │   │
#  ├───┼───┼───┤   ├───┼───┼───┤   ├───┼───┼───┤
#  │ ○ │ ○ │ ○ │ → │ ○ │   │   │ → │ ○ │   │   │
#  ├───┼───┼───┤   ├───┼───┼───┤   ├───┼───┼───┤
#  │   │ ○ │ ○ │   │ ○ │   │ ○ │   │   │ ○ │   │
#  └───┴───┴───┘   └───┴───┴───┘   └───┴───┴───┘
#
# Napište čistou funkci, která dostane jako parametry počáteční stav
# hry (jako dvourozměrný seznam nul a jedniček) a počet kroků a
# vrátí stav hry po odpovídajícím počtu kroků.

def life(initial, generations):
    pass


def main():
    assert life([[0, 1, 1],
                 [1, 1, 1],
                 [0, 1, 1]], 1) \
        == [[1, 0, 1], [1, 0, 0], [1, 0, 1]]
    assert life([[0, 1, 1],
                 [1, 1, 1],
                 [0, 1, 1]], 2) \
        == [[0, 1, 0], [1, 0, 0], [0, 1, 0]]
    assert life([[0, 1, 1],
                 [1, 1, 1],
                 [0, 1, 1]], 3) \
        == [[0, 0, 0], [1, 1, 0], [0, 0, 0]]
    assert life([[0, 1, 1],
                 [1, 1, 1],
                 [0, 1, 1]], 4) \
        == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    assert life([[0, 1, 1],
                 [1, 1, 1],
                 [0, 1, 1]], 5) \
        == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    assert life([[0, 1, 1],
                 [1, 1, 1],
                 [0, 1, 1]], 0) \
        == [[0, 1, 1], [1, 1, 1], [0, 1, 1]]

    assert life([[1, 1],
                 [1, 1]], 3) \
        == [[1, 1], [1, 1]]
    assert life([[1, 1],
                 [0, 1]], 1) \
        == [[1, 1], [1, 1]]

    assert life([[1, 0, 1, 0],
                 [0, 1, 0, 1],
                 [1, 0, 0, 1],
                 [0, 0, 1, 1]], 5) \
        == [[0, 0, 1, 0],
            [1, 0, 0, 1],
            [1, 1, 0, 1],
            [1, 1, 0, 0]]


if __name__ == "__main__":
    main()
