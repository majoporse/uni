# Napište čistou funkci ‹word_wrap› která podle potřeby nahradí
# mezery ve vstupním řetězci ‹orig› za znaky nového řádku, a to tak,
# aby pro každý řádek platilo, že je buď dlouhý nejvýše
# ‹max_line_len› znaků, nebo neobsahuje žádné mezery.

def word_wrap(orig: str, max_line_len: int) -> str:
    pass


def main() -> None:
    test_str = "Python python python.\n" + \
               "Python.\n" + \
               "Python python python python.\n" + \
               "Python python.\n"

    expected_results = {
        13:
        "Python python\n" +
        "python.\n" +
        "Python.\n" +
        "Python python\n" +
        "python\n" +
        "python.\n" +
        "Python\n" +
        "python.\n",

        1:
        "Python\n" +
        "python\n" +
        "python.\n" +
        "Python.\n" +
        "Python\n" +
        "python\n" +
        "python\n" +
        "python.\n" +
        "Python\n" +
        "python.\n",

        35:
        "Python python python.\n" +
        "Python.\n" +
        "Python python python python.\n" +
        "Python python.\n",

        21:
        "Python python python.\n" +
        "Python.\n" +
        "Python python python\n" +
        "python.\n" +
        "Python python.\n"}

    for max_len, expected in expected_results.items():
        assert word_wrap(test_str, max_len) == expected, max_len

    assert word_wrap("xxxx xx xxx xx", 4) == "xxxx\nxx\nxxx\nxx"


if __name__ == "__main__":
    main()
