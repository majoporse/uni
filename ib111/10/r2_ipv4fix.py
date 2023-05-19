from typing import Set


# Napište (čistou) funkci, která dostane na vstup řetězec složený
# pouze z číslic od 1 do 9 včetně a vrátí množinu všech možných IPv4
# adres, z nichž tento řetězec mohl vzniknout vynecháním teček.
# Za IPv4 adresu považujeme řetězec tvořený čtyřmi čísly v rozsahu
# od ‹0› po ‹255› včetně oddělenými tečkami. Například řetězec
# ‹25525511135› mohl vzniknout výše popsaným způsobem z adres
# ‹255.255.11.135› a ‹255.255.111.35›.

def ipv4_restore(digits: str) -> Set[str]:
    pass


def main() -> None:
    assert ipv4_restore("25525511135") == {"255.255.11.135", "255.255.111.35"}
    assert ipv4_restore("1111") == {"1.1.1.1"}
    assert ipv4_restore("555") == set()
    assert ipv4_restore("11112") \
        == {"1.1.1.12", "1.1.11.2", "1.11.1.2", "11.1.1.2"}


if __name__ == '__main__':
    main()
