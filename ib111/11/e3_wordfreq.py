from typing import List


# Napište funkci, která ve vstupním souboru najde 3 nejčastější
# slova. Obsahuje-li soubor méně než 3 různá slova, výsledný seznam
# bude kratší. V případě, kdy mají dvě slova stejnou frekvenci
# výskytu, upřednostněte to, které je lexikograficky menší.

def most_common(path: str) -> List[str]:
    pass


def main() -> None:
    data = [("Python", ["python"]),
            ("Python python python", ["python"]),
            ("Pamatujte si, že return vždy ukončí vykonávání " +
             "funkce. Znamená to, že kdykoliv se provede return, " +
             "je to poslední příkaz před ukončením funkce, a nic " +
             "dalšího se v této funkci vykonávat nebude. " +
             "Zejména ne příkaz, který po return bezprostředně " +
             "následuje.", ["return", "funkce", "příkaz"]),
            ("aa, aa, bb, bb, a", ["aa", "bb", "a"])]

    for text, expect in data:
        with open('zt.wordfreq.txt', "w") as file:
            file.write(text)
        common = most_common('zt.wordfreq.txt')
        assert common == expect, (common, expect)


if __name__ == "__main__":
    main()
