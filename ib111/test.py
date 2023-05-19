# !/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
# mypy: ignore-errors
# pylint: skip-file

from  hw4 import Warehouse, Package, Movement
from math import isclose


def print_warehouse(warehouse: Warehouse) -> None:
    print("===== INVENTORY =====", end="")
    for item, pkgs in warehouse.inventory.items():
        print(f"\n* Item: {item}")
        print("    amount  price  expiration date")
        print("  ---------------------------------")
        for pkg in pkgs:
            print(f"     {pkg.amount:4d}   {pkg.price:4d}     {pkg.expiry}")
    print("\n===== HISTORY ======")
    print("    item     amount  price   tag")
    print("-------------------------------------------")
    for mov in warehouse.history:
        print(f" {mov.item:^11}   {mov.amount:4d}   "
              f"{mov.price:4d}   {mov.tag}")


def example_warehouse() -> Warehouse:
    wh = Warehouse()

    wh.store("rice", 100, 17, "20220202", "ACME Rice Ltd.")
    wh.store("corn", 70, 15, "20220315", "UniCORN & co.")
    wh.store("rice", 200, 158, "20771023", "RICE Unlimited")
    wh.store("peas", 9774, 1, "20220921", "G. P. a C.")
    wh.store("rice", 90, 14, "20220202", "Theorem's Rice")
    wh.store("peas", 64, 7, "20211101", "Discount Peas")
    wh.store("rice", 42, 9, "20211111", "ACME Rice Ltd.")

    return wh


def test1() -> None:
    wh = example_warehouse()

    for item, length in ('rice', 4), ('peas', 2), ('corn', 1):
        assert item in wh.inventory
        assert len(wh.inventory[item]) == length

    assert len(wh.history) == 7

    # uncomment to visually check the output:
    print_warehouse(wh)


def test2() -> None:
    wh = example_warehouse()
    assert wh.find_inconsistencies() == set()

    wh.inventory['peas'][0].amount = 9773
    wh.history[4].price = 12

    assert wh.find_inconsistencies() == {
        ('peas', 1, -1),
        ('rice', 14, 90),
        ('rice', 12, -90),
    }


def test3() -> None:
    wh = example_warehouse()
    bad_peas = wh.inventory['peas'][-1]
    assert wh.remove_expired('20211111') == [bad_peas]
    assert len(wh.history) == 8

    mov = wh.history[-1]
    assert mov.item == 'peas'
    assert mov.amount == -64
    assert mov.price == 7
    assert mov.tag == 'EXPIRED'

    assert len(wh.inventory['peas']) == 1


def test4() -> None:
    wh = example_warehouse()
    assert wh.try_sell('rice', 500, 9, 'Pear Shop') == (42, 42 * 9)
    assert len(wh.history) == 8
    assert wh.find_inconsistencies() == set()

    wh = example_warehouse()
    assert wh.try_sell('rice', 500, 12, 'Pear Shop') \
        == (42 + 25, 42 * 9 + 25 * 17)
    assert len(wh.history) == 9
    assert wh.find_inconsistencies() == set()

    wh = example_warehouse()
    assert wh.try_sell('rice', 500, 14, 'Pear Shop') \
           == (42 + 70, 42 * 9 + 70 * 17)
    assert len(wh.history) == 9
    assert wh.find_inconsistencies() == set()

    wh = example_warehouse()
    assert wh.try_sell('rice', 500, 15, 'Pear Shop')\
           == (42 + 100 + 90, 42 * 9 + 100 * 17 + 90 * 14)
    assert len(wh.history) == 10
    assert wh.find_inconsistencies() == set()

    wh = example_warehouse()
    assert wh.try_sell('rice', 500, 16, 'Pear Shop') \
        == (42 + 100 + 90 + 2, 42 * 9 + 100 * 17 + 90 * 14 + 2 * 158)
    assert len(wh.history) == 11
    assert wh.find_inconsistencies() == set()

    # uncomment to visually check the output:
    print_warehouse(wh)

    wh = example_warehouse()
    assert wh.try_sell('rice', 500, 81, 'Pear Shop') \
        == (42 + 100 + 90 + 200, 42 * 9 + 100 * 17 + 90 * 14 + 200 * 158)
    assert len(wh.history) == 11
    assert wh.find_inconsistencies() == set()


