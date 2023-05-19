from typing import Optional

# European Article Number (EAN) je systém číslování výrobků, který
# pravděpodobně znáte z čárových kódů v supermarketech. EAN funguje
# podobně jako ISBN, se kterým jste minulý týden pracovali
# v příkladu ‹04/isbn.py›, nicméně neomezuje se na knihy. V této
# ukázce budeme pokračovat v používání «tvrzení» (‹assert›) pro
# popis vstupních a výstupních podmínek funkcí. Protože budeme chtít
# převádět číselné kódy na čárové a obráceně, využijeme funkce pro
# práci s čárovými kódy, které jsme definovali v předchozí ukázce.

from d2_barcode import barcode_valid, barcode_decode, barcode_encode, \
    barcode_digits


# Podobně jako v případě ISBN budeme EAN reprezentovat jako řetězec.
# Jako první si zadefinujeme predikát, který bude rozhodovat,
# jedná-li se o platný EAN: postup je podobný jako pro ISBN,
# poslední cifra je kontrolní. EAN existuje v několika délkách, ale
# algoritmus pro jejich kontrolu je vždy stejný: proto dostane náš
# predikát krom samotného EAN jako parametr i očekávanou délku kódu.
# Tento predikát samotný nemá žádné vstupní podmínky.

def ean_valid(ean: str, length: int) -> bool:
    checksum = 0
    odd = length % 2 == 1
    if len(ean) != length:
        return False
    for digit in ean:
        if not digit.isdecimal():
            return False
        checksum += int(digit) * ean_digit_weight(odd)
        odd = not odd

    return checksum % 10 == 0


# Pomocná funkce, která popisuje váhy jednotlivých číslic v EAN
# kódu (pro účely výpočtu kontrolní číslice).

def ean_digit_weight(odd: bool) -> int:
    return 1 if odd else 3


# Další funkce, kterou budeme definovat, slouží k vytvoření platného
# EAN-13 kódu z jednotlivých komponent: prefixu GS1 (zjednodušeně
# odpovídá zemi výrobce), kódu výrobce (který je minimálně
# pěticiferný) a kódu samotného výrobku. Vstupní podmínky odpovídají
# omezením na jednotlivé komponenty. Celková délka kódu bez
# kontrolního součtu musí být 12 cifer. Funkce komponenty zkombinuje
# a přidá kontrolní cifru. Výstupní podmínkou je, že jsme vytvořili
# platný třináctimístný EAN kód (kontrolujeme ji těsně před návratem
# z funkce).

def generate_ean(gs1: str, manufacturer: str, product: str) -> str:
    assert len(gs1) == 3
    assert len(manufacturer) >= 5
    assert len(gs1) + len(manufacturer) + len(product) == 12

    ean = gs1 + manufacturer + product
    odd = True
    check = 0
    for digit in ean:
        check += int(digit) * ean_digit_weight(odd)
        odd = not odd
    check = 10 - check % 10

    ean = gs1 + manufacturer + product + str(check)
    assert ean_valid(ean, 13)
    return ean


# Následují dvě funkce pro konverzi mezi číselným a čárovým kódem.
# První dostane na vstupu platnou číselnou reprezentaci EAN-8 (tuto
# vstupní podmínku kontroluje první příkaz ‹assert›). Výstupní
# podmínkou naopak je, že funkce vytvoří platný čárový kód – tuto
# kontrolujeme, jak je obvyklé, těsně před návratem.

def ean8_to_barcode(ean: str) -> str:
    assert ean_valid(ean, 8)
    left = barcode_encode(ean[0:4], 'L')
    right = barcode_encode(ean[4:8], 'R')

    barcode = '101' + left + '01010' + right + '101'
    assert barcode_valid(barcode, 8, 'L', 'R')
    return barcode


# Poslední funkce v tomto souboru slouží pro opačnou konverzi:
# z čárového kódu vytvoří číselnou reprezentaci. Vstupní podmínkou
# je, že čárový kód je platný a kóduje 8 číslic; toto díky predikátu
# ‹barcode_valid› lehce ověříme. Nicméně si musíme dát pozor na
# «výstupní» podmínku: mohlo by se zdát, že analogicky k předchozímu
# případu by bylo rozumné požadovat platnost číselného EAN.

# Není tomu tak: byla-li splněna vstupní podmínka (čárový kód
# ‹barcode› je platný), funkce musí svoji výstupní podmínku «vždy
# splnit». Musíme si ale uvědomit, že existují platné osmičíslicové
# čárové kódy, které «nekódují» platný EAN-8. Proto je výstupní
# podmínka platnosti EAN kódu příliš silná – nedokážeme ji
# zabezpečit.

# Jako vhodné řešení se jeví v případě, kdy na vstupu dostaneme
# čárový kód reprezentující neplatný EAN, vrátit hodnotu ‹None›:
# výstupní podmínku tak zeslabíme jen minimálně. Bude vždy platit,
# že výstupem je buď platný EAN-8 (a to vždy, když je to možné),
# nebo hodnota ‹None› (pouze v případech, kdy vstup reprezentoval
# neplatný EAN-8). Ze zápisu návratové hodnoty je zřejmé, že tato
# výstupní podmínka je splněna, nemá tedy smysl ji dodatečně
# kontrolovat příkazem ‹assert›.

def barcode_to_ean8(barcode: str) -> Optional[str]:
    assert barcode_valid(barcode, 8, 'L', 'R')
    left, right = barcode_digits(barcode)
    ean = barcode_decode(left, 'L') + barcode_decode(right, 'R')
    if not ean_valid(ean, 8):
        return None
    return ean


def main() -> None:  # demo
    assert ean_valid("12345670", 8)
    assert ean_valid("1122334455666", 13)
    assert not ean_valid("12345674", 8)
    assert not ean_valid("1122334455664", 13)
    assert generate_ean("123", "123212", "123") == "1231232121235"
    assert generate_ean("444", "12345", "1111") == "4441234511119"
    assert ean8_to_barcode("12345670") == \
           "10100110010010011011110101000110" \
           "10101001110101000010001001110010101"
    assert ean8_to_barcode("11112228") == \
           "10100110010011001001100100110010101" \
           "01101100110110011011001001000101"
    assert barcode_to_ean8("10100110010010011011110101000110"
           "10101001110101000010001001110010101") == "12345670"
    assert barcode_to_ean8("10100110010011001001100100110010101"
           "01101100110110011011001001000101") == "11112228"
    assert barcode_to_ean8("10100110010011001001100100110010101"
           "01101100110110011011001110010101") is None


if __name__ == '__main__':
    main()
