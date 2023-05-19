from typing import Tuple, Optional

# Tato ukázka je první z dvojice, která demonstruje použití
# «tvrzení» (assertion) pro popis vstupních a výstupních podmínek.
# Nejprve si v rychlosti zopakujme trochu teorie.

# Velmi důležitá vlastnost tvrzení je, že ve «správném» (korektním)
# programu «musí za všech okolností platit». Dojde-li k porušení
# některého tvrzení, program havaruje s chybou ‹AssertionError› a
# «vždy» se jedná o «chybu v programu». Je-li tedy uživatel schopen
# programu předložit vstup, který způsobí, že program havaruje
# s chybou ‹AssertionError›, tento program je špatně.

# Smyslem takovýchto tvrzení tedy není kontrola vstupu, nebo jiných
# okolností, které můžou selhat – naopak, slouží jako dokumentace a
# pomůcka k ladění: odhalit příčinu chybného chování programu je tím
# snazší, čím dříve si všimneme nějakou odchylku od chování
# očekávaného. Budeme-li důsledně kontrolovat vstupní a výstupní
# podmínky příkazy ‹assert›, je pravděpodobné, že chybu odchytíme
# brzo (program havaruje).

# Naopak, budeme-li spoléhat na vlastní neomylnost (případně
# neomylnost kolegů), ale chyba se do programu přeci dostane, bude
# se pravděpodobně nekontrolovaně šířit – funkce, kterých vstupní
# podmínka nebyla splněna jednoduše vypočtou nesprávný výsledek, se
# kterým bude program nadále pracovat a produkovat další a další
# nesmyslné mezivýsledky. Výstup nebo chování programu bude
# nesprávné, ale bude velice obtížné a časově náročné poznat, ve
# kterém kroku výpočtu došlo k první chybě.

# Nyní již můžeme přejít k ukázkovému programu: téma první části
# budou čárové kódy. V tomto modulu se budeme zabývat samotným
# kódováním sekvence černých a bílých pruhů, zatímco v části druhé
# (‹ean.py›) se budeme zabývat již dekódovanými číselnými hodnotami.

# Čárový kód sestává z řady «pruhů» (anglicky area), kde každý pruh
# může být černý nebo bílý. Pruhy zabírají celou výšku kódu a mají
# fixní šířku, přičemž na šířku se vždy dotýkají: dva sousední černé
# pruhy tvoří jednolitou plochu. Každá číslice je kódována do sedmi
# pruhů, třeba číslice 2 vypadá takto (v binárním zápisu 0010011; na
# obrázku je šířka jednoho pruhu přehnaná, skutečné pruhy jsou velmi
# úzké).

#    ┌┄┬┄┬┄┬┄┬┄┬┄┬┄┐
#    ┆ ┆ ┆█┆ ┆ ┆█┆█┆
#    ┆ ┆ ┆█┆ ┆ ┆█┆█┆
#    ┆ ┆ ┆█┆ ┆ ┆█┆█┆
#    ┆ ┆ ┆█┆ ┆ ┆█┆█┆
#    ┆ ┆ ┆█┆ ┆ ┆█┆█┆
#    └┄┴┄┴┄┴┄┴┄┴┄┴┄┘
#     0 0 1 0 0 1 1

# Každá číslice má 3 různá možná kódování, značená ‹L›, ‹R› a ‹G›,
# přičemž v kódech EAN-8, se kterými budeme pracovat, se objevují
# pouze kódování ‹L› a ‹R›, která jsou vzájemně inverzní: obrázek
# výše je v kódování ‹L›, odpovídající kódování ‹R› je následovné:

#    ┌┄┬┄┬┄┬┄┬┄┬┄┬┄┐
#    │█┆█┆ ┆█┆█┆ ┆ │
#    │█┆█┆ ┆█┆█┆ ┆ │
#    │█┆█┆ ┆█┆█┆ ┆ │
#    │█┆█┆ ┆█┆█┆ ┆ │
#    │█┆█┆ ┆█┆█┆ ┆ │
#    └┄┴┄┴┄┴┄┴┄┴┄┴┄┘
#     1 1 0 1 1 0 0

