# !/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
# mypy: ignore-errors
# pylint: skip-file

import hw4 as student
from math import isclose

def print_warehouse(warehouse: student.Warehouse) -> None:
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


def example_warehouse() -> student.Warehouse:
    wh = student.Warehouse()

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
    ws = student.Warehouse()
    ws.history = [student.Movement('rice', 1, 1, 'A'), student.Movement('rice', 1, 1, 'A'),
                  student.Movement('rice', 1, 1, 'A')]
    ws.inventory = {
      'rice': [student.Package(1, 1, '20000101'), student.Package(1, 1, '20000101'),
               student.Package(1, 1, '20000101')],
    }
    ws.remove_expired('20000102')

    ws = student.Warehouse()
    ws.history = [student.Movement('rice', 1, 1, 'A'), student.Movement('rice', 1, 1, 'B')]
    ws.inventory = {
      'rice': [student.Package(1, 1, '20000101'), student.Package(1, 1, '20000101')],
    }
    ws.best_suppliers()

    wh = student.Warehouse()
    wh.history = [student.Movement('rice', 1, 1, 'A'), student.Movement('rice', -1, 1, 'A')]
    wh.inventory = {
        'rice': [],
    }
    wh.average_prices()

    wh = student.Warehouse()
    wh.store('rice', 100, 17, '20220202', 'ACME Rice Ltd.')
    wh.store('corn', 70, 15, '20220315', 'UniCORN & co.')
    wh.store('rice', 200, 158, '20771023', 'RICE Unlimited.')
    wh.store('peas', 9774, 1, '20220921', 'G. P. a C.')
    wh.store('rice', 90, 14, '20220202', "Theorem's Rice")
    wh.store('peas', 64, 7, '20211101', 'Discount Peas')
    wh.store('rice', 42, 9, '20211111', 'ACME Rice Ltd.')
    wh.try_sell('peas', 64, 10, 'Pea Shop')
    assert len(wh.inventory['peas']) == 1.

    wh.history = [student.Movement('rice', 1, 1, 'A'), student.Movement('rice', -1, 1, 'A')]
    wh.inventory = {
        'rice': [],
    }
    assert "rice" not in wh.average_prices()

    wh.history = [student.Movement('rice', 2, 1, 'A'), student.Movement('rice', 2, 1, 'B')]
    wh.inventory = {
      'rice': [student.Package(2, 1, '20000101'), student.Package(2, 1, '20000101')],
    }
    assert wh.best_suppliers() == {'B', 'A'}

    wh = student.Warehouse()
    wh.store('rice', 100, 17, '20220202', 'ACME Rice Ltd.')
    wh.store('corn', 70, 15, '20220315', 'UniCORN & co.')
    wh.store('rice', 200, 158, '20771023', 'RICE Unlimited.')
    wh.store('peas', 9774, 1, '20220921', 'G. P. a C.')
    wh.store('rice', 90, 14, '20220202', "Theorem's Rice")
    wh.store('peas', 64, 7, '20211101', 'Discount Peas')
    wh.store('rice', 42, 9, '20211111', 'ACME Rice Ltd.')
    assert wh.try_sell('rice', 500, 9, 'Pear Shop')
    assert len(wh.inventory['rice']) == 3

    wh = student.Warehouse()
    wh.store('rice', 100, 17, '20220202', 'ACME Rice Ltd.')
    wh.store('corn', 70, 15, '20220315', 'UniCORN & co.')
    wh.store('rice', 200, 158, '20771023', 'RICE Unlimited.')
    wh.store('peas', 9774, 1, '20220921', 'G. P. a C.')
    wh.store('rice', 90, 14, '20220202', "Theorem's Rice")
    wh.store('peas', 64, 7, '20211101', 'Discount Peas')
    wh.store('rice', 42, 9, '20211111', 'ACME Rice Ltd.')
    assert wh.try_sell('rice', 500, 15, 'Pear Shop') == (232, 3338)


    wh = student.Warehouse()
    wh.store('rice', 100, 17, '20220202', 'ACME Rice Ltd.')
    wh.store('corn', 70, 15, '20220315', 'UniCORN & co.')
    wh.store('rice', 200, 158, '20771023', 'RICE Unlimited.')
    wh.store('peas', 9774, 1, '20220921', 'G. P. a C.')
    wh.store('rice', 90, 14, '20220202', "Theorem's Rice")
    wh.store('peas', 64, 7, '20211101', 'Discount Peas')
    wh.store('rice', 42, 9, '20211111', 'ACME Rice Ltd.')
    wh.try_sell('peas', 64, 10, 'Pea Shop')
    assert len(wh.history) == 8

    wh = student.Warehouse()
    wh.history = [student.Movement('rice', 1, 1, 'A'), student.Movement('rice', -1, 1, 'A')]
    wh.inventory = {'rice': []}
    assert wh.find_inconsistencies() == set()

    wh = student.Warehouse()
    wh.store('rice', 100, 17, '20220202', 'ACME Rice Ltd.')
    wh.store('corn', 70, 15, '20220315', 'UniCORN & co.')
    wh.store('rice', 200, 158, '20771023', 'RICE Unlimited.')
    wh.store('peas', 9774, 1, '20220921', 'G. P. a C.')
    wh.store('rice', 90, 14, '20220202', "Theorem's Rice")
    wh.store('peas', 64, 7, '20211101', 'Discount Peas')
    wh.store('rice', 42, 9, '20211111', 'ACME Rice Ltd.')
    assert wh.try_sell('rice', 500, 8, 'Pear Shop') == (0, 0)

    wh = student.Warehouse()
    wh.store('rice', 100, 17, '20220202', 'ACME Rice Ltd.')
    wh.store('corn', 70, 15, '20220315', 'UniCORN & co.')
    wh.store('rice', 200, 158, '20771023', 'RICE Unlimited.')
    wh.store('peas', 9774, 1, '20220921', 'G. P. a C.')
    wh.store('rice', 90, 14, '20220202', "Theorem's Rice")
    wh.store('peas', 64, 7, '20211101', 'Discount Peas')
    wh.store('rice', 42, 9, '20211111', 'ACME Rice Ltd.')
    assert wh.try_sell('rice', 500, 8, 'Pear Shop') == (0, 0)

    wh = student.Warehouse()
    wh.history = [student.Movement('rice', 1, 1, 'A'), student.Movement('rice', -1, 1, 'EXPIRED')]
    wh.inventory = {'rice': []}
    assert wh.best_suppliers() == {"A"}
    
