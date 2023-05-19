from typing import List, Dict


# Třída ‹Warrior› reprezentuje válečníka, který má jméno a sílu.
# Tyto jeho vlastnosti bude třída reprezentovat atributy ‹name› a
# ‹strength›. Tato třída má jedinou metodu, a to ‹__init__›.

class Warrior:
    def __init__(self, name: str, strength: int):
        self.name = name
        self.strength = strength


# Velké množství válečníků tvoří hordu, kterou reprezentujeme třídou
# ‹Horde›. Horda má interní strukturu – je rozdělena do
# pojmenovaných klanů, které reprezentujeme slovníkem (jméno klanu,
# seznam válečníků).

class Horde:

    # Vytvoří hordu se zadanými klany.

    def __init__(self, clans: Dict[str, List[Warrior]]):
        self.horde = clans

    # Metoda vrátí aktuální stav hordy, t.j. slovník všech klanů.

    def clans(self) -> Dict[str, List[Warrior]]:
        return self.horde

    # Metoda přidá válečníka do klanu. Neexistuje-li klan daného
    # jména, metoda jej vytvoří.

    def add_warrior(self, clan: str, warrior: Warrior) -> None:
        if self.horde.get(clan) is None:
            self.horde[clan] = [warrior]
        else:
            self.horde[clan] = self.horde.get(clan) + [warrior]

    # Metoda (a zároveň predikát) zkontroluje, má-li každý klan
    # dostatečný počet válečníků.

    def validate_clan_strength(self, required: int) -> bool:
        for clan in self.clans():
            if self.horde.get(clan) == []:
                return False
            for warrior in self.horde.get(clan):
                if warrior.strength < required:
                    return False
        return True


def main() -> None:
    noname = Warrior('Noname', 12)
    assert noname.name == 'Noname'
    assert noname.strength == 12

    achilleus = Warrior('Achilleus', 1000)
    patrokles = Warrior('Patrokles', 700)

    horde = Horde({"peasants": [noname]})
    assert horde.clans() == {"peasants": [noname]}
    assert horde.validate_clan_strength(10)
    assert not horde.validate_clan_strength(13)

    horde.add_warrior("heroes", achilleus)
    horde.add_warrior("heroes", patrokles)
    assert horde.clans() == {"peasants": [noname],
                             "heroes": [achilleus, patrokles]}
    assert not horde.validate_clan_strength(50)

    empty_horde = Horde({})
    assert empty_horde.validate_clan_strength(100)
    assert empty_horde.validate_clan_strength(1)

    empty_horde = Horde({"empty_clan": []})
    assert not empty_horde.validate_clan_strength(100)
    assert not empty_horde.validate_clan_strength(1)


if __name__ == "__main__":
    main()
