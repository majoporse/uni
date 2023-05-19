from typing import Dict
from math import isclose


# V této ukázce demonstrujeme použití slovníku (‹dict›) k jednoduché
# frekvenční analýze textu, konkrétně výpočtu relativní frekvence
# digramů, kde:
#
#  • digram je dvojice (po sobě jdoucích) písmen,
#  • relativní frekvencí myslíme poměr počtu výskytů daného digramu
#    vůči celkovému počtu digramů.
#
# Implementace bude čistá funkce, která na vstupu dostane řetězec a
# výstupem bude slovník, kde klíče budou dvojpísmenné řetězce a
# hodnoty budou typu ‹float› v rozsahu 0–1 takové, že součet všech
# hodnot v slovníku bude 1.

def digram_frequency(text: str) -> Dict[str, float]:
    freq: Dict[str, float] = {}

    # Nejprve potřebujeme zjistit samotné počty výskytů jednotlivých
    # digramů, které v dalším cyklu normalizujeme. Procházíme
    # všechny dvojpísmenné podřetězce, ale dále se zabýváme pouze
    # těmi, které sestávají ze dvou písmen (tzn. mezery,
    # interpunkci, číslice atd. ignorujeme). Slovník indexujeme
    # klíčem – indexace funguje podobně jako u seznamu, s tím
    # rozdílem, že indexy nemusí být celá čísla, ani nemusí tvořit
    # souvislou řadu. Pokus o indexaci klíčem, který ve slovníku
    # zatím neexistuje, je chyba. Zde stojí za připomenutí, že
    # operátor ‹x += y› je obvykle zkratka pro ‹x = x + y›, a tedy
    # ‹dict[key] += y› se chová jako ‹dict[key] = dict[key] + y›,
    # tedy pokus o indexaci klíčem ‹key› na pravé straně proběhne
    # dříve, než samotné vložení klíče vnitřním přiřazením.

    for i in range(len(text) - 1):
        digram = text[i:i + 2].lower()
        if digram.isalpha():

            # Na ověření přítomnosti klíče ve slovníku můžeme použít
            # operátor ‹in› resp. ‹not in›.

            freq[digram] = freq.get(digram,0) + 1
            

    # Metoda ‹values› nám umožňuje chovat se k hodnotám uloženým ve
    # slovníku jako k sekvenci (klíče zapomene). Sečíst všechny
    # hodnoty ve slovníku je tedy velmi jednoduché.

    total = sum(freq.values())

    # Metoda ‹items› naopak ze slovníku vyrobí sekvenci dvojic
    # (klíč, hodnota) – tuto sekvenci lze iterovat (stejně jako
    # seznam) a jednotlivé dvojice lze rozbalit do proměnných.

    for key, value in freq.items():
        freq[key] = value / total

    return freq


# Jako obvykle si ověříme, že funkce ‹digram_frequency› se na
# jednoduchých vstupech chová tak, jak čekáme:

def main() -> None:  # demo
    freq = digram_frequency("lorem ipsum dolor sit amet")
    assert isclose(freq['lo'], 2 / 17)
    assert isclose(freq['or'], 2 / 17)
    assert isclose(freq['am'], 1 / 17)
    assert 'rs' not in freq
    assert ' i' not in freq

    freq = digram_frequency("hrad Veveří nehoří")
    assert isclose(freq['ve'], 2 / 13)
    assert isclose(freq['ří'], 2 / 13)
    assert isclose(freq['ne'], 1 / 13)

    freq = digram_frequency("ехал Грека через реку")
    assert isclose(freq['ре'], 3 / 14)
    assert isclose(freq['ек'], 2 / 14)


if __name__ == '__main__':
    main()
