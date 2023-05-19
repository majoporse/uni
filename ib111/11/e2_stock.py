from typing import Tuple


# Implementujte podprogram ‹stock_value›, který spočítá horní a
# dolní odhad průměrné hodnoty prodaných akcí v zadaném měsíci
# ‹month› roku ‹year›. Data o akciovém trhu podprogram dostane
# v souboru s cestou ‹path› ve formátu JSON.

# Informace o obchodování pro jednotlivé dny naleznete v objektu
# (slovníku) ‹days›. Nás budou pro výpočet zajímat položky ‹low› a
# ‹high›, které dávají nejnižší a nejvyšší hodnotu akcí pro daný
# den, a položka ‹volume›, která udává počet prodaných akcí. Data
# vypadají takto (rozsáhlejší příklad naleznete v souboru
# ‹zz.stock.json›):

#     {
#       "days": {
#         "2020-11-18": {
#             "open": 227.4000, "close": 233.2000,
#             "low": 225.7000, "high": 233.8000,
#             "volume": 39543200
#         },
#         "2020-11-17": {
#             "open": 225.0000, "close": 228.6000,
#             "low": 224.8000, "high": 228.9000,
#             "volume": 23420151
#         }
#       }
#     }

# Spodní odhad získáte jako vážený průměr hodnoty ‹low› přes
# jednotlivé dny (váhou je objem, ‹volume›, obchodu v daný den).
# Analogicky horní odhad (použijete hodnotu ‹high›).

# V tomto příkladu můžete použít standardní knihovny: ‹datetime›,
# ‹calendar›, ‹statistics›, ‹math› a ‹json›.


def stock_value(path: str, year: int, month: int) \
        -> Tuple[float, float]:
    pass


def main() -> None:
    check_stock(2020, 5, 231.32, 238.42)
    check_stock(2008, 2, 397.02, 408.60)
    check_stock(2014, 1, 324.18, 331.49)
    check_stock(2010, 6, 392.48, 401.64)
    check_stock(2005, 7, 314.77, 320.00)
    check_stock(2011, 11, 393.77, 401.94)


def check_stock(year: int, month: int,
                expect_low: float, expect_high: float) -> None:
    low, high = stock_value('zz.stock.json', year, month)
    assert round(100 * low) == round(100 * expect_low)
    assert round(100 * high) == round(100 * expect_high)


if __name__ == "__main__":
    main()