def test7() -> None:
    wh = student.Warehouse()
    wh.inventory = {"rice": [student.Package(20,1,""), student.Package(20,100,"")]}
    wh.history = [student.Movement("rice", 20, 1, "a"), student.Movement("rice", 20, 100, "b")]
    assert wh.try_sell("rice", 26, 80, "c") == (26, 2006)
    assert wh.find_inconsistencies() == set()
    assert len(wh.history) == 4
    
def test8() -> None:
    wh = student.Warehouse()
    wh.inventory = {"rice": [student.Package(1,1,""), student.Package(1,2,""), student.Package(1,3,"")]}
    wh.history = [student.Movement("rice", 1, 1, "a"), student.Movement("rice", 1, 2, "b"), student.Movement("rice", 1, 3, "b")]
    assert wh.try_sell("rice", 2,  3, "c") == (2, 5)
    assert wh.find_inconsistencies() == set()
    assert len(wh.history) == 5
    
def test9() -> None:
    wh = student.Warehouse()
    wh.inventory = {"rice": [student.Package(100,1,""), student.Package(20,60,""), student.Package(10,50,"")]}
    wh.history = [student.Movement("rice", 100, 1, "a"), student.Movement("rice", 20, 60, "b"), student.Movement("rice", 10, 50, "b")]
    assert wh.try_sell("rice", 50,  40, "c") == (50, 1720)
    assert wh.find_inconsistencies() == set()
    assert len(wh.history) == 6
    
