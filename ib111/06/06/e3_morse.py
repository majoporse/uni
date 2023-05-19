# Morseova abeceda je způsob jednoduchého kódování písmen latinské
# abecedy používán v telegrafii. Jednotlivá písmena se v ní kódují
# následovně: ‹A›: ‹.-›, ‹B›: ‹-...›, ‹C›: ‹-.-.›, ‹D›: ‹-..›, ‹E›:
# ‹.›, ‹F›: ‹..-.›, ‹G›: ‹--.›, ‹H›: ‹....›, ‹I›: ‹..›, ‹J›: ‹.---›,
# ‹K›: ‹-.-›, ‹L›: ‹.-..›, ‹M›: ‹--›, ‹N›: ‹-.›, ‹O›: ‹---›, ‹P›:
# ‹.--.›, ‹Q›: ‹--.-›, ‹R›: ‹.-.›, ‹S›: ‹...›, ‹T›: ‹-›, ‹U›: ‹..-›,
# ‹V›: ‹...-›, ‹W›: ‹.--›, ‹X›: ‹-..-›, ‹Y›: ‹-.--›, ‹Z›: ‹--..›.

# Napište (čistou) funkci, která na vstupu dostane text složený
# z velkých písmen latinské abecedy (kterých kódy jsou popsány výše)
# a mezer a vrátí tento text zakódovaný do Morseovy abecedy, přičemž
# mezi kódy jednotlivých písmen budou mezery a na místech, kde byly
# mezery v původním textu, budou mezery ve výsledném kódu tři.

MORSE = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
'Y': '-.--', 'Z': '--..'}

def morse_encode(text: str) -> str:
    result = ""
    for i in (text.upper()):
        if i == ' ':
            result += '  '
        else:
            result += MORSE.get(i) + ' '
    return result[:-1]

# Dále napište (čistou) funkci, která na vstupu dostane text
# zakódovaný v Morseově abecedě (postupem popsaným výše) a vrátí
# původní text, ze kterého tento kód vznikl.

def morse_decode(code: str) -> str:
    words = code.split('   ')
    result = ""
    for i in words:
        for j in i.split():
            result += list(MORSE.keys())[list(MORSE.values()).index(j)]
        result += ' '
    return result[:-1]


def main() -> None:
    assert morse_encode("ABC") == ".- -... -.-."
    assert morse_encode("PYTHON") == ".--. -.-- - .... --- -."
    assert morse_encode("WE LOVE PYTHON") == ".-- .   .-.. --- ...- .   .--. "\
                                             "-.-- - .... --- -."

    assert morse_decode(".- -... -.-.") == "ABC"
    assert morse_decode(".--. -.-- - .... --- -.") == "PYTHON"
    assert morse_decode(".-- .   .-.. --- ...- .   .--. -.-- - .... --- -.") \
           == "WE LOVE PYTHON"


if __name__ == '__main__':
    main()
