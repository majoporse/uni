from typing import List, Optional, Tuple

# † V této ukázce použijeme celou řadu standardních modulů jazyka
# Python k vyřešení relativně složitého úkolu, který obnáší několik
# komplikovaných interakcí s prostředím. Doporučujeme u každého
# modulu alespoň zběžně prohlédnout dokumentaci dostupnou na adrese
# ‹http://docs.python.org/3/› (a trochu méně zběžně u funkcí, které
# v ukázce používáme a kterým třeba nerozumíte). Ne proto, abyste se
# knihovnu jako takovou učili – ta je samozřejmě specifická pro
# jazyk Python, ale abyste se učili číst technickou dokumentaci (a
# také v ní hledat) – to je naopak schopnost, kterou využijete ještě
# mnohokrát, bez ohledu na to, v jakém jazyce budete programovat.

# Nyní již k samotnému problému. Knihovny třetích stran určené pro
# jazyk Python jsou obvykle k dispozici v takzvaném PyPI – Python
# Package Index. Naším úkolem bude podle jména knihovny (resp.
# balíku, angl. «package») příslušnou knihovnu najít, stáhnout
# z internetu, a z distribučního souboru ve formátu ‹.whl› (Python
# wheel) získat základní informace o této knihovně, například jméno
# autora nebo její krátký popis.

# Co k tomu budeme potřebovat? Protože jak seznam adres, ze kterých
# lze distribuční soubor získat, tak samotný tento soubor musíme
# stáhnout z internetu, budeme k tomu potřebovat tzn. klienta
# protokolu HTTP (tento protokol běžně využívají webové prohlížeče
# pro stahování stránek a jiných souborů ze serverů v internetu).
# Jeden takový klient je k dispozici v modulu ‹http.client›:

import http.client

# Dále budeme pracovat s textem: jednak s již zmiňovaným seznamem
# adres, ale také s textovým souborem s metadaty, který je součástí
# distribučního souboru ‹.whl›. Protože budeme vyhledávat vzory,
# které nejsou úplně jednoduché, použijeme k tomu regulární výrazy,
# dostupné v modulu ‹re›.

import re

# Distribuční soubor ‹.whl› vnitřně používá formát ZIP, který nám
# pomůže načíst modul ‹zipfile›. Abychom mohli pracovat se souborem
# uloženým v paměti (a nikoliv na disku), budeme potřebovat ještě
# pomocnou třídu ‹BytesIO› ze standardního modulu ‹io›.

from zipfile import ZipFile
from io import BytesIO

# Konečně v testech se nám bude hodit modul ‹sys›, konkrétně
# ‹sys.stderr› pro výpis chyb na obrazovku a ‹sys.exit› pro
# neúspěšné ukončení skriptu.

import sys


# Jako první si zadefinujeme podprogram ‹fetch_package_paths›, který
# podle názvu balíku, zadaném parametrem ‹package›, stáhne ze
# serveru ‹pypi.org› index distribučních souborů ve formátu HTML
# a najde v něm všechny odpovídající cesty (samotné distribuční
# soubory jsou uloženy na serveru ‹files.pythonhosted.org›).

def fetch_package_paths(package: str) -> List[str]:

    # Nejprve navážeme spojení se serverem, a zašleme mu tzv.
    # «požadavek»: v tomto případě ‹GET› a cestu k souboru nebo
    # adresáři, kterého obsah chceme stáhnout.

    conn = http.client.HTTPSConnection('pypi.org')
    conn.request("GET", '/simple/' + package + '/')

    # Dále získáme odpověď serveru a zjistíme, jestli byl požadavek
    # úspěšný: pokud ano, stavový kód odpovědi bude 200 (toto je
    # „dobře známé“ číslo, podobně jako třeba 404, které indikuje
    # chybu „file not found“).

    response = conn.getresponse()
    if response.status != 200:
        return []

    # Byl-li požadavek úspěšný, přečteme data, která nám server
    # poslal – bude to velmi jednoduchý HTML soubor, který
    # v podstatě obsahuje pouze seznam odkazů na jednotlivé
    # distribuční soubory. Protože struktura souboru i samotných
    # odkazů je velmi jednoduchá, můžeme si dovolit použít k jejich
    # získání regulární výraz (pozor, v obecném případě by tento
    # přístup nefungoval!).

    html = response.read().decode('utf-8')

    # Samotný regulární výraz („regex“) popisuje řetězce, které
    # začínají prefixem uloženým v ‹base› který nás dále nebude
    # zajímat, a pokračují ‹/packages/…/soubor.whl› – toto je část,
    # která nás zajímá, proto je v regexu uzavřena v závorkách,
    # které indikují tzv. «capture group». Funkce ‹re.findall› nám
    # vrátí právě ty části původního řetězce, které odpovídají
    # částem regexu uzavřeným v závorkách. Tato část regexu popisuje
    # řetězce, které začínají ‹/packages/›, pokračují nějakým
    # nenulovým počtem znaků, které ale nesmí být ‹#› ani ‹"›, a
    # končí příponou ‹.whl›. Adresa pokračuje znakem ‹#› který ale
    # již nebudeme potřebovat.

    base = 'https://files.pythonhosted.org'
    regex = base + r'(/packages/[^#"]+\.whl)#'
    return re.findall(regex, html)


