from datetime import date
import json
import datetime

# Implementujte podprogram ‹coldest_day›, který najde nejchladnější
# den pro město ‹city› v předpovědi počasí uložené v souboru ‹path›
# ve formátu JSON. Data předpovědi jsou získaná ze serveru
# ‹openweathermap.org›. Soubor obsahuje několik záznamů počasí pro
# různá města: jméno města naleznete v atributu ‹name› objektu
# ‹city›. Můžete předpokládat, že hledaný záznam se v souboru
# nachází.
#
# Dále nás ze záznamu bude zajímat samotná předpověď počasí pro
# jednotlivé dny. Ta se nachází v seznamu ‹list›, kterého každý
# prvek obsahuje atributy:
#
#  • ‹dt› je datum ve formátu „unix time stamp“, tzn. v počtu vteřin
#    od půlnoci 1.1.1970 v zóně UTC (pro konverzi do typu ‹date›
#    naleznete v knihovně ‹datetime› vhodnou funkci),
#  • seznam ‹temp› obsahuje naměřené teploty, konkrétně atribut
#    ‹min› obsahuje tu nejnižší z daného dne.
#
# Relevantní část jednoho záznamu na vstupu vypadá takto (vstup jako
# celek je seznam takových záznamů, a každý záznam obsahuje řadu
# dalších informací):
#
#     { "city": { "name": "Brno" },
#       "list": [ { "dt": 1605693600, "temp": { "min": 5.23 } },
#                 { "dt": 1605780000, "temp": { "min": 4.81 } } ] }
#
# V tomto úkolu máte povoleno použít knihovny ‹datetime› a ‹json›.

def coldest_day(path: str, city: str) -> date:
    with open(path) as file:
        josn_file = json.load(file)
        for city_dict in json_file:
            if city_dict["city"]["name"] == city:
                result = 0
                min_temp = None
                for day in city_dict:
                    if day["temp"]["min"] < min_temp:
                        min_temp = day["temp"]["min"]
                        result = day["dt"]
    return date.fromtimestamp(result)


def main() -> None:
    check_coldest("Brno", 2020, 11, 22)
    check_coldest("Praha", 2020, 11, 21)
    check_coldest("Bratislava", 2020, 11, 18)
    check_coldest("London", 2020, 11, 30)
    check_coldest("Paris", 2020, 11, 21)


def check_coldest(city: str, year: int, month: int, day: int) -> None:
    assert coldest_day("zz.weather.json", city) == date(year, month, day)


if __name__ == "__main__":
    main()