# Čárové kódy standardu EAN mají 5 skupin pruhů:
#
#  • počáteční skupina, vždy 101,
#  • první polovina číslic (každá kódována do sedmi pruhů),
#  • středová dělící skupina, vždy 01010,
#  • druhá polovina číslic (opět po sedmi pruzích),
#  • koncová skupina, vždy 101.

# Následuje kompletní příklad se dvěma číslicemi (2 a 2), první
# kódovanou v ‹L› a druhou v ‹R›. Pro odlišení jsou pruhy koncových
# a středové skupiny vybarveny světlejší barvou a místo 0 a 1
# používají symboly _ a X:
#
#   ┌┄┬┄┬┄┬┄┬┄┬┄┬┄┬┄┬┄┬┄┬┄┬┄┬┄┬┄┬┄┬┄┬┄┬┄┬┄┬┄┬┄┬┄┬┄┬┄┬┄┐
#   ┆▓┆ ┆▓┆ ┆ ┆█┆ ┆ ┆█┆█┆ ┆▓┆ ┆▓┆ ┆█┆█┆ ┆█┆█┆ ┆ ┆▓┆ ┆▓┆
#   ┆▓┆ ┆▓┆ ┆ ┆█┆ ┆ ┆█┆█┆ ┆▓┆ ┆▓┆ ┆█┆█┆ ┆█┆█┆ ┆ ┆▓┆ ┆▓┆
#   ┆▓┆ ┆▓┆ ┆ ┆█┆ ┆ ┆█┆█┆ ┆▓┆ ┆▓┆ ┆█┆█┆ ┆█┆█┆ ┆ ┆▓┆ ┆▓┆
#   ┆▓┆ ┆▓┆ ┆ ┆█┆ ┆ ┆█┆█┆ ┆▓┆ ┆▓┆ ┆█┆█┆ ┆█┆█┆ ┆ ┆▓┆ ┆▓┆
#   ┆▓┆ ┆▓┆ ┆ ┆█┆ ┆ ┆█┆█┆ ┆▓┆ ┆▓┆ ┆█┆█┆ ┆█┆█┆ ┆ ┆▓┆ ┆▓┆
#   └┄┴┄┴┄┴┄┴┄┴┄┴┄┴┄┴┄┴┄┴┄┴┄┴┄┴┄┴┄┴┄┴┄┴┄┴┄┴┄┴┄┴┄┴┄┴┄┴┄┘
#    X _ X 0 0 1 0 0 1 1 _ X _ X _ 1 1 0 1 1 0 0 X _ X


# Jako první definujeme predikát ‹barcode_valid›, který bude
# kontrolovat platnost kódu (tzn. má-li požadovanou strukturu a
# správně zakódované číslice). Protože se jedná o relativně složitý
# predikát, některé kontroly oddělíme do samostatných funkcí (mnoho
# z nich navíc později využijeme při dekódování). Krom samotného
# čárového kódu má funkce parametry ‹digit_count› (počet očekávaných
# číslic kódu), ‹l_coding› je požadované kódování levé číselné části
# (‹L› nebo ‹R›) a ‹r_coding› pravé číselné části.

