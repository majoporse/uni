# † Napište a otypujte funkci ‹parse_datetime›, která z řetězce ve
# formátu ‹den/měsíc/rok hodiny:minuty› přečte datum a čas.
# Návratovou hodnotou funkce bude dvojice ‹(datum, čas)›, kde
# ‹datum› je trojice ve tvaru ‹(den, měsíc, rok)› a ‹čas› je dvojice
# ‹(hodiny, minuty)›. Všech pět položek je typu ‹int›. Není-li
# vstupní řetězec v zadaném formátu, nebo neobsahuje platné datum a
# čas, funkce vrátí ‹None›.

def parse_datetime(input_string):
    pass


def main() -> None:
    assert parse_datetime("19/05/2020 17:00") == ((19, 5, 2020), (17, 0))
    assert parse_datetime("31/03/1998 6:07") == ((31, 3, 1998), (6, 7))
    assert parse_datetime("30/04/2007 7:45") == ((30, 4, 2007), (7, 45))
    assert parse_datetime("30/12/2010 13:30") == ((30, 12, 2010), (13, 30))
    assert parse_datetime("31/08/1998 21:20") == ((31, 8, 1998), (21, 20))
    assert parse_datetime("29/02/2020 23:51") == ((29, 2, 2020), (23, 51)), \
        "not accepting leap year additional day"

    # invalid days
    assert parse_datetime("00/01/2018 10:00") is None, \
        "accepting invalid day"
    assert parse_datetime("31/04/2018 15:12") is None, \
        "accepting invalid day"
    assert parse_datetime("29/02/2019 16:00") is None, \
        "accepting invalid day"
    assert parse_datetime("33/05/2015 15:12") is None, \
        "accepting invalid day"

    # invalid month
    assert parse_datetime("10/00/2018 15:12") is None, \
        "accepting invalid month"
    assert parse_datetime("10/14/2000 15:00") is None, \
        "accepting invalid month"

    # invalid time
    assert parse_datetime("19/05/2020 0:67") is None, \
        "accepting invalid minutes"
    assert parse_datetime("19/05/2020 10:60") is None, \
        "accepting invalid minutes"
    assert parse_datetime("19/05/2020 0:67:00") is None, \
        "accepting invalid time"
    assert parse_datetime("19/05/2020 24:00") is None, \
        "accepting invalid hours"
    assert parse_datetime("19/05/2020 35:00") is None, \
        "accepting invalid hours"

    # invalid format
    assert parse_datetime("10:14:2000 15:00") is None, \
        "accepting invalid format"
    assert parse_datetime("10:14:2000:15:00") is None, \
        "accepting invalid format"
    assert parse_datetime("10/14/2000") is None, \
        "accepting invalid format"
    assert parse_datetime("15:00 10/14/2000") is None, \
        "accepting invalid format"
    assert parse_datetime("invalid text") is None, \
        "accepting invalid format"
    assert parse_datetime("1/1/2020 time") is None, \
        "accepting invalid format"
    assert parse_datetime("date 20:15") is None, \
        "accepting invalid format"
    assert parse_datetime("20/08/2021 O:12") is None, \
        "accepting invalid format (the letter O is not the digit 0)"
    assert parse_datetime("20/O8/2021 0:12") is None, \
        "accepting invalid format (the letter O is not the digit 0)"


if __name__ == "__main__":
    main()
