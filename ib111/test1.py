# !/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
# mypy: ignore-errors
# pylint: skip-file

from unittest import TestCase
from hw4 import Warehouse, Movement, Package
from unittest import main


class TestWarehouse(TestCase):
    @staticmethod
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

    def test_store(self) -> None:
        wh = TestWarehouse.example_warehouse()

        for item_tst, length in ('rice', 4), ('peas', 2), ('corn', 1):
            self.assertIn(item_tst, wh.inventory)
            self.assertEqual(len(wh.inventory[item_tst]), length)

        self.assertEqual(len(wh.history), 7)

    def test_find_inconsistencies(self) -> None:
        wh = TestWarehouse.example_warehouse()
        self.assertSetEqual(wh.find_inconsistencies(), set())

        wh.inventory['peas'][0].amount = 9773
        wh.history[4].price = 12

        self.assertSetEqual(wh.find_inconsistencies(), {
            ('peas', 1, -1),
            ('rice', 14, 90),
            ('rice', 12, -90),
        })

    def test_remove_expired_1(self) -> None:
        wh = TestWarehouse.example_warehouse()
        bad_peas = wh.inventory['peas'][-1]
        self.assertListEqual(wh.remove_expired('20211111'), [bad_peas])
        self.assertEqual(len(wh.history), 8)

        mov = wh.history[-1]
        self.assertEqual(mov.item, 'peas')
        self.assertEqual(mov.amount, -64)
        self.assertEqual(mov.price, 7)
        self.assertEqual(mov.tag, 'EXPIRED')

        self.assertEqual(len(wh.inventory['peas']), 1)
        self.assertSetEqual(wh.find_inconsistencies(), set())

        wh = Warehouse()

        wh.history = [Movement('rice', 1, 1, 'A'),
                      Movement('rice', -1, 1, 'A')]
        wh.inventory = {
            'rice': [],
        }

        self.assertListEqual(wh.remove_expired('20000101'), [])
        self.assertSetEqual(wh.find_inconsistencies(), set())

    def test_remove_expired_2(self) -> None:
        wh = Warehouse()

        wh.history = [Movement('rice', 1, 1, 'A'), Movement('rice', 1, 1, 'A')]
        wh.inventory = \
            {'rice': [Package(1, 1, '20000101'), Package(1, 1, '20000101')]}

        self.assertListEqual(wh.remove_expired('20000101'), [])
        self.assertSetEqual(wh.find_inconsistencies(), set())

        wh = TestWarehouse.example_warehouse()
        self.assertEqual(len(wh.remove_expired('20880101')), 7)
        self.assertSetEqual(wh.find_inconsistencies(), set())

        wh = TestWarehouse.example_warehouse()
        self.assertEqual(len(wh.remove_expired('20771023')), 6)
        self.assertSetEqual(wh.find_inconsistencies(), set())

    def test_try_sell_1(self) -> None:
        wh = TestWarehouse.example_warehouse()
        self.assertTupleEqual(wh.try_sell('rice', 500, 9, 'Pear Shop'),
                              (42, 42 * 9))
        self.assertEqual(len(wh.history), 8)
        self.assertSetEqual(wh.find_inconsistencies(), set())

        wh = TestWarehouse.example_warehouse()
        self.assertTupleEqual(wh.try_sell('rice', 500, 12, 'Pear Shop'),
                              (42 + 25, 42 * 9 + 25 * 17))
        self.assertEqual(len(wh.history), 9)
        self.assertSetEqual(wh.find_inconsistencies(), set())

        wh = TestWarehouse.example_warehouse()
        self.assertTupleEqual(wh.try_sell('rice', 500, 14, 'Pear Shop'),
                              (42 + 70, 42 * 9 + 70 * 17))
        self.assertEqual(len(wh.history), 9)
        self.assertSetEqual(wh.find_inconsistencies(), set())

        wh = TestWarehouse.example_warehouse()
        self.assertTupleEqual(wh.try_sell('rice', 500, 15, 'Pear Shop'),
                              (42 + 100 + 90, 42 * 9 + 100 * 17 + 90 * 14))
        self.assertEqual(len(wh.history), 10)
        self.assertSetEqual(wh.find_inconsistencies(), set())

        wh = TestWarehouse.example_warehouse()
        self.assertTupleEqual(wh.try_sell('rice', 500, 16, 'Pear Shop'),
                              (42 + 100 + 90 + 2, 42 * 9 +
                               100 * 17 + 90 * 14 + 2 * 158))
        self.assertEqual(len(wh.history), 11)
        self.assertSetEqual(wh.find_inconsistencies(), set())

        wh = TestWarehouse.example_warehouse()
        self.assertTupleEqual(wh.try_sell('rice', 500, 81, 'Pear Shop'),
                              (42 + 100 + 90 + 200, 42 * 9 + 100 * 17 +
                               90 * 14 + 200 * 158))
        self.assertEqual(len(wh.history), 11)
        self.assertSetEqual(wh.find_inconsistencies(), set())

    def test_try_sell_2(self) -> None:
        wh = Warehouse()

        wh.history = [Movement('chickpeas', 259, 66562, 'A'),
                      Movement('corn', 258, 1, 'A'),
                      Movement('potatoes', 258, 1, 'A'),
                      Movement('peas', 16844290, 16843778, 'C'),
                      Movement('rice', 258, 258, 'BB'),
                      Movement('peas', 770, 1, 'B'),
                      Movement('peas', 65794, 258, 'BBC'),
                      Movement('corn', 16843010, 50397185, 'C'),
                      Movement('peas', 16974084, 65794, 'B'),
                      Movement('peas', 1, 2, 'C'),
                      Movement('barley', 100860007, 3164012802, 'C'),
                      Movement('peas', 2, 258, 'C'),
                      Movement('peas', 16843009, 2, 'D'),
                      Movement('peas', 1, 5, 'BC'),
                      Movement('barley', 2, 1797, 'e'),
                      Movement('rice', 2562, 2, 'Fu')]
        wh.inventory = {
            'chickpeas': [Package(259, 66562, '19990202')],
            'corn': [Package(258, 1, '22570101'),
                     Package(16843010, 50397185, '19990203')],
            'potatoes': [Package(258, 1, '19990101')],
            'peas': [Package(16974084, 65794, '20000104'),
                     Package(16843009, 2, '20000102'),
                     Package(16844290, 16843778, '20000102'),
                     Package(65794, 258, '19990201'),
                     Package(770, 1, '19990102'),
                     Package(2, 258, '19970102'), Package(1, 5, '19940203'),
                     Package(1, 2, '19041012')],
            'rice': [Package(258, 258, '19990301'),
                     Package(2562, 2, '19990211')],
            'barley': [Package(2, 1797, '19990306'),
                       Package(100860007, 3164012802, '19980204')],
        }

        self.assertTupleEqual(wh.try_sell('peas', 33753867, 8405601, 'z'),
                              (33753867, 283721531989783))
        self.assertTupleEqual(wh.try_sell('pudding', 100, 1, 'None'), (0, 0))

    def test_try_sell_3(self) -> None:
        wh = Warehouse()

        wh.history = [
            Movement('kebab', 1000, 1, 'I'),
            Movement('kebab', 20, 30, 'Need'),
            Movement('kebab', 20, 20, 'Sleep'),
        ]
        wh.inventory = {
            'kebab': [Package(20, 20, '11111111'),
                      Package(20, 30, '11111111'),
                      Package(1000, 1, '11111111')],
        }

        self.assertTupleEqual(wh.try_sell("kebab", 25, 24, "Me"), (25, 25))
        self.assertEqual(len(wh.history), 4)
        self.assertSetEqual(wh.find_inconsistencies(), set())

    def test_try_sell_4(self) -> None:
        wh = Warehouse()

        wh.history = [
            Movement('kebab', 1000, 1, 'What'),
            Movement('kebab', 20, 30, 'Is'),
            Movement('kebab', 20, 20, 'This'),
        ]
        wh.inventory = {
            'kebab': [Package(1000, 1, '11111111'),
                      Package(20, 30, '11111111'),
                      Package(20, 20, '11111111')],
        }

        self.assertTupleEqual(wh.try_sell("kebab", 45, 24, "Me"), (45, 1005))
        self.assertEqual(len(wh.history), 6)
        self.assertSetEqual(wh.find_inconsistencies(), set())

    def test_try_sell_5(self) -> None:
        wh = Warehouse()

        wh.history = [
            Movement('kebab', 1000, 1, 'I'),
            Movement('kebab', 20, 30, 'Am'),
            Movement('kebab', 20, 20, 'Hungry'),
        ]
        wh.inventory = {
            'kebab': [Package(1000, 1, '11111111'),
                      Package(20, 30, '11111111'),
                      Package(20, 20, '11111111')]
        }

        self.assertTupleEqual(wh.try_sell("kebab", 45, 21, "Me"), (22, 460))
        self.assertEqual(len(wh.history), 5)
        self.assertSetEqual(wh.find_inconsistencies(), set())

    def test_try_sell_6(self) -> None:
        wh = Warehouse()

        wh.history = [
            Movement('kebab', 1000, 1, 'Im'),
            Movement('kebab', 20, 100, 'Going'),
            Movement('kebab', 20, 20, 'Insane'),
        ]
        wh.inventory = {
            'kebab': [Package(1000, 1, '11111111'),
                      Package(20, 100, '11111111'),
                      Package(20, 20, '11111111')]
        }

        self.assertTupleEqual(wh.try_sell("kebab", 200, 21, "Me"), (200, 2560))
        self.assertEqual(len(wh.history), 6)
        self.assertSetEqual(wh.find_inconsistencies(), set())

    def test_try_sell_7(self) -> None:
        wh = Warehouse()

        wh.history = [
            Movement('kebab', 50, 1, 'Young'),
            Movement('kebab', 20, 100, 'Heretics'),
        ]
        wh.inventory = {
            'kebab': [Package(50, 1, '11111111'),
                      Package(20, 100, '11111111')]
        }

        self.assertTupleEqual(wh.try_sell("kebab", 100, 41, ""), (70, 2050))
        if 'kebab' in wh.inventory:
            self.assertListEqual(wh.inventory['kebab'], [])
        self.assertEqual(len(wh.history), 4)
        self.assertSetEqual(wh.find_inconsistencies(), set())

    def test_try_sell_8(self) -> None:
        wh = Warehouse()

        wh.history = [
            Movement('figurine', 200, 1, 'Young'),
            Movement('figurine', 3, 200, 'Heretics'),
            Movement('figurine', 1, 500, 'Bones'),
            Movement('figurine', 4, 320, 'of a'),
            Movement('figurine', 20, 100, 'Rabbit'),
        ]
        wh.inventory = {
            'figurine': [Package(200, 1, '11111111'),
                         Package(3, 200, '11111111'),
                         Package(1, 500, '11111111'),
                         Package(4, 320, '11111111'),
                         Package(20, 100, '11111111')]
        }

        self.assertTupleEqual(wh.try_sell('figurine', 150, 90, 'sale'),
                              (150, 4502))
        self.assertEqual(len(wh.history), 10)
        self.assertEqual(len(wh.inventory['figurine']), 1)
        self.assertEqual(wh.inventory['figurine'][0].amount, 78)
        self.assertSetEqual(wh.find_inconsistencies(), set())

    def test_try_sell_9(self) -> None:
        wh = Warehouse()

        wh.history = [
            Movement('album', 40, 1, 'Aquilus'),
            Movement('album', 50, 10, '-'),
            Movement('album', 20, 20, 'Griseus'),
        ]
        wh.inventory = {
            'album': [Package(40, 1, '11111111'),
                      Package(50, 10, '11111111'),
                      Package(20, 20, '11111111')]
        }

        self.assertTupleEqual(wh.try_sell('album', 30, 10, 'K'), (0, 0))
        self.assertEqual(len(wh.inventory), 1)
        self.assertEqual(len(wh.inventory['album']), 3)
        self.assertEqual(len(wh.history), 3)
        self.assertSetEqual(wh.find_inconsistencies(), set())

    def test_try_sell_10(self) -> None:
        wh = Warehouse()

        wh.history = [
            Movement('shisha', 40, 10, 'Expedition'),
            Movement('shisha', -40, 10, 'Clubhouse')
        ]

        self.assertTupleEqual(wh.try_sell('album', 4, 9, 'Pls'), (0, 0))
        self.assertDictEqual(wh.inventory, {})
        self.assertEqual(len(wh.history), 2)
        self.assertSetEqual(wh.find_inconsistencies(), set())

    def test_try_sell_11(self) -> None:
        wh = Warehouse()

        wh.history = [Movement('bananas', 1, 1, 'ACME Everything'),
                      Movement('bananas', 1, 22, 'ACME Everything'),
                      Movement('bananas', 1, 2, 'ACME Everything'),
                      Movement('bananas', 1, 23, 'ACME Everything'),
                      Movement('bananas', 1, 3, 'ACME Everything'),
                      Movement('bananas', 1, 24, 'ACME Everything'),
                      Movement('bananas', 2, 4, 'ACME Everything'),
                      Movement('bananas', 1, 25, 'ACME Everything'),
                      Movement('bananas', 2, 5, 'ACME Everything'),
                      Movement('bananas', 1, 26, 'ACME Everything'),
                      Movement('bananas', 3, 6, 'ACME Everything'),
                      Movement('bananas', 1, 27, 'ACME Everything'),
                      Movement('bananas', 4, 7, 'ACME Everything'),
                      Movement('bananas', 1, 28, 'ACME Everything'),
                      Movement('bananas', 5, 8, 'ACME Everything'),
                      Movement('bananas', 1, 29, 'ACME Everything'),
                      Movement('bananas', 9, 9, 'ACME Everything'),
                      Movement('bananas', 1, 30, 'ACME Everything'),
                      Movement('bananas', 19, 10, 'ACME Everything'),
                      Movement('bananas', 1, 31, 'ACME Everything')]
        wh.inventory = {
            'bananas': [Package(1, 31, '20211231'),
                        Package(19, 10, '20211231'),
                        Package(1, 30, '20211231'), Package(9, 9, '20211231'),
                        Package(1, 29, '20211231'), Package(5, 8, '20211231'),
                        Package(1, 28, '20211231'), Package(4, 7, '20211231'),
                        Package(1, 27, '20211231'), Package(3, 6, '20211231'),
                        Package(1, 26, '20211231'), Package(2, 5, '20211231'),
                        Package(1, 25, '20211231'), Package(2, 4, '20211231'),
                        Package(1, 24, '20211231'), Package(1, 3, '20211231'),
                        Package(1, 23, '20211231'), Package(1, 2, '20211231'),
                        Package(1, 22, '20211231'), Package(1, 1, '20211231')],
        }
        self.assertTupleEqual(wh.try_sell('bananas', 57, 11,
                                          'Customer #524721'), (56, 615))
        self.assertEqual(len(wh.inventory['bananas']), 1)
        self.assertSetEqual(wh.find_inconsistencies(), set())

    def test_average_prices(self) -> None:
        wh = TestWarehouse.example_warehouse()

        expected = {
            'rice': 80.875,
            'corn': 15,
            'peas': (9774 + 64 * 7) / (9774 + 64),
        }

        avg_prices = wh.average_prices()

        self.assertSetEqual(set(expected.keys()), set(avg_prices.keys()))

        for item in avg_prices:
            self.assertAlmostEqual(avg_prices[item], expected[item])

        assert wh.best_suppliers() \
               == {'UniCORN & co.', 'G. P. a C.', 'RICE Unlimited'}

        wh = Warehouse()

        wh.history = [Movement('rice', 1, 1, 'A'),
                      Movement('rice', -1, 1, 'A')]
        wh.inventory = {
            'rice': [],
        }

        self.assertDictEqual(wh.average_prices(), {})

    def test_best_suppliers(self) -> None:
        wh = TestWarehouse.example_warehouse()

        self.assertSetEqual(wh.best_suppliers(),
                            {'UniCORN & co.', 'G. P. a C.', 'RICE Unlimited'})

        wh = Warehouse()

        wh.history = [Movement('rice', 1, 1, 'A'),
                      Movement('rice', -1, 1, 'A')]
        wh.inventory = {
            'rice': [],
        }

        self.assertSetEqual(wh.best_suppliers(), {'A'})

        wh = Warehouse()

        wh.history = [Movement('rice', 1, 1, 'A'),
                      Movement('rice', -1, 1, 'A')]
        wh.inventory = {}

        self.assertSetEqual(wh.best_suppliers(), {'A'})
        self.assertSetEqual(wh.find_inconsistencies(), set())
        

if __name__ == '__main__':
    main()
