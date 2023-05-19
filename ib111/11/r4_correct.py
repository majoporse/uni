from typing import Set, Optional


# V první ukázce jsme viděli jednoduchý program na kontrolu
# pravopisu. Tento úkol bude podobný, ale místo vyznačení nalezených
# chyb je budeme rovnou opravovat.

# Ze 4. kapitoly si možná pamatujete tzv. Hammingovu vzdálenost:
# jednalo se o funkci, která dvojici slov stejné délky přidělí
# nezáporné celé číslo: počet znaků, ve kterých se liší. Náš
# „autocorrect“ bude pro jednoduchost používat právě tuto metriku.

# Pro každé slovo ze vstupu, které se nenachází ve slovníku, tedy:
#
#  1. nalezněte všechna slova stejné délky,
#  2. vyberte ta, která mají minimální Hammingovu vzdálenost od toho
#     vstupního,
#  3. obsahuje-li seznam slova, která se se vstupem shodují na první
#     pozici, ponechte pouze tato,
#  4. obdobně na poslední pozici, pak na druhé, předposlední, atd.,
#  5. ze zbytku vyberte první slovo dle abecedy a toto použijte jako
#     opravu.

# Procedura ‹autocorrect› má 3 parametry: název souboru
# s komprimovaným slovníkem (ve formátu ‹gzip›), název vstupního
# souboru a název výstupního souboru, do kterého zapíše opravený
# text. Níže máte nachystaných několik čistých funkcí, které Vám
# řešení můžou usnadnit – rozmyslete si, co dělají, a jak je použít.

def autocorrect(dict_file: str, input_file: str,
                output_file: str) -> None:
    pass


def hamming(s1: str, s2: str) -> int:
    assert len(s1) == len(s2)

    distance = 0

    for x, y in zip(s1.upper(), s2.upper()):
        if x != y:
            distance += 1

    return distance


def closest_by_hamming(word: str, words: Set[str]) -> Set[str]:
    res: Set[str] = set()
    best: Optional[int] = None

    for curr_word in words:
        distance = hamming(word, curr_word)

        if best is None or distance < best:
            res = set()
            best = distance
        if distance == best:
            res.add(curr_word)

    return res


def closest_by_ends(word: str, candidates: Set[str]) -> Set[str]:
    for offset in range(len(word) // 2):
        for direction in [-1, 1]:
            idx = direction * offset
            filtered = set()

            for curr_word in candidates:
                if word[idx] == curr_word[idx]:
                    filtered.add(curr_word)

            if filtered:
                candidates = filtered

    return candidates


def main() -> None:
    dict_file = "zz.words.gz"
    data = [("large caterpillar\nsmoking\t a long hookah",
             "large caterpillar\nsmoking\t a long hookah"),
            ("large caterplilar\nsmoking\t a long hookah",
             "large caterpillar\nsmoking\t a long hookah"),
            ("large pytoon.\nsmoikng\t a long hookab!",
             "large python.\nsmoking\t a long hookah!"),
            ("pithon is great.\nfloing circus \t is a blost!",
             "python is great.\nflying circus \t is a blast!")]

    for bad, good in data:
        with open("zt.correct.in", "w+") as file:
            file.write(bad)
        autocorrect(dict_file, "zt.correct.in", "zt.correct.out")
        with open("zt.correct.out") as file:
            corrected = file.read()
            assert corrected == good, (corrected, good)


if __name__ == "__main__":
    main()
