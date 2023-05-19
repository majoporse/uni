# V této ukázce se budeme zabývat jednoduchými objekty, které můžeme
# chápat jako rozšíření složených typů o «metody». Metoda je
# podprogram, který je svázán se svým složeným typem (objektem):
# metoda má vždy parametr, který reprezentuje instanci objektu se
# kterou bude pracovat. V Pythonu tento parametr explicitně uvádíme
# v hlavičce metody (tzn. v seznamu formálních parametrů), a to vždy
# jako první a vždy se jménem ‹self›.

# Při «volání» metod používáme tečkovou notaci, stejně jako
# u zabudovaných typů: máme-li hodnotu ‹items› typu ‹list›, můžeme
# napsat třeba ‹items.append(1)› a víme, že toto volání provede
# nějakou akci nad hodnotou ‹items›. Naše metody se budou chovat
# stejně (ve skutečnosti je totiž ‹append› metoda třídy ‹list›).

# Máme-li hodnotu ‹hospital› typu ‹Hospital› (u objektů také mluvíme
# o instanci ‹hospital› třídy ‹Hospital›), můžeme napsat třeba
# ‹hospital.add_doctor('dept', doc)›. Metodě definované jako
# ‹add_doctor(self, department, doctor)› bude hodnota ‹hospital›
# předána právě parametrem ‹self›, hodnoty uvedené při volání
# v závorkách pak v dalších parametrech.  Přesněji:
#
# • metoda ‹add_doctor› má 3 formální parametry,
# • uvažujeme volání ‹hospital.add_doctor('dept', doc)›.
#
# Parametry se předají takto:
#
# • hodnota ‹hospital› bude předána prvním parametrem (‹self›),
# • druhý parametr, ‹department›, bude mít hodnotu ‹'dept'›,
# • třetí parametr, ‹doctor›, bude mít hodnotu ‹doc›.

from typing import List, Dict


# Třída ‹Doctor› je obyčejný složený typ bez metod, jaké známe
# z předchozí ukázky. Bude mít atributy ‹name› (jméno lékaře) a
# ‹night_shift› (lze-li tomuto lékaři plánovat noční směny).

class Doctor:
    def __init__(self, name: str, night_shift: bool):
        self.name = name
        self.night_shift = night_shift


# Třída ‹Hospital› reprezentuje samotnou nemocnici. Nemocnice má
# lékaře a oddělení, na kterých jednotliví lékaři pracují. Data
# budeme ukládat do slovníku, ve kterém jako klíče použijeme názvy
# jednotlivých oddělení a hodnoty budou seznamy lékařů.

class Hospital:

    # Metoda ‹__init__› inicializuje novou nemocnici. Krom objektu,
    # který bude inicializovat (parametr ‹self›) jí předáme seznam
    # názvů oddělení (parametr ‹departments›). Metoda inicializuje
    # atribut ‹departments›.

    def __init__(self, departments: List[str]):
        self.departments: Dict[str, List[Doctor]] = {}
        for name in departments:
            self.departments[name] = []

    # Metoda ‹add_doctor› zařadí lékaře ‹doctor› na oddělení
    # ‹department›. Vstupní podmínkou je, že toto oddělení
    # v nemocnici existuje.

    def add_doctor(self, department: str, doctor: Doctor) -> None:
        self.departments[department].append(doctor)

    # Protože krom zvláštního zápisu volání je metoda podprogram
    # jako každý jiný, lze metody stejně tak klasifikovat na čisté
    # funkce, predikáty a podobně. Není ale obvyklé mluvit v tomto
    # kontextu o procedurách: metody velmi často mění předaný objekt
    # (parametr ‹self›) – na rozdíl od funkcí budeme tedy
    # předpokládat, není-li uvedeno jinak, že metoda mění objekt
    # ‹self›.

    # Budeme nicméně nadále explicitně uvádět, má-li mít metoda
    # nějaké «jiné» vedlejší efekty. Není-li tedy uvedeno jinak,
    # metoda může měnit «pouze» objekt předaný parametrem ‹self›.
    # Metoda, která je označená jako «čistá» (a tedy i metoda, která
    # je označená jako «predikát») «nemění» ani tento.

    # Metoda (predikát) ‹night_coverage› zkontroluje, že je na
    # každém oddělení aspoň jeden lékař, který může být zařazen na
    # noční směnu.

    def night_coverage(self) -> bool:
        for department, doctor_list in self.departments.items():
            found = False
            for doctor in doctor_list:
                if doctor.night_shift:
                    found = True

            if not found:
                return False
        return True


def main() -> None:
    house = Doctor('House', False)
    chase = Doctor('Chase', True)
    wilson = Doctor('Wilson', True)

    assert house.name == 'House'
    assert not house.night_shift
    assert chase.night_shift

    hospital = Hospital(["oncology", "diagnostics"])
    assert hospital.departments == {"oncology": [], "diagnostics": []}
    assert not hospital.night_coverage()

    hospital.add_doctor("oncology", wilson)
    assert hospital.departments == {"oncology": [wilson], "diagnostics": []}
    assert not hospital.night_coverage()

    hospital.add_doctor("diagnostics", house)
    assert hospital.departments == \
        {"oncology": [wilson], "diagnostics": [house]}
    assert not hospital.night_coverage()

    hospital.add_doctor("diagnostics", chase)
    assert hospital.departments == \
        {"oncology": [wilson], "diagnostics": [house, chase]}
    assert hospital.night_coverage()


if __name__ == "__main__":
    main()