def test10() -> None:
    wh = student.Warehouse()
    wh.history = [student.Movement('rice', 1, 1, 'A'), student.Movement('rice', -1, 1, 'A')]
    wh.inventory = {}
    assert wh.best_suppliers() == {"A"}

def test11() -> None:
    wh = student.Warehouse()
    wh.history = [student.Movement('rice', 1, 1, 'A'), student.Movement('rice', 1, 1, 'A')]
    wh.inventory = {'rice': [student.Package(1, 1, '20000101'), student.Package(1, 1, '20000101')]}
    assert  wh.find_inconsistencies() == set()
    
def test12() -> None:
    wh = student.Warehouse()
    wh.store('rice', 100, 17, '20220202', 'ACME Rice Ltd.')
    wh.store('corn', 70, 15, '20220315', 'UniCORN & co.')
    wh.store('rice', 200, 158, '20771023', 'RICE Unlimited.')
    wh.store('peas', 9774, 1, '20220921', 'G. P. a C.')
    wh.store('rice', 90, 14, '20220202', "Theorem's Rice")
    wh.store('peas', 64, 7, '20211101', 'Discount Peas')
    wh.store('rice', 42, 9, '20211111', 'ACME Rice Ltd.')
    assert wh.try_sell('rice', 100, 9, 'Pear Shop') == (42, 378)
    
def test13() -> None:
    wh = student.Warehouse()
    wh.history = [student.Movement('rice', 5, 1, 'A'), student.Movement('rice', 1, 1, 'A'), student.Movement('rice', -3, 1, 'A')]
    wh.inventory = {'rice': [student.Package(1, 1, '20000101'), student.Package(2, 1, '20000101')]}
    assert  wh.find_inconsistencies() == set()
    
def test14() -> None:
    wh = student.Warehouse()
    wh.store('rice', 100, 17, '20220202', 'ACME Rice Ltd.')
    wh.store('corn', 70, 15, '20220315', 'UniCORN & co.')
    wh.store('rice', 200, 158, '20771023', 'RICE Unlimited.')
    wh.store('peas', 9774, 1, '20220921', 'G. P. a C.')
    wh.store('rice', 90, 14, '20220202', "Theorem's Rice")
    wh.store('peas', 64, 7, '20211101', 'Discount Peas')
    wh.store('rice', 42, 9, '20211111', 'ACME Rice Ltd.')
    assert wh.try_sell('soy', 1, 100, 'Soy Shop') == (0, 0)
    
def test15() -> None:
    wh = student.Warehouse()
    wh.history = [student.Movement('rice', 5, 1, 'A'), student.Movement('rice', 1, 1, 'A'), student.Movement('rice', -3, 1, 'A'), student.Movement('rice', 1, 1, 'A')]
    wh.inventory = {'rice': [student.Package(1, 1, '20000101'), student.Package(2, 1, '20000101'), student.Package(1, 1, '20000101')]}
    assert  wh.find_inconsistencies() == set()
    

def test16() -> None:
    wh = student.Warehouse()
    wh.inventory = {"rice": [student.Package(80 ,1,""), student.Package(20,100,""), student.Package(25,60,"")]}
    wh.history = [student.Movement("rice",80, 1, "a"), student.Movement("rice", 20, 100, "b"), student.Movement("rice", 25, 60, "b")]
    assert wh.try_sell("rice", 105 , 34, "c") == (105, 3560)
    assert wh.find_inconsistencies() == set()
    assert len(wh.history) == 6
    
def test17() -> None:
    wh = student.Warehouse()
    wh.history = [student.Movement('rice', 1, 1, 'A'), student.Movement('rice', -1, 1, 'EXPIRED'),
                  student.Movement('rice', 1, 1, 'A'), student.Movement('rice', 1, 1, 'A'),
                  student.Movement('rice', 1, 1, 'A'), student.Movement('rice', 1, 1, 'A')]
    wh.inventory = {'rice': [student.Package(1, 2, '20000101'), student.Package(1, 1, '20000101'),
                             student.Package(1, 1, '20000101'), student.Package(1, 1, '20000101')],}
    assert wh.find_inconsistencies() == {('rice', 1, -1), ('rice', 2, 1)}

