from typing import Set


# Napište (čistou) funkci, která dostane na vstupu množinu neprázdných
# slov (obsahují pouze malá písmena české abecedy) a vrátí délku nejdelšího
# slovního kruhu, který se z těchto slov dá vytvořit. Pokud se žádný slovní
# kruh vytvořit nedá, vrátí 0.

# Slovní kruh je posloupnost slov (bez opakování) taková, že každé další
# slovo začíná stejným znakem, jakým končí slovo předcházející. Navíc první
# slovo v posloupnosti začíná stejným znakem, jakým končí poslední slovo.

def word_circle(words: Set[str]) -> int:
    pass


def main() -> None:
    assert word_circle(set()) == 0
    assert word_circle({"abc", "klm"}) == 0
    assert word_circle({"abcd", "def", "fa"}) == 3
    assert word_circle({"aba"}) == 1
    assert word_circle({"abc", "ca", "cd", "da"}) == 3
    assert word_circle({"abc", "ca", "acd", "da"}) == 4


if __name__ == '__main__':
    main()
