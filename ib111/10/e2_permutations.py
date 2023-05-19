from typing import Set


# Napište čistou funkci, která ze vstupního slova vytvoří množinu
# všech jeho permutací (tedy slov takových, že jsou tvořena stejnými
# písmeny v libovolném pořadí).

def permutations(word: str) -> Set[str]:
    if len(word) <= 1:
        return {word}
    result = set()
    for letter in word:
        result |= {letter + rest
                   for rest in permutations(word.replace(letter,'',1))}
    return result

def main() -> None:
#     assert permutations("") == {""}
    assert permutations("aa") == {"aa"}
    assert permutations("Aa") == {"Aa", "aA"}
    assert permutations("abc") == {"abc", "acb", "bac", "bca", "cab", "cba"}


if __name__ == '__main__':
    main()