def test18() -> None:
    wh = student.Warehouse()
    wh.history = [student.Movement('rice', 1, 1, 'A'), student.Movement('rice', -1, 1, 'EXPIRED'),
                  student.Movement('rice', 1, 1, 'A'), student.Movement('rice', 1, 1, 'A'),
                  student.Movement('rice', 1, 1, 'A'), student.Movement('rice', 1, 2, 'A'),
                  student.Movement('rice', 3, 4, 'A')]
    wh.inventory = {'rice': [student.Package(1, 2, '20000101'), student.Package(1, 1, '20000101'),
                             student.Package(1, 1, '20000101'), student.Package(1, 1, '20000101')],}
    assert wh.find_inconsistencies() == {('rice', 4, -3)}
    
def test19() -> None:
    wh = student.Warehouse()
    wh.history = [student.Movement('rice', 1, 1, 'A')]
    wh.inventory = {}
    assert wh.find_inconsistencies() == {('rice', 1, -1)}
    
def test20() -> None:
    wh = student.Warehouse()
    wh.history = []
    wh.inventory = {'rice': [student.Package(1, 1, '20000101')]}
    assert wh.find_inconsistencies() == {('rice', 1, 1)}
    
def test21() -> None:
    wh = student.Warehouse()
    wh.history = [student.Movement('rice', 1, 1, 'A'), student.Movement('rice', -1, 1, 'EXPIRED'),
                  student.Movement('rice', 1, 1, 'A'), student.Movement('rice', 1, 1, 'A'),
                  student.Movement('rice', 1, 1, 'A'), student.Movement('rice', 2, 1, 'A'),
                  student.Movement('rice', 3, 4, 'A')]
    wh.inventory = {}
    assert wh.find_inconsistencies() == {('rice', 1, -5), ('rice', 4, -3)}


def test22() -> None:
    wh = student.Warehouse()
    wh.history = []
    wh.inventory = {'rice': [student.Package(1, 2, '20000101'), student.Package(1, 1, '20000101'),
                             student.Package(1, 1, '20000101'), student.Package(1, 1, '20000101')],}
    assert wh.find_inconsistencies() == {('rice', 2, 1), ('rice', 1, 3)}
    
def test23() -> None:
    wh = student.Warehouse()
    wh.history = [student.Movement('rice', 1, 1, 'A'), student.Movement('rice', -1, 1, 'EXPIRED'),
                  student.Movement('rice', 1, 1, 'A'), student.Movement('rice', 1, 1, 'A'),
                  student.Movement('rice', 1, 1, 'A'), student.Movement('rice', 2, 1, 'A'),
                  student.Movement('rice', 3, 4, 'A'), student.Movement('rice', 6, 5, 'A')]
    wh.inventory = {}
    assert wh.find_inconsistencies() == {('rice', 1, -5), ('rice', 4, -3), ('rice', 5, -6)}
    
def test24() -> None:
    wh = student.Warehouse()
    wh.history = []
    wh.inventory = {'rice': [student.Package(1, 2, '20000101'), student.Package(1, 1, '20000101'),
                             student.Package(1, 1, '20000101'), student.Package(1, 1, '20000101'),
                             student.Package(5, 4, '20000101')]}
    assert wh.find_inconsistencies() == {('rice', 2, 1), ('rice', 1, 3), ('rice', 4, 5)}