def test5() -> None:
    wh = example_warehouse()

    expected = {
        'rice': 80.875,
        'corn': 15,
        'peas': (9774 + 64 * 7) / (9774 + 64),
    }

    avg_prices = wh.average_prices()

    assert expected.keys() == avg_prices.keys()

    for item in avg_prices:
        assert isclose(avg_prices[item], expected[item])

    assert wh.best_suppliers() \
        == {'UniCORN & co.', 'G. P. a C.', 'RICE Unlimited'}


def test6() -> None:
    ws = Warehouse()
    ws.history = [Movement('rice', 1, 1, 'A'), Movement('rice', 1, 1, 'A'),
                  Movement('rice', 1, 1, 'A')]
    ws.inventory = {
      'rice': [Package(1, 1, '20000101'), Package(1, 1, '20000101'),
               Package(1, 1, '20000101')],
    }
    ws.remove_expired('20000102')

    ws = Warehouse()
    ws.history = [Movement('rice', 1, 1, 'A'), Movement('rice', 1, 1, 'B')]
    ws.inventory = {
      'rice': [Package(1, 1, '20000101'), Package(1, 1, '20000101')],
    }
    ws.best_suppliers()

    wh = Warehouse()
    wh.history = [Movement('rice', 1, 1, 'A'), Movement('rice', -1, 1, 'A')]
    wh.inventory = {
        'rice': [],
    }
    wh.average_prices()

    wh = Warehouse()
    wh.store('rice', 100, 17, '20220202', 'ACME Rice Ltd.')
    wh.store('corn', 70, 15, '20220315', 'UniCORN & co.')
    wh.store('rice', 200, 158, '20771023', 'RICE Unlimited.')
    wh.store('peas', 9774, 1, '20220921', 'G. P. a C.')
    wh.store('rice', 90, 14, '20220202', "Theorem's Rice")
    wh.store('peas', 64, 7, '20211101', 'Discount Peas')
    wh.store('rice', 42, 9, '20211111', 'ACME Rice Ltd.')
    wh.try_sell('peas', 64, 10, 'Pea Shop')
    assert len(wh.inventory['peas']) == 1.

    wh.history = [Movement('rice', 1, 1, 'A'), Movement('rice', -1, 1, 'A')]
    wh.inventory = {
        'rice': [],
    }
    assert "rice" not in wh.average_prices()

    wh.history = [Movement('rice', 2, 1, 'A'), Movement('rice', 2, 1, 'B')]
    wh.inventory = {
      'rice': [Package(2, 1, '20000101'), Package(2, 1, '20000101')],
    }
    assert wh.best_suppliers() == {'B', 'A'}

    wh = Warehouse()
    wh.store('rice', 100, 17, '20220202', 'ACME Rice Ltd.')
    wh.store('corn', 70, 15, '20220315', 'UniCORN & co.')
    wh.store('rice', 200, 158, '20771023', 'RICE Unlimited.')
    wh.store('peas', 9774, 1, '20220921', 'G. P. a C.')
    wh.store('rice', 90, 14, '20220202', "Theorem's Rice")
    wh.store('peas', 64, 7, '20211101', 'Discount Peas')
    wh.store('rice', 42, 9, '20211111', 'ACME Rice Ltd.')
    assert wh.try_sell('rice', 500, 9, 'Pear Shop')
    assert len(wh.inventory['rice']) == 3

    wh = Warehouse()
    wh.store('rice', 100, 17, '20220202', 'ACME Rice Ltd.')
    wh.store('corn', 70, 15, '20220315', 'UniCORN & co.')
    wh.store('rice', 200, 158, '20771023', 'RICE Unlimited.')
    wh.store('peas', 9774, 1, '20220921', 'G. P. a C.')
    wh.store('rice', 90, 14, '20220202', "Theorem's Rice")
    wh.store('peas', 64, 7, '20211101', 'Discount Peas')
    wh.store('rice', 42, 9, '20211111', 'ACME Rice Ltd.')
    assert wh.try_sell('rice', 500, 15, 'Pear Shop') == (232, 3338)


    wh = Warehouse()
    wh.store('rice', 100, 17, '20220202', 'ACME Rice Ltd.')
    wh.store('corn', 70, 15, '20220315', 'UniCORN & co.')
    wh.store('rice', 200, 158, '20771023', 'RICE Unlimited.')
    wh.store('peas', 9774, 1, '20220921', 'G. P. a C.')
    wh.store('rice', 90, 14, '20220202', "Theorem's Rice")
    wh.store('peas', 64, 7, '20211101', 'Discount Peas')
    wh.store('rice', 42, 9, '20211111', 'ACME Rice Ltd.')
    wh.try_sell('peas', 64, 10, 'Pea Shop')
    assert len(wh.history) == 8

    wh = Warehouse()
    wh.history = [Movement('rice', 1, 1, 'A'), Movement('rice', -1, 1, 'A')]
    wh.inventory = {'rice': []}
    assert wh.find_inconsistencies() == set()

    wh = Warehouse()
    wh.store('rice', 100, 17, '20220202', 'ACME Rice Ltd.')
    wh.store('corn', 70, 15, '20220315', 'UniCORN & co.')
    wh.store('rice', 200, 158, '20771023', 'RICE Unlimited.')
    wh.store('peas', 9774, 1, '20220921', 'G. P. a C.')
    wh.store('rice', 90, 14, '20220202', "Theorem's Rice")
    wh.store('peas', 64, 7, '20211101', 'Discount Peas')
    wh.store('rice', 42, 9, '20211111', 'ACME Rice Ltd.')
    assert wh.try_sell('rice', 500, 8, 'Pear Shop') == (0, 0)

    wh = Warehouse()
    wh.store('rice', 100, 17, '20220202', 'ACME Rice Ltd.')
    wh.store('corn', 70, 15, '20220315', 'UniCORN & co.')
    wh.store('rice', 200, 158, '20771023', 'RICE Unlimited.')
    wh.store('peas', 9774, 1, '20220921', 'G. P. a C.')
    wh.store('rice', 90, 14, '20220202', "Theorem's Rice")
    wh.store('peas', 64, 7, '20211101', 'Discount Peas')
    wh.store('rice', 42, 9, '20211111', 'ACME Rice Ltd.')
    assert wh.try_sell('rice', 500, 8, 'Pear Shop') == (0, 0)

    wh = Warehouse()
    wh.history = [Movement('rice', 1, 1, 'A'), Movement('rice', -1, 1, 'EXPIRED')]
    wh.inventory = {'rice': []}
    assert wh.best_suppliers() == {"A"}

    wh = Warehouse()
    wh.inventory = {"rice": [Package(20,1,""), Package(20,100,"")]}
    wh.history = [Movement("rice", 20, 1, "a"), Movement("rice", 20, 100, "b")]
    assert wh.try_sell("rice", 26, 80, "c") == (26, 2006)
    assert wh.find_inconsistencies() == set()
    assert len(wh.history) == 4

    wh = Warehouse()
    wh.store('rice', 100, 17, '20220202', 'ACME Rice Ltd.')
    wh.store('corn', 70, 15, '20220315', 'UniCORN & co.')
    wh.store('rice', 200, 158, '20771023', 'RICE Unlimited.')
    wh.store('peas', 9774, 1, '20220921', 'G. P. a C.')
    wh.store('rice', 90, 14, '20220202', "Theorem's Rice")
    wh.store('peas', 64, 7, '20211101', 'Discount Peas')
    wh.store('rice', 42, 9, '20211111', 'ACME Rice Ltd.')
    wh.try_sell('soy', 1, 100, 'Soy Shop')

    wh = Warehouse()
    wh.history = [Movement('rice', 1, 1, 'A'), Movement('rice', -1, 1, 'A')]
    wh.inventory = {}
    assert wh.best_suppliers() == {"A"}

    wh = Warehouse()
    wh.history = [Movement('rice', 1, 1, 'A'), Movement('rice', 1, 1, 'A')]
    wh.inventory = {'rice': [Package(1, 1, '20000101'), Package(1, 1, '20000101')]}
    assert  wh.find_inconsistencies() == set()

    wh = Warehouse()
    wh.store('rice', 100, 17, '20220202', 'ACME Rice Ltd.')
    wh.store('corn', 70, 15, '20220315', 'UniCORN & co.')
    wh.store('rice', 200, 158, '20771023', 'RICE Unlimited.')
    wh.store('peas', 9774, 1, '20220921', 'G. P. a C.')
    wh.store('rice', 90, 14, '20220202', "Theorem's Rice")
    wh.store('peas', 64, 7, '20211101', 'Discount Peas')
    wh.store('rice', 42, 9, '20211111', 'ACME Rice Ltd.')
    assert wh.try_sell('rice', 100, 9, 'Pear Shop') == (42, 378)

    wh = Warehouse()
    wh.history = [Movement('rice', 5, 1, 'A'), Movement('rice', 1, 1, 'A'), Movement('rice', -3, 1, 'A')]
    wh.inventory = {'rice': [Package(1, 1, '20000101'), Package(2, 1, '20000101')]}
    assert  wh.find_inconsistencies() == set()

    wh = Warehouse()
    wh.inventory = {"rice": [Package(80 ,1,""), Package(20,100,""), Package(25,60,"")]}
    wh.history = [Movement("rice",80, 1, "a"), Movement("rice", 20, 100, "b"), Movement("rice", 25, 60, "b")]
    assert wh.try_sell("rice", 105 , 34, "c") == (105, 3560)
    assert wh.find_inconsistencies() == set()
    assert len(wh.history) == 6

    wh = Warehouse()
    wh.history = [Movement('rice', 1, 1, 'A'), Movement('rice', -1, 1, 'EXPIRED'),
                  Movement('rice', 1, 1, 'A'), Movement('rice', 1, 1, 'A'),
                  Movement('rice', 1, 1, 'A'), Movement('rice', 1, 1, 'A')]
    wh.inventory = {'rice': [Package(1, 2, '20000101'), Package(1, 1, '20000101'),
                             Package(1, 1, '20000101'), Package(1, 1, '20000101')],}
    assert wh.find_inconsistencies() == {('rice', 1, -1), ('rice', 2, 1)}

