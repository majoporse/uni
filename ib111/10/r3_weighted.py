from typing import Set


# Napište čistou funkci, která vrátí množinu všech slov, tvořených
# znaky ‹{"0", "1", "2"}› s danou délkou ‹length› a váhou ‹weight›.
# Váhou myslíme počet nenulových číslic v daném slově.

def weighted_words(length: int, weight: int) -> Set[str]:
    pass


def main() -> None:
    assert weighted_words(1, 2) == set()
    assert weighted_words(0, 0) == {""}
    assert weighted_words(2, 2) == {"11", "12", "21", "22"}
    assert weighted_words(3, 1) == {"001", "002", "010", "020", "100", "200"}


if __name__ == '__main__':
    main()
