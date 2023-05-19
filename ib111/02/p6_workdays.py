# Napište funkci, která zjistí, kolik bude pracovních dnů v roce
# ‹year›, přičemž parametr ‹day_of_week› udává, na který den v týdnu
# v tomto roce padne první leden. Dny v týdnu mají hodnoty 0–6
# počínaje pondělím s hodnotou 0.

# České státní svátky jsou:
#
# │  datum │ svátek                                         │
# ├┄┄┄┄┄┄┄▻┼◅┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄│
# │   1.1. │ Den obnovy samostatného českého státu          │
# │      — │ Velký pátek                                    │
# │      — │ Velikonoční pondělí                            │
# │   1.5. │ Svátek práce                                   │
# │   8.5. │ Den vítězství                                  │
# │   5.7. │ Den slovanských věrozvěstů Cyrila a Metoděje   │
# │   6.7. │ Den upálení mistra Jana Husa                   │
# │  28.9. │ Den české státnosti                            │
# │ 28.10. │ Den vzniku samostatného československého státu │
# │ 17.11. │ Den boje za svobodu a demokracii               │
# │ 24.12. │ Štědrý den                                     │
# │ 25.12. │ 1. svátek vánoční                              │
# │ 26.12. │ 2. svátek vánoční                              │


def workdays(year, day_of_week):
    pass


def main():
    assert workdays(2020, 2) == 251
    assert workdays(2021, 4) == 252
    assert workdays(2016, 4) == 252
    assert workdays(2004, 3) == 253
    assert workdays(1993, 4) == 252
    assert workdays(1991, 1) == 251
    assert workdays(1990, 0) == 250
    assert workdays(1900, 0) == 250
    assert workdays(2000, 5) == 250


if __name__ == "__main__":
    main()