def test25():
    wh = student.Warehouse()
    wh.history = [student.Movement('chickpeas', 34341129, 3054436383, 'A'), student.Movement('corn', 1287, 65794, 'A'),
                student.Movement('barley', 65796, 16843011, 'B'), student.Movement('soy', 16843039, 16843265, 'C'),
                student.Movement('potatoes', 65793, 16843009, 'D'), student.Movement('rice', 16843010, 16843268, 'B'),
                student.Movement('peas', 65796, 16842753, 'D'), student.Movement('peas', 27328770, 33620226, 'BC'),
                student.Movement('peas', 1, 4, 'D'), student.Movement('hops', 6, 257, 'A'),
                student.Movement('peas', 16777218, 50397698, 'D'), student.Movement('peas', 2, 50397442, 'G'),
                student.Movement('rice', 2, 516, 'C'), student.Movement('soy', 2, 182, 'K'),
                student.Movement('hops', 263169, 50397392, 'B'), student.Movement('hops', 151717380, 35218, 'P'),
                student.Movement('hops', 3842, 8925, 'B'), student.Movement('rice', 330, 2, 'S'),
                student.Movement('rice', 1, 16844036, 'U'), student.Movement('peas', 661762, 16843011, 'D'),
                student.Movement('corn', 2, 266, 'C'), student.Movement('peas', 770, 2, 'HC'),
                student.Movement('avocado', 1, 29998, 'BB'), student.Movement('rice', 2, 16842753, 'P'),
                student.Movement('peas', 7925, 257, 'B'), student.Movement('corn', 18481409, 258, 'C'),
                student.Movement('corn', 2, 259, 'e'), student.Movement('hops', 513, 471015340, 'BXq')]
    wh.inventory = {
      'chickpeas': [student.Package(34341129, 3054436383, '19990505')],
      'corn': [student.Package(18481409, 258, '22940105'), student.Package(2, 259, '20000201'), student.Package(2, 266, '19991001'), student.Package(1287, 65794, '19990204')],
      'barley': [student.Package(65796, 16843011, '20000101')],
      'soy': [student.Package(2, 182, '19990617'), student.Package(16843039, 16843265, '19990201')],
      'potatoes': [student.Package(65793, 16843009, '19930101')],
      'rice': [student.Package(330, 2, '27180511'), student.Package(1, 16844036, '19990923'), student.Package(16843010, 16843268, '19990301'), student.Package(2, 516, '19930104'), student.Package(2, 16842753, '19700204')],
      'peas': [student.Package(2, 50397442, '22570407'), student.Package(16777218, 50397698, '22570404'), student.Package(7925, 257, '22570107'), student.Package(770, 2, '19990501'), student.Package(27328770, 33620226, '19990204'), student.Package(65796, 16842753, '19990102'), student.Package(1, 4, '19980103'), student.Package(661762, 16843011, '19790101')],
      'hops': [student.Package(6, 257, '19990301'), student.Package(3842, 8925, '19990201'), student.Package(263169, 50397392, '19990108'), student.Package(513, 471015340, '19970101'), student.Package(151717380, 35218, '19960630')],
      'avocado': [student.Package(1, 29998, '19990301')],
  }
    assert wh.try_sell('corn', 2, 27476, 'x') == (0, 0)
    

    

if __name__ == '__main__':
    test1()
    print("----------------------------")
    test2()
    print("----------------------------")
    test3()
    print("----------------------------")
    test4()
    print("----------------------------")
    test5()
    print("----------------------------")
    test6()
    print("----------------------------")
    test7()
    print("----------------------------")
    test8()
    print("----------------------------")
    test9()
    print("----------------------------")
    test10()
    print("----------------------------")
    test11()
    print("----------------------------")
    test12()
    print("----------------------------")
    test13()
    print("----------------------------")
    test14()
    print("----------------------------")
    test15()
    print("----------------------------")
    test16()
    print("----------------------------")
    test17()
    print("----------------------------")
    test18()
    print("----------------------------")
    test19()
    print("----------------------------")
    test20()
    print("----------------------------")
    test21()
    print("----------------------------")
    test22()
    print("----------------------------")
    test23()
    print("----------------------------")
    test24()
    print("----------------------------")
    test25()