def barcode_valid(barcode: str, digit_count: int,
                  l_coding: str, r_coding: str) -> bool:

    # Vstupní podmínky tohoto predikátu se dotýkají pouze pomocných
    # parametrů. Zapíšeme je jako tvrzení na začátku těla:

    assert l_coding == 'L' or l_coding == 'R'
    assert r_coding == 'L' or r_coding == 'R'
    assert digit_count % 2 == 0

    # Pro lepší čitelnost kódu si pojmenujeme několik užitečných
    # konstant.

    boundary_size = 3
    center_size = 5
    total_marker_size = 2 * boundary_size + center_size

    # Nejprve zkontrolujeme, má-li čárový kód správnou délku: musí
    # obsahovat dvě krajové a jednu středovou skupinu a sudý počet
    # pruhů, které kódují číslice.

    if len(barcode) < total_marker_size:
        return False  # not enough space for all required markers
    if (len(barcode) - total_marker_size) % 2 != 0:
        return False  # does not evenly split into halves

    half_width = barcode_half_width(barcode)
    center_start = boundary_size + half_width
    center_end = center_start + center_size

    # Dále prověříme, že krajové a středová značka mají správné
    # hodnoty.

    if barcode[:boundary_size] != '101':
        return False  # bad start marker
    if barcode[-boundary_size:] != '101':
        return False  # bad end marker
    if barcode[center_start:center_end] != '01010':
        return False

    # Nakonec zkontrolujeme, že má správně zakódované číslice. Zde
    # uplatníme několik pomocných funkcí, kterých definice uvidíme
    # později: (čistá) funkce ‹barcode_digits› z čárového kódu
    # extrahuje dvě číslice-kódující oblasti, predikát
    # ‹barcode_valid_digits› ověří, že vstupní číselná oblast
    # správně kóduje číslice.

    if half_width % 7 != 0:
        return False
    if 2 * half_width // 7 != digit_count:
        return False

    left, right = barcode_digits(barcode)

    if not barcode_valid_digits(left, l_coding):
        return False
    if not barcode_valid_digits(right, r_coding):
        return False

    return True


# Pomocná funkce pro výpočet délky jedné ze dvou číslicových oblastí
# čárového kódu, v počtu pruhů. Vstupní podmínkou je správná délka
# kódu (taková, aby se dal správně rozdělit na příslušné oblasti).
# Vstupní podmínku opět zapíšeme pomocí příkazů ‹assert›.

def barcode_half_width(barcode: str) -> int:
    assert len(barcode) >= 11
    assert (len(barcode) - 11) % 2 == 0
    return (len(barcode) - 11) // 2


# Jak již bylo zmíněno, funkce ‹barcode_digits› extrahuje z čárového
# kódu dvě číselné oblasti. Potřebné vstupní podmínky již kontroluje
# pomocná funkce ‹barcode_half_width› kterou hned na začátku voláme,
# nebudeme je tedy ve funkci ‹barcode_digits› opakovat.

def barcode_digits(barcode: str) -> Tuple[str, str]:
    half_width = barcode_half_width(barcode)
    left = barcode[3:3 + half_width]
    right = barcode[8 + half_width:-3]
    return (left, right)


# Dále potřebujeme být schopni kódovat a dekódovat jednotlivé
# číslice, k čemu nám poslouží následující dvojice funkcí. V druhém
# parametru zadáváme, které kódování číslic požadujeme (‹L› nebo
# ‹R›). V kódovací funkci je vstupní podmínkou jednak správnost
# druhého parametru, ale také to, že ‹digit› je skutečně jediná
# číslice.

def barcode_encode_digit(digit: int, coding: str) -> str:
    assert 0 <= digit <= 9
    assert coding == 'L' or coding == 'R'

    codes = ['0001101', '0011001', '0010011', '0111101', '0100011',
             '0110001', '0101111', '0111011', '0110111', '0001011']

    code = ''
    for area in codes[digit]:
        if coding == 'L':
            code += area
        if coding == 'R':
            code += '1' if area == '0' else '0'
    return code


# Dekódování číslic provedeme „hrubou silou“ (lze to i lépe, ale pro
# tuto chvíli k tomu úplně nemáme ty správné jazykové prostředky).
# Vstupní podmínkou je, že v ‹code› je správný počet pruhů (7).
# Nepovede-li se číslici v zadaném kódování přečíst, funkce vrátí
# ‹None›.

