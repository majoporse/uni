# V této úloze se budeme zabývat systémem číslování knih ISBN,
# konkrétně variantami ISBN-10 (deseticifernou) a ISBN-13
# (třinácticifernou). Obě tyto varianty ISBN obsahují ve své
# poslední cifře informaci, která slouží k jejich validaci, zatímco
# ostatní cifry reprezentují vybrané atributy dané publikace.

# Napište predikát, jehož hodnota bude ‹True›, představuje-li
# hodnota parametru ‹isbn› korektně utvořené ISBN-10. Parametr bude
# do funkce předáván jako řetězec.

# ISBN-10 se skládá z devíti desítkových cifer, které popisujících
# danou publikaci a poslední desáté cifry, jejíž hodnota může být 0
# až 10 (kde hodnotu 10 zapisujeme jako velké X). Validní ISBN musí
# dále splnit následující podmínku:

# Očíslujeme-li jednotlivé cifry daného ISBN zprava doleva, každou
# z cifer vynásobíme jejím pořadovým číslem, a výsledky sečteme,
# výsledný součet musí být dělitelný jedenácti. (Zkuste si
# rozmyslet, proč potřebujeme u poslední cifry povolit hodnotu 10.)

# Příkladem validního ISBN-10 je 007462542X: ⟦10⋅0 + 9⋅0 + 8⋅7 + 7⋅4
# + 6⋅6 + 5⋅2 + 4⋅5 + 3⋅4 + 2⋅2 + 1⋅10 = 176⟧ a zároveň ⟦176 =
# 11⋅16⟧.

def isbn10_validator(isbn):
    if len(isbn) != 10:
        return False
    count = 0
    for i in range(len(isbn)):
        if ord(isbn[i]) in range(48, 58):
            count += int(isbn[i])*(len(isbn)-i)
        elif ord(isbn[i]) == 88:
            count += 10 * (len(isbn)-i)
        else:
            return False
    if count % 11 != 0:
        return False
    return True


# Dále napište podobný predikát, který ověří korektnost ISBN-13.
# Kontrolní součet provedeme takto:
#
#  1. očíslujeme jednotlivé cifry daného ISBN zprava doleva,
#  2. každou z cifer vynásobíme 3 je-li její pořadové číslo sudé
#  3. výsledky sečteme a ověříme, že výsledek je dělitelný deseti.
#
# Rozmyslete si, proč u této varianty není potřeba povolit „X“.
#
# Příkladem validního ISBN-13 je 9780716703440 protože ⟦9 + 7⋅3 + 8
# + 0⋅3 + 7 + 1⋅3 + 6 + 7⋅3 + 0 + 3⋅3 + 4 + 4⋅3 + 0 = 100⟧ a zároveň
# ⟦100 = 10⋅10⟧.

def isbn13_validator(isbn):
    if len(isbn) != 13:
        return False
    count = 0
    for i in range(1, len(isbn)+1):
        if ord(isbn[-i]) in range(48, 58):
            count += int(isbn[-i]) * (3 if i % 2 == 0 else 1)
        else:
            return False
    if count % 10 != 0:
        return False
    return True


def main():
    assert isbn10_validator("007462542X")
    assert isbn10_validator("1111111111")
    assert isbn10_validator("522516983X")
    assert isbn10_validator("9225169833")
    assert not isbn10_validator("522516983x")
    assert not isbn10_validator("454545454")
    assert not isbn10_validator("X07462542X")
    assert not isbn10_validator("0X7462542X")
    assert not isbn10_validator("1121111111")
    assert not isbn10_validator("9780716703440")
    assert not isbn10_validator("11111a1111")

    assert isbn13_validator("9780716703440")
    assert isbn13_validator("1564236945126")
    assert isbn13_validator("1111111111116")
    assert not isbn13_validator("978071670344X")
    assert not isbn13_validator("007462542X")
    assert not isbn13_validator("1111111111")
    assert not isbn13_validator("1111111111117")
    assert not isbn13_validator("111111a111116")


if __name__ == "__main__":
    main()
