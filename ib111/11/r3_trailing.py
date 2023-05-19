import sys


# Někdy se stane, že při programování v Pythonu omylem necháte na
# konci řádku mezery, nebo jiné bílé znaky (např. tabulátor). Při
# kontrole programem ‹flake8› je toto označeno za chybu. Vaším
# úkolem je napsat jednoduchý program, který tento typ chyby
# v zadaných souborech opraví. Seznam souborů k opravě dostanete
# jako argumenty na příkazové řádce (v Pythonu je naleznete
# v seznamu ‹sys.argv› počínaje indexem 1). Soubor, se kterým právě
# pracujete, můžete načíst celý do paměti.
#
# Poznámka: tento program lze testovat dvěma způsoby. Spustíte-li
# jej bez dalších parametrů, spustí se přiložené testy. Předáte-li
# naopak programu nějaké parametry, spustí se přímo procedura
# ‹trailing›, která tyto zpracuje obvyklým způsobem. Například:
#
#     python r3_trailing.py soubor1.txt soubor2.py

def trailing() -> None:
    for arg in sys.argv[1:]:
        with open(arg) as file:
            content = file.readlines()
        with open(arg, 'w') as file:
            for line in content:
                line = line.rstrip()
                print(line, file=file)


def main() -> None:
    if len(sys.argv) > 1:
        trailing()
        return

    files = {"zt.trailing1.txt":
             ("   py    \npy py\t\t\t\n\n   \n\t\npy\n",
              "   py\npy py\n\n\n\npy\n"),

             "zt.trailing2.txt":
             ("  \t\npython \npython\n", "\npython\npython\n"),

             "zt.trailing3.txt":
             ("Python  \tPython  \t\n\n", "Python  \tPython\n\n")}

    for name, (data, _) in files.items():
        with open(name, "w+") as file:
            file.write(data)

    sys.argv = [""] + list(files.keys())
    trailing()

    for name, (_, expect) in files.items():
        with open(name, "r") as file:
            assert file.read() == expect, name + " is wrong"


if __name__ == '__main__':
    main()
