# Podobně jako v ‹cellular› budeme v této úloze pracovat
# s 1D buněčným automatem. Místo výpočtu nové konfigurace do
# nového seznamu ale budeme «modifikovat» stávající seznam.
#
# Toto samozřejmě nelze při použití stejných pravidel: v době
# vyhodnocování ‹i›-té buňky by již byla buňka s indexem ‹i -
# 1› přepsaná novou hodnotou. Proto použijeme pravidlo, které se
# dívá jen doprava:
#
# │‹old[i]›│‹old[i + 1]›│‹old[i + 2]›│‹new[i]›│
# ├┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄│┄┄┄┄┄┄┄┄│
# │    1   │      0     │      0     │    0   │
# │    0   │      1     │      0     │    1   │
# │    0   │      1     │      1     │    1   │
# │    1   │      0     │      1     │    0   │
# │    1   │      1     │      1     │    0   │
#
# Na rozdíl od předchozích příkladů, budeme v tomto implementovat
# «proceduru»: ‹cellular_in_situ› nebude hodnotu vracet, místo toho
# bude editovat seznam, který dostala jako parametr (viz též úvod
# k tomuto týdnu).

def cellular_in_situ(state):
    pass


def main():
    state = [1, 0, 0, 1, 1, 0]
    cellular_in_situ(state)
    assert state == [0, 0, 1, 1, 0, 0]
    cellular_in_situ(state)
    assert state == [0, 1, 1, 0, 0, 0]

    state = []
    cellular_in_situ(state)
    assert state == []

    state = [1, 1, 1, 1]
    cellular_in_situ(state)
    assert state == [0, 0, 1, 0]
    cellular_in_situ(state)
    assert state == [0, 1, 0, 0]


if __name__ == "__main__":
    main()
