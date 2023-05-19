# V této ukázce implementujeme (čistou) funkci, která spočítá tzv.
# Hammingovu vzdálenost dvou řetězců, která určuje, v kolika znacích
# se odlišují. Pro jednoduchost budeme uvažovat pouze řetězce
# stejné délky. Velikost písmen budeme ignorovat (tzn. vzdálenost
# ‹hamming('a', 'A')› bude 0).

def hamming(s1, s2):

    # Doteď jsme to sice nedělali, ale zde se velice žádá ověřit
    # vstupní podmínku, totiž že řetězce jsou stejně dlouhé.

    assert len(s1) == len(s2)

    # Asi nejjednodušší způsob, jak ignorovat velikost písmen je
    # upravit si oba řetězce tak, aby obsahovaly pouze jednu
    # velikost písmen (v tomto případě volíme velká písmena).
    # Protože řetězce jsou vnitřně «neměnné» (nemají vnitřní
    # přiřazení), jejich metody jsou čisté funkce a tedy volání
    # ‹upper› vytvoří nový řetězec a ten původní zůstane beze změny.
    # Přiřazením pouze změníme význam lokálních jmen ‹s1› a ‹s2›.

    s1 = s1.upper()
    s2 = s2.upper()

    # Pro dosud vypočtenou vzdálenost si vytvoříme střadač
    # (akumulátor), do kterého budeme přičítat každou odlišnou
    # dvojici znaků, kterou v řetězcích ‹s1› a ‹s2› potkáme.

    distance = 0

    # V cyklu spočítáme pozice, na kterých se řetězce liší.
    # Použijeme indexovou proměnnou, protože v těle cyklu
    # potřebujeme přistupovat na stejnou pozici dvou různých
    # řetězců. Všimněte si, že řetězce indexujeme stejně jako
    # seznamy nebo n-tice.

    for i in range(len(s1)):
        if s1[i] != s2[i]:
            distance += 1

    # V tuto chvíli máme již v ‹distance› napočítaný výsledek, který
    # vrátíme volajícímu.

    return distance


def main():  # demo
    assert hamming("Python", "python") == 0
    assert hamming("AbCd", "aBcD") == 0
    assert hamming("string", "string") == 0
    assert hamming("aabcd", "abbcd") == 1
    assert hamming("abcd", "ghef") == 4
    assert hamming("Abcd", "bbcd") == 1
    assert hamming("gHefgh", "ghefkl") == 2


if __name__ == '__main__':
    main()
