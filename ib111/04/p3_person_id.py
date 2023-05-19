# Napište predikát, který validuje rodná čísla.  Rodné číslo budeme
# v parametru předávat jako řetězec a pro zjednodušení budeme
# uvažovat pouze rodná čísla v současně přidělované formě:
# ‹RRMMDD/XXXX›, kde:
#
#  • ‹RR› představuje poslední dvojčíslí roku narození,
#  • ‹MM› měsíc narození, jedná-li se o rodné číslo muže a
#    měsíc narození zvýšený o 50 jedná-li se o rodné číslo ženy,
#  • ‹DD› den narození, a konečně
#  • ‹XXXX› je unikátní čtyřčíslí, které odlišuje dvě osoby stejného
#    pohlaví a data narození.

# Například 065101 je prvních šest číslic rodného čísla dívky
# narozené 1. ledna 2006.

# Každé platné rodné číslo musí být navíc po vynechání znaku / beze
# zbytku dělitelné jedenácti. Rodná čísla v uvedeném formátu začala
# platit v roce 1954, proto hodnoty ‹RR› větší než 53 označují roky
# 20. století a ty s hodnotou menší než 54 označují roky
# 21. století. Nezapomeňte se zamyslet, jaká další omezení na platné
# rodné číslo plynou z významu jednotlivých dvojčíslí.
def hasanextraday(year):
    return year % 4 == 0 and year != 0


def person_id_validator(id_candidate):
    if len(id_candidate) != 11:
        return False

    for i in range(len(id_candidate)):

        if ord(id_candidate[i]) not in range(48 if i != 6 else 47,
                                             58 if i != 6 else 48):
            return False

    divby11 = int(id_candidate.replace('/', '')) % 11
    if divby11 != 0:
        return False

    date, num = id_candidate.split('/')
    year = date[:2]
    month = date[2:4]
    day = date[4:6]
    if int(year) not in range(53, 100) and int(year) not in range(00, 21):
        return False

    if int(month) not in range(1, 13) and int(month) not in range(51, 63):
        return False

    if int(day) not in range(1, 31 if int(month) % 2 == 0 else 32)\
       or (int(month) == 2 and hasanextraday(int(year))
           and int(day) not in range(1, 30))\
       or (int(month) == 2 and not hasanextraday(int(year))
           and int(day) not in range(1, 29)):
        return False

    return True


def main():
    assert person_id_validator("010101/0008")
    assert person_id_validator("125430/3545")
    assert person_id_validator("000131/0001")
    assert person_id_validator("200229/0070")
    assert person_id_validator("190228/8080")
    assert not person_id_validator("125431/4545")
    assert not person_id_validator("125430/3544")
    assert not person_id_validator("121301/0040")
    assert not person_id_validator("010166/2000")
    assert not person_id_validator("000001/1000")
    assert not person_id_validator("000100/1000")
    assert not person_id_validator("10101/0008")
    assert not person_id_validator("0101010008")
    assert not person_id_validator("01a101/0008")
    assert not person_id_validator("0010101/0008")
    assert not person_id_validator("200230/0003")
    assert not person_id_validator("190229/9080")


if __name__ == '__main__':
    main()