# Další podprogram bude ‹fetch_package›, který stáhne distribuční
# soubor zadaný cestou ‹path› (kterou lze získat použitím
# ‹fetch_package_paths›). Výsledkem bude ‹None› (v případě, že se
# soubor nepovede stáhnout) nebo instance třídy ‹ZipFile›, která nám
# umožní jednoduše přistupovat k obsahu distribučního souboru.
# Protože stažený obsah souboru dostaneme jako hodnotu typu ‹bytes›
# a třída ‹ZipFile› očekává otevřený soubor, použijeme ještě
# pomocnou třídu ‹BytesIO›, která poskytuje rozhraní souboru, ale
# data přečte právě z hodnoty typu ‹bytes›.

def fetch_package(path: str) -> Optional[ZipFile]:
    conn = http.client.HTTPSConnection('files.pythonhosted.org')
    conn.request("GET", path)
    response = conn.getresponse()
    if response.status != 200:
        return None
    return ZipFile(BytesIO(response.read()))


# Distribuční soubor je archiv: obsahuje v sobě řadu menších
# souborů, které tvoří samotnou knihovnu, a dále soubory, které
# balík a jeho obsah popisují: tzv. «metadata». Hlavní část metadat
# se nachází v souboru ‹METADATA› ve složce ‹balík-verze.dist-info›:
# protože přesnou verzi (a v tuto chvíli vlastně ani název balíku)
# neznáme, pomůžeme si opět regulárním výrazem. Protože název složky
# nemůže obsahovat lomítko, budeme hledat nejdelší řetězec bez
# lomítek, který končí ‹.dist-info› – tato část odpovídá názvu
# složky, ‹/METADATA› pak názvu souboru.

# Jakmile najdeme správný soubor, přečteme jeho obsah (dostaneme
# hodnotu typu ‹bytes›), dekódujeme do hodnoty typu ‹str› a pomocí
# ‹split› získáme první „odstavec“ (blok textu oddělený od zbytku
# prázdným řádkem), který obsahuje strojově zpracovatelnou část
# metazz.

def get_metadata(pkg: ZipFile) -> Optional[str]:
    for f in pkg.namelist():
        if re.match(r'[^/]+\.dist-info/METADATA', f):
            return pkg.read(f).decode('utf-8').split('\n\n')[0]
    return None


# Funkce ‹get_metadata› vrátí řetězec, ve kterém je na každém řádku
# nejprve název pole (angl. «field») a za ním dvojtečkou oddělená
# hodnota tohoto pole. Například:
#
#     Author: Random J. Hacker
#     Summary: An efficient flux capacitor frobnifier.
#
# Jednotlivá pole nejsou unikátní – můžou se objevit několikrát, a
# tedy mít víc asociovaných hodnot. Proto je nemůžeme ukládat do
# obyčejného slovníku. Možností jak taková data reprezentovat je
# několik, my pro jednoduchost zvolíme prostý seznam dvojic. Čistá
# funkce ‹get_info› tento seznam vytvoří z metadat uložených
# v jednom řetězci (tak, jak je dodá podprogram ‹get_metadata›).
# Čistá funkce ‹find_item› pak v tomto seznamu najde první hodnotu,
# která odpovídá zadanému klíči.

Info = List[Tuple[str, str]]


def get_info(metadata: str) -> Info:
    info = []
    for line in metadata.split('\n'):
        k, v = line.split(': ', 1)
        info.append((k, v))
    return info


def find_item(info: Info, key: str) -> Optional[str]:
    for k, v in info:
        if k == key:
            return v
    return None


# Veškerou funkcionalitu spojíme do jednoho jednoduše použitelného
# podprogramu, který v parametru dostane název balíku a na výstupu
# poskytne metadata ve strukturované podobě (typu ‹Info›).
# Nepodaří-li se některá operace, ‹fetch_latest_info› vrátí ‹None›.

def fetch_latest_info(pkg_name: str) -> Optional[Info]:
    paths = fetch_package_paths(pkg_name)
    if paths:
        path = paths[-1]  # latest version comes last
        pkg = fetch_package(path)
        if pkg is not None:
            meta = get_metadata(pkg)
            if meta is not None:
                return get_info(meta)
    return None


# Nakonec program otestujeme. Jako cvičení si můžete automatický
# test nahradit jednoduchým uživatelským rozhraním: názvy balíků
# můžete vzít třeba z argumentů programu (dostupné v seznamu
# ‹sys.argv›) a odpovídající informace vypsat na standardní výstup
# (použitím zabudované procedury ‹print›).

def main() -> None:  # demo
    info = fetch_latest_info('black')
    if info is None:
        print("download failed, aborting test", file=sys.stderr)
        sys.exit(1)
    else:
        assert find_item(info, 'Summary') == \
            'The uncompromising code formatter.'
        assert find_item(info, 'Author') == 'Łukasz Langa'


if __name__ == '__main__':
    main()
