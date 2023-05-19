from typing import Dict, List


# Napište predikát, jehož hodnota bude ‹True› pokud lze požadované slovo
# ‹wanted› utvořit z iniciálního slova ‹initial› pomocí přepisovacích pravidel
# ‹rules› a ‹False› jinak. Slova vytváříme tak, že kterékoli písmeno z již
# vytvořených slov nacházející se mezi klíči slovníku pravidel ‹rules›
# můžeme nahradit za kterékoli písmeno z příslušné hodnoty. (Pro zjednodušení
# možnost zacyklení procesu vytváření slov nemusíte vůbec řešit.)

def is_creatable(wanted: str, initial: str,
                 rules: Dict[str, List[str]]) -> bool:

    if wanted == initial:
        return True
    else:
        if rules == {}:
            return False
        for num, char in enumerate(initial):
            if wanted[num] == char:
                continue
            elif rules.get(char) is not None:
                new_char = rules[char]
                for x in new_char:
                    new_initial = initial[:num] + x + initial[num + 1:]
                    if is_creatable(wanted, new_initial, rules):
                        return True
        return False


def main() -> None:
    assert is_creatable("abc", "abc", {})
    assert not is_creatable("bc", "abc", {})
    assert is_creatable("abc", "abc", {"a": ["c", "d"]})
    assert not is_creatable("bbc", "abc", {"a": ["c", "d"]})
    assert is_creatable("aec", "abc",
                        {"a": ["e", "f"], "b": ["a", "f"]})
    assert is_creatable("fec", "abc",
                        {"a": ["e", "f"], "b": ["a", "f"]})
    assert is_creatable("bbb", "aaa", {"a": ["c"], "c": ["b"]})
    assert is_creatable("bcb", "aaa", {"a": ["c"], "c": ["b"]})
    assert is_creatable("ccc", "aaa", {"a": ["c"], "c": ["b"]})
    assert is_creatable("abcd", "aaaa",
                        {"a": ["b", "c", "d", "e"], "c": ["b"]})
    assert is_creatable("a", "a", {"a": ["b", "c"]})
    assert not is_creatable("aa", "bb",
                            {"b": ["c", "d", "e", "f"],
                             "c": ["d", "e", "f"],
                             "d": ["e", "f"],
                             "e": ["f"]})
    assert is_creatable("fd", "bc",
                        {"b": ["c", "d", "e"],
                         "c": ["d"],
                         "d": ["f"],
                         "e": ["f"]})


if __name__ == '__main__':
    main()
