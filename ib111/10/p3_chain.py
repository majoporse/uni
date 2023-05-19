from typing import Set, List


# Napište (čistou) funkci, která dostane na vstupu množinu neprázdných
# slov (obsahují pouze malá písmena české abecedy) a zadanou délku.
# Funkce vrátí množinu všech navazujících posloupností slov zadané
# délky. Navazující posloupnost je taková, že každé další slovo začíná
# stejným znakem, jakým končí předcházející slovo. Slova se v posloupnosti
# nesmí opakovat a navazující posloupnosti budou ve výsledku zapsány tak,
# že jednotlivá slova budou spojena znakem ‹-›.

def word_chain(words: Set[str], length: int) -> Set[str]:
    return chain2(words, length, [], set())


def chain2(words: Set[str], length: int,
           current: List[str], result: Set[str]) -> Set[str]:
    if length == 0:
        return {""}

    if len(current) >= 2 and current[-2][-1] != current[-1][0]:
        return result

    if len(current) == length:
        result.add(transform(current))
        return result

    for word in set(words):
        current.append(word)
        words.remove(word)
        chain2(words, length, current, result)
        words.add(current.pop())

    return result


def transform(list_: List[str]) -> str:
    result = ''
    for i in list_[:-1]:
        result += i + '-'
    result += list_[-1]
    return result


def main() -> None:
    assert word_chain({"oko"}, 1) == {"oko"}
    assert word_chain({"oko", "kolo"}, 0) == {""}
    assert word_chain({"abc", "cde"}, 2) == {"abc-cde"}
    assert word_chain({"abc", "cde"}, 3) == set()
    assert (word_chain({"obal", "kolo", "lok", "oko"}, 3)) \
        == {"kolo-obal-lok", "oko-obal-lok", "lok-kolo-oko",
            "obal-lok-kolo", "kolo-oko-obal", "lok-kolo-obal"}


if __name__ == '__main__':
    main()