def barcode_decode_digit(code: str, coding: str) -> Optional[int]:
    assert len(code) == 7
    for digit in range(10):
        if barcode_encode_digit(digit, coding) == code:
            return digit
    return None


# Nyní jsme již připraveni definovat predikát, který bude
# kontrolovat správné kódování dané číselné oblasti. Jednak musí
# ověřit správnou délku. Jestli délka vyhovuje, opakovaným použitím
# funkce ‹barcode_decode_digit› se pokusíme jednotlivé číslice
# přečíst – selže-li tato funkce na některé skupině sedmi pruhů, je
# kód neplatný.

def barcode_valid_digits(areas: str, coding: str) -> bool:
    if len(areas) % 7 != 0:
        return False
    while len(areas) > 0:
        if barcode_decode_digit(areas[0:7], coding) is None:
            return False
        areas = areas[7:]
    return True


# Konečně můžeme přistoupit k samotnému kódování a dekódování
# číselných oblastí čárového kódu. Dekódovat lze pouze platnou
# číselnou oblast, vstupní podmínkou je tedy pravdivost predikátu
# ‹barcode_valid_digits›. Je tedy odpovědnost volajícího špatné
# čárové kódy zamítnout před pokusem o jejich dekódování (lze k tomu
# využít třeba právě predikátu ‹barcode_valid_digits›, není-li
# platnost zaručena jinak).

def barcode_decode(areas: str, coding: str) -> str:
    assert barcode_valid_digits(areas, coding)
    result = ''
    while len(areas) > 0:
        digit = barcode_decode_digit(areas[:7], coding)
        areas = areas[7:]

        # Protože v ‹areas› je uložena platná číselná oblast, musí
        # se nám povést každou jednotlivou číslici dekódovat.

        assert digit is not None
        result += str(digit)
    return result


# Zbývá poslední funkce, která ze zadaných číslic vytvoří číselnou
# oblast čárového kódu. Vstupní podmínkou je zde to, že vstupní
# řetězec se skládá pouze z číslic. Všimněte si, že podmínku
# kontrolujeme «postupně», vždy předtím, než se pokusíme danou
# číslici zakódovat.

# Výstupní podmínkou je, že jsme vytvořili platnou číselnou oblast.
# Vzpomeňte si, že výstupní podmínka je (v případě čisté funkce)
# vlastnost návratové hodnoty, kterou funkce sama zaručuje. Výstupní
# podmínku zapisujeme jako tvrzení (‹assert›) před návratem
# z funkce.

def barcode_encode(digits: str, coding: str) -> str:
    result = ''
    for digit in digits:
        assert digit.isdecimal()
        result += barcode_encode_digit(int(digit), coding)
    assert barcode_valid_digits(result, coding)
    return result


def main() -> None:  # demo
    assert not barcode_valid('111', 0, 'L', 'L')
    assert barcode_valid('10101010101', 0, 'L', 'L')
    code_27_good = '101' + '0010011' + '01010' + '0111011' + '101'
    code_27_bad1 = '101' + '0010011' + '01010' + '0101011' + '101'
    code_27_bad2 = '101' + '0010111' + '01010' + '0111011' + '101'
    code_1337_good = '101' + '0011001' + '0111101' + '01010' \
        + '1000010' + '1000100' + '101'
    assert barcode_valid(code_27_good, 2, 'L', 'L')
    assert barcode_valid(code_1337_good, 4, 'L', 'R')
    assert not barcode_valid(code_27_bad1, 2, 'L', 'L')
    assert not barcode_valid(code_27_bad2, 2, 'L', 'L')
    code_27_l, code_27_r = barcode_digits(code_27_good)
    assert code_27_l == '0010011'
    assert code_27_r == '0111011'
    assert barcode_decode(code_27_l, 'L') == '2'
    assert barcode_decode(code_27_r, 'L') == '7'
    assert barcode_encode('13', 'L') == '00110010111101'
    assert barcode_encode('37', 'R') == '10000101000100'


if __name__ == '__main__':
    main()
