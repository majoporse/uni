from typing import Set, Dict


# V této úloze budete zjišťovat, je-li možné pomocí alchymie vyrobit
# požadovanou substanci. Vstupem je:
#
#  • množina substancí, které již máte k dispozici (máte-li už
#    nějakou substanci, máte ji k dispozici v neomezeném množství),
#  • slovník, který určuje, jak lze z existujících substancí vytvářet
#    nové: klíčem je substance kterou můžeme vytvořit a hodnotou je
#    seznam „vstupních“ substancí, které k výrobě potřebujeme,
#  • cílová substance, kterou se pokoušíme vyrobit.
#
# Napište predikát, kterého hodnota bude ‹True›, lze-li z daných
# substancí podle daných pravidel vytvořit substanci požadovanou,
# ‹False› jinak.


def is_creatable(owned_substances: Set[str],
                 rules: Dict[str, Set[str]], wanted: str) -> bool:

    to_find = rules.get(wanted)
    if rules == {}:
        return wanted  in owned_substances


    while to_find != set():
        for j in set(to_find):
            if j not in owned_substances and rules.get(j) is not None:
                to_find.update(rules.get(j))
                to_find.remove(j)
                break

            if j in owned_substances:
                to_find.remove(j)
            else:
                return False

    return not len(to_find) > 0

def main() -> None:
    assert is_creatable({"a"}, {}, "a")
    assert is_creatable({"a", "b"}, {"c": {"a", "b"}}, "c")
    assert is_creatable({"a", "b"}, {"c": {"a"}, "d": {"c"}}, "d")

    assert is_creatable({"a", "b"}, {"c": {"a", "b"}, "d": {"a", "c"}, "e": {"d", "b"}, "f": {"e", "a"}}, "f")

    assert is_creatable({"b", "c", "d"}, {"a": {"b", "c", "d"},
                                          "e": {"a", "b", "c", "d"},
                                          "f": {"a", "b", "c", "d", "e"}}, "f")

    assert not is_creatable({"a"}, {"c": {"a", "b"}}, "c")
    assert not is_creatable(set(), {"c": {"a", "b"}}, "c")
    assert not is_creatable({"a", "b"}, {}, "c")
    assert not is_creatable({"a", "b"}, {"c": {"a", "b"}, "d": {"a", "c"},
                                         "e": {"d", "b"},
                                         "f": {"e", "a", "h"}}, "f")


if __name__ == '__main__':
    main()
