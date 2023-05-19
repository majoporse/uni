# Napište a otypujte funkci ‹parse_gps›, která přečte GPS souřadnice
# ze vstupního řetězce ‹raw›. Očekávaný vstup je ve formátu
# ‹lat=X;lon=Y› kde ‹X› a ‹Y› jsou čísla s povinnou desetinnou
# tečkou. Je-li vstup ve správném formátu a obě souřadnice spadají
# do svého přípustného rozsahu, funkce vrátí dvojici hodnot typu
# ‹float›, které odpovídají číselným hodnotám zeměpisné šířky
# (latitude) a délky (longitude). V opačném případě vrátí ‹None›.
# Přípustný rozsah zeměpisné šířka je -90 až 90 a zeměpisné délky
# -180 až 180.


def parse_gps(raw):
    pass


# Dále napište a otypujte funkci ‹parse_gps_stream›, která přečte
# seznam GPS souřadnic a vrátí seznam dvojic s číselnými hodnotami
# souřadnic. Souřadnice na vstupu jsou každá na vlastním řádku.
# Nekóduje-li kterýkoliv řádek GPS souřadnici, funkce vrátí ‹None›.

def parse_gps_stream(raw):
    pass


def main() -> None:
    assert parse_gps("lat=49.2099839;lon=16.5989169") \
        == (49.2099839, 16.5989169)
    assert parse_gps("lat=49.2099839;lon=-16.5989169") \
        == (49.2099839, -16.5989169)
    assert parse_gps("lat=-49.2099839;lon=16.5989169") \
        == (-49.2099839, 16.5989169)

    assert parse_gps("lat=99.2099839;lon=16.5989169") is None, \
        "latitude out of range"
    assert parse_gps("lat=-99.2099839;lon=16.5989169") is None, \
        "latitude out of range"
    assert parse_gps("lat=49.2099839;lon=-196.5989169") is None, \
        "longitude out of range"
    assert parse_gps("lat=49.2099839;lon=196.5989169") is None, \
        "longitude out of range"
    assert parse_gps("text") is None, "invalid format"
    assert parse_gps("49.2099839;16.5989169") is None, "invalid format"
    assert parse_gps("lat=49.2099839 lon=16.5989169") is None, "invalid format"
    assert parse_gps("lon=16.5989169;lat=49.2099839") is None, "invalid format"
    assert parse_gps("lat=49;lon=16") is None, "invalid format"
    assert parse_gps("lat=49;2099839;lon=16;5989169") is None, "invalid format"
    assert parse_gps("lat=-49.2O99839;lon=16.5989l69") is None, \
        "invalid format"

    assert parse_gps_stream("""lat=49.2099839;lon=16.5989169
lat=48.1516986;lon=17.1093064
lat=50.0835494;lon=14.4341414""") \
        == [(49.2099839, 16.5989169),
            (48.1516986, 17.1093064),
            (50.0835494, 14.4341414)]

    assert parse_gps_stream("""lat=49.2099839;lon=16.5989169
lat=48.1516986;lon=-17.1093064
lat=-50.0835494;lon=14.4341414""") \
        == [(49.2099839, 16.5989169),
            (48.1516986, -17.1093064),
            (-50.0835494, 14.4341414)]

    assert parse_gps_stream("") == []

    assert parse_gps_stream("""lat=49.2099839;lon=16.5989169
lat=48.1516986;lon=-189.1093064
lat=-50.0835494;lon=14.4341414""") \
        is None

    assert parse_gps_stream("""lat=49.2099839;lon=16.5989169
lat=48.1516986;lon=17.1093064
invalid entry""") \
        is None


if __name__ == "__main__":
    main()
