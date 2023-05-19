from typing import Tuple, List, Optional

# V této úloze bude Vaším úkolem implementovat a otypovat
# následující funkce, které implementují dotazy na školní kurzy.
# Kurz je reprezentován seznamem dvojic (student, známka), přičemž
# student je trojice (učo, jméno, semestr) a známka je řetězec
# z rozsahu ‹A› až ‹F›.


# Funkce ‹failed› vrátí seznam studentů kurzu ‹course›, kteří z něj
# mají známku ‹F›.
triple = Tuple[int, str, int]
typecourse = List[Tuple[triple, str]]


def failed(course: typecourse) -> List[triple]:
    bad_students = []
    for i in range(len(course)):
        if course[i][-1] == "F":
            bad_students.append(course[i][0])
    return bad_students


# Funkce ‹count_passed› vrátí počet studentů, kteří úspěšně ukončili
# kurz ‹course›, tedy z něj nemají známku ‹F›. Parametr ‹semester›
# je volitelný: je-li specifikován (není ‹None›), funkce vrátí počet
# úspěšných studentů v daném semestru, jinak vrátí počet všech
# úspěšných studentů.


def count_passed(course: typecourse, semester: Optional[int]) -> int:
    good_students = []

    for i in range(len(course)):
        if course[i][-1] != "F":
            good_students.append(course[i][0])

    sem_list: List[triple] = []

    if semester is not None:
        for i in range(len(good_students)):
            if semester == good_students[i][-1]:
                sem_list.append(good_students[i])
    else:
        sem_list = good_students

    return len(sem_list)

# Funkce ‹student_grade› vrátí známku studenta s učem ‹uco›. Pokud
# takový student v kurzu ‹course› není, vrací ‹None›.


def student_grade(uco: int, course: typecourse) -> Optional[str]:
    for i in range(len(course)):
        if course[i][0][0] == uco:
            return course[i][1]
    return None


def main() -> None:
    s1 = (311799, "Dennis Ritchie", 1)
    s2 = (121436, "George Boole", 3)
    s3 = (463522, "Ada Lovelace", 3)
    s4 = (336100, "Alonzo Church", 2)
    s5 = (378500, "Noam Chomsky", 1)
    s6 = (473521, "Donald Knuth", 1)

    ib111 = [(s1, "F"), (s2, "A"), (s4, "E"), (s6, "F")]
    ib001 = [(s2, "D"), (s4, "C"), (s3, "F"), (s5, "D"), (s6, "B")]
    ib002 = [(s6, "A"), (s1, "B"), (s3, "A"), (s4, "C"), (s5, "A")]

    failed_ib111 = failed(ib111)
    failed_ib001 = failed(ib001)

    # Test failed
    assert s1 in failed_ib111 and s6 in failed_ib111 and len(failed_ib111) == 2
    assert s3 in failed_ib001 and len(failed_ib001) == 1
    assert failed(ib002) == []

    # Test count_passed
    assert count_passed(ib111, None) == 2
    assert count_passed(ib001, None) == 4
    assert count_passed(ib002, None) == 5
    assert count_passed(ib002, 1) == 3
    assert count_passed(ib001, 3) == 1
    assert count_passed(ib111, 3) == 1

    # Test student_grade
    assert student_grade(311799, ib111) == "F"
    assert student_grade(311799, ib001) is None
    assert student_grade(311799, ib002) == "B"
    assert student_grade(463522, ib111) is None
    assert student_grade(463522, ib001) == "F"
    assert student_grade(463522, ib002) == "A"
    assert student_grade(473521, ib111) == "F"
    assert student_grade(473521, ib001) == "B"


if __name__ == "__main__":
    main()