def test7():
    wh = Warehouse()
    wh.history = [Movement('chickpeas', 34341129, 3054436383, 'A'), Movement('corn', 1287, 65794, 'A'),
                Movement('barley', 65796, 16843011, 'B'), Movement('soy', 16843039, 16843265, 'C'),
                Movement('potatoes', 65793, 16843009, 'D'), Movement('rice', 16843010, 16843268, 'B'),
                Movement('peas', 65796, 16842753, 'D'), Movement('peas', 27328770, 33620226, 'BC'),
                Movement('peas', 1, 4, 'D'), Movement('hops', 6, 257, 'A'),
                Movement('peas', 16777218, 50397698, 'D'), Movement('peas', 2, 50397442, 'G'),
                Movement('rice', 2, 516, 'C'), Movement('soy', 2, 182, 'K'),
                Movement('hops', 263169, 50397392, 'B'), Movement('hops', 151717380, 35218, 'P'),
                Movement('hops', 3842, 8925, 'B'), Movement('rice', 330, 2, 'S'),
                Movement('rice', 1, 16844036, 'U'), Movement('peas', 661762, 16843011, 'D'),
                Movement('corn', 2, 266, 'C'), Movement('peas', 770, 2, 'HC'),
                Movement('avocado', 1, 29998, 'BB'), Movement('rice', 2, 16842753, 'P'),
                Movement('peas', 7925, 257, 'B'), Movement('corn', 18481409, 258, 'C'),
                Movement('corn', 2, 259, 'e'), Movement('hops', 513, 471015340, 'BXq')]
    wh.inventory = {
      'chickpeas': [Package(34341129, 3054436383, '19990505')],
      'corn': [Package(18481409, 258, '22940105'), Package(2, 259, '20000201'), Package(2, 266, '19991001'), Package(1287, 65794, '19990204')],
      'barley': [Package(65796, 16843011, '20000101')],
      'soy': [Package(2, 182, '19990617'), Package(16843039, 16843265, '19990201')],
      'potatoes': [Package(65793, 16843009, '19930101')],
      'rice': [Package(330, 2, '27180511'), Package(1, 16844036, '19990923'), Package(16843010, 16843268, '19990301'), Package(2, 516, '19930104'), Package(2, 16842753, '19700204')],
      'peas': [Package(2, 50397442, '22570407'), Package(16777218, 50397698, '22570404'), Package(7925, 257, '22570107'), Package(770, 2, '19990501'), Package(27328770, 33620226, '19990204'), Package(65796, 16842753, '19990102'), Package(1, 4, '19980103'), Package(661762, 16843011, '19790101')],
      'hops': [Package(6, 257, '19990301'), Package(3842, 8925, '19990201'), Package(263169, 50397392, '19990108'), Package(513, 471015340, '19970101'), Package(151717380, 35218, '19960630')],
      'avocado': [Package(1, 29998, '19990301')],
  }
    assert wh.try_sell('corn', 2, 27476, 'x') == (0, 0)

