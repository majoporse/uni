from typing import List, Tuple
# V této úloze bude Vaším úkolem implementovat funkce pracující se
# seznamem pacientů ‹patients› u lékaře. Každý pacient má záznam
# (dvojici), který obsahuje jeho unikátní identifikátor a seznam
# návštěv s výsledky. Návštěva je reprezentovaná čtveřicí – rokem,
# kdy pacient navštívil lékaře, a naměřenými hodnotami: pulz,
# systolický a diastolický tlak. Seznam návštěv pacienta je
# uspořádaný vzestupně od nejstarší. Můžete předpokládat, že každý
# pacient má alespoň jeden záznam.

# Vaším prvním úkolem bude implementovat a otypovat funkci
# ‹missing_visits›, která zjistí, kteří pacienti nebyli na prohlídce
# od roku ‹year›. Jako výsledek vraťte seznam identifikátorů
# pacientů.

def missing_visits(year: int, patients: List[Tuple[int, List[Tuple[int, int, int, int]]]]) -> List[int]:
    skippers = []
    for i in range(len(patients)):
        current_year = 0
        for j in range(len(patients[i][1])):
            if patients[i][1][j][0] > year:
                current_year = patients[i][1][j][0]
                break
            else:
                current_year = patients[i][1][j][0]
        if current_year <= year:
            skippers.append(patients[i][0])
    return skippers
            


# Dále napište a otypujte funkci ‹patient_reports›, která vrátí
# seznam zpráv o pacientech. Zpráva o pacientovi je čtveřice, která
# obsahuje záznam o jeho nejvyšším doposud naměřeném pulzu a pro
# každou měřenou hodnotu informaci, zda se měření dané hodnoty
# v jednotlivých letech konzistentně zvyšují (‹True› nebo ‹False›).

# Například zpráva o pacientovi ‹(1, [(2015, 91, 120, 80), (2018,
# 89, 125, 82), (2020, 93, 120, 88)])› je ‹(93, False, False,
# True)›.

def patient_reports(patients: List[Tuple[int, List[Tuple[int, int, int, int]]]]) -> List[Tuple[int, bool, bool, bool]]:
    my_list: List[Tuple[int, bool, bool, bool]] = []
    for i in range(len(patients)):
        person = [True, True, True]
        max_hr = patients[i][1][0][1]
        for j in range(len(patients[i][1]) - 1):
            for k in range(1,4):

                if patients[i][1][j][k] >= patients[i][1][j + 1][k]:
                    person[k-1] = False
                    if k == 1:
                        if max_hr < patients[i][1][j][k]:
                            max_hr = patients[i][1][j][k]

            if max_hr < patients[i][1][-1][1]:
                max_hr = patients[i][1][-1][1]

        my_list.append((max_hr, person[0], person[1], person[2]))
    return my_list

def main() -> None:
    p1 = (0, [(2016, 102, 140, 95)])
    p2 = (1, [(2015, 91, 120, 80), (2018, 89, 125, 82),
              (2020, 93, 120, 88)])
    p3 = (2, [(2010, 73, 110, 70), (2015, 75, 112, 70),
              (2017, 76, 114, 71), (2019, 79, 116, 72)])
    p4 = (3, [(2016, 82, 115, 82), (2017, 83, 117, 80)])
    p5 = (4, [(2005, 81, 130, 90), (2007, 81, 130, 90),
              (2011, 80, 130, 90), (2013, 81, 130, 90),
              (2017, 82, 130, 90)])

    p6 = (5, [(2000, 74, 120, 80), (2011, 107, 142, 95),
              (2012, 94, 140, 97)])
    p7 = (6, [(2019, 101, 145, 95), (2020, 101, 145, 95)])

    patients = [p1, p2, p3, p4, p5]
    assert missing_visits(2017, patients) == [0, 3, 4]
    assert missing_visits(2016, patients) == [0]
    assert missing_visits(2000, patients) == []

    assert patient_reports(patients) == \
        [(102, True, True, True), (93, False, False, True),
         (79, True, True, False), (83, True, True, False),
         (82, False, False, False)]

    assert patient_reports([p6, p7]) == \
        [(107, False, False, True), (101, False, False, False)]


if __name__ == "__main__":
    main()