def test8():
    wh = Warehouse()
    wh.history = [Movement('corn', 102171, 16843010, 'A'), Movement('wheat', 16843014, 16843040, 'A'),
                Movement('bananas', 19792133, 33554689, 'B'), Movement('chickpeas', 268505602, 262, 'B'),
                Movement('bananas', 19136774, 167837953, 'DQA'), Movement('wheat', 32659, 50053, 'D'),
                Movement('peas', 41329, 513, 'C'), Movement('rice', 4, 1, 'AB'),
                Movement('rice', 21890053, 50399234, 'C'), Movement('rice', 5, 524, 'C'),
                Movement('rice', 2, 3, 'C'), Movement('peas', 26881, 3, 'C'),
                Movement('peas', 2709670634, 283, 'CO'), Movement('peas', 16843523, 682603524, 'D'),
                Movement('corn', 2199257603, 16843782, 'E'), Movement('soy', 117506571, 2, 'E'),
                Movement('avocado', 2, 6, 'G'), Movement('hops', 272, 264, 'H'),
                Movement('hops', 6, 17675, 'a'), Movement('hops', 42314, 4158802438, 'l'),
                Movement('barley', 2, 27730322, 'm'), Movement('peas', 1, 2, 'r'),
                Movement('barley', 5, 117506306, 's'), Movement('potatoes', 2, 16849410, 't'),
                Movement('wheat', 63, 1, 'u'), Movement('chickpeas', 151, 35073, 'v'),
                Movement('rice', 47709, 62400, 'x'), Movement('soy', 504377107, 34213, 'z')]
    wh.inventory = {
      'corn': [Package(102171, 16843010, '22570203'), Package(2199257603, 16843782, '19990301')],
      'wheat': [Package(16843014, 16843040, '22570212'), Package(32659, 50053, '20000102'), Package(63, 1, '19890205')],
      'bananas': [Package(19792133, 33554689, '22570521'), Package(19136774, 167837953, '19990202')],
      'chickpeas': [Package(268505602, 262, '22570102'), Package(151, 35073, '19760221')],
      'peas': [Package(41329, 513, '20300202'), Package(16843523, 682603524, '19990206'), Package(2709670634, 283, '19990203'), Package(26881, 3, '19990202'), Package(1, 2, '19971212')],
      'rice': [Package(4, 1, '22570402'), Package(2, 3, '20000426'), Package(5, 524, '20000207'), Package(21890053, 50399234, '19990201'), Package(47709, 62400, '19690102')],
      'soy': [Package(117506571, 2, '19990307'), Package(504377107, 34213, '19061113')],
      'avocado': [Package(2, 6, '19990404')],
      'hops': [Package(6, 17675, '84630312'), Package(42314, 4158802438, '19991214'), Package(272, 264, '19990928')],
      'barley': [Package(2, 27730322, '19990101'), Package(5, 117506306, '19960101')],
      'potatoes': [Package(2, 16849410, '19960102')],
  }
    x = wh.try_sell('peas', 51937, 3, 'z')
    assert x == (26882, 80645)


if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
    test8()
