import math
from typing import List, Dict, Set, Tuple


class Package:
    def __init__(self, amount: int, price: int, expiry: str):
        self.amount = amount
        self.price = price
        self.expiry = expiry


class Movement:
    def __init__(self, item: str, amount: int, price: int, tag: str):
        self.item = item
        self.amount = amount
        self.price = price
        self.tag = tag


class Warehouse:
    def __init__(self) -> None:
        self.history: List['Movement'] = []
        self.inventory: Dict[str, List['Package']] = {}

    def store(self, item: str, amount: int,
              price: int, expiry: str, tag: str) -> None:
        package_list = self.inventory.get(item, [])

        for i in range(len(package_list)):

            if int(expiry) >= int(package_list[i].expiry):
                package_list.insert(i, Package(amount, price, expiry))
                break

            elif i == len(package_list) - 1:
                package_list.append(Package(amount, price, expiry))

        if len(package_list) == 0:
            package_list.append(Package(amount, price, expiry))

        self.inventory[item] = package_list
        self.history.append(Movement(item, amount, price, tag))

    def make_inventory(self, history: List['Movement']) -> \
            Dict[str, Dict[int, int]]:
        inventory: Dict[str, Dict[int, int]] = {}

        for movement in history:
            item = movement.item
            amount = movement.amount
            price = movement.price

            inventory[item] = inventory.get(item, {})
            inventory[item][price] = \
                inventory.get(item, {}).get(price, 0) + amount

        return inventory

    def find_inconsistencies(self) -> Set[Tuple[str, int, int]]:
        history = self.history
        inventory2 = self.make_inventory(history)
        for item in self.inventory:

            for package in self.inventory[item]:
                price = package.price
                amount = package.amount

                inventory2[item] = inventory2.get(item, {})
                inventory2[item][price] = \
                    inventory2[item].get(price, 0) - amount

        return {(item, price, -inventory2[item][price])
                for item in inventory2
                for price in inventory2[item]
                if inventory2[item][price] != 0}  # v haskeli sme to teraz
                                                  # mali tak som vyskusal :)

    def remove_package(self, package: Package,
                       package_list: str, message: str) -> None:

        self.history.append(Movement(package_list,
                                  - package.amount,
                                  package.price,
                                  '{}'.format(message)))

        self.inventory[package_list].remove(package)

    def remove_expired(self, today: str) -> List['Package']:
        trash = []
        inventory = self.inventory
        for package_list in inventory:
            for package in list(inventory[package_list]):
                if int(package.expiry) < int(today):
                    trash.append(package)
                    self.remove_package(package, package_list, 'EXPIRED')
        return trash

    def average_prices(self) -> Dict[str, float]:
        inventory = self.inventory
        result = {}
        for package_list in inventory:
            avg = []
            amount = []
            for package in inventory[package_list]:
                avg.append(package.amount * package.price)
                amount.append(package.amount)
            if amount != []:
                result[package_list] = (sum(avg) / sum(amount))
        return result

    def best_suppliers(self) -> Set[str]:
        history = self.history
        result: Set[str] = set()
        items: Dict[str, Dict[str, int]] = {}
        for movement in history:

            item = movement.item
            name = movement.tag
            amount = movement.amount

            if amount > 0:
                suppliers = items.get(item, {})
                suppliers[name] = suppliers.get(name, 0) + amount
                items[item] = suppliers

        for item in items:
            best = 0
            best_suppliers = set()
            for supplier in items[item]:
                current = items[item][supplier]
                if current == best:
                    best_suppliers.add(supplier)

                if current > best:
                    best = items[item][supplier]
                    best_suppliers = {supplier}

            result = result.union(best_suppliers)
        return result

    def find_packages(self, inventory: List['Package'], amount: int,
                      price: int) -> Tuple[int, int, int, int]:
        total_price, total_amount = 0, 0
        to_sell = 0
        best_amount, best_price = 0, 0

        for i in range(-1, -len(inventory) - 1, -1):
            quantity = inventory[i].amount
            value = inventory[i].price

            if total_amount + quantity > amount:
                break

            total_price += quantity * value
            total_amount += quantity

            if total_price / total_amount <= price:
                best_price, best_amount = total_price, total_amount
                to_sell = i

                if i == -len(inventory):
                    return (to_sell, best_amount, best_price, 0)

        last = i
        leftovers = (amount - total_amount) % quantity

        if (total_price + leftovers * value) / \
           (total_amount + leftovers) <= price:

            best_price, best_amount = total_price + leftovers * value,\
                                    total_amount + leftovers
            if leftovers > 0:
                to_sell = last + 1
                inventory[last].amount -= leftovers

        return (to_sell, best_amount, best_price, leftovers)

    def remove_packages(self, to_sell: int, inventory: List['Package'],
                        item: str, tag: str) -> None:

        for i in range(-1, to_sell - 1, -1):
            package = inventory[i]
            amount = package.amount
            price = package.price
            self.history.append(Movement(item, -amount, price, tag))
            self.inventory[item].pop()

    def find_leftovers(self, index, best_amount, best_price, parameters):
        inventory, price, item, tag = parameters

        value = inventory[index].price
        big_leftovers = (best_price - best_amount*price) // (price-value)
        best_price += big_leftovers * value
        best_amount += big_leftovers

        if big_leftovers > 0:
            inventory[index].amount -= big_leftovers
            self.history.append(Movement(item, - (big_leftovers), value, tag))

        return best_amount, best_price

    def try_sell(self, item: str, amount: int,
                 price: int, tag: str) -> Tuple[int, int]:
        inventory = self.inventory.get(item, []).copy()
        if inventory == []:
            return (0, 0)

        to_sell, best_amount, best_price, leftovers = \
            self.find_packages(inventory, amount, price)

        self.remove_packages(to_sell, inventory, item, tag)

        if leftovers > 0:
            if best_amount < amount and to_sell - 1 >= - len(inventory):

                parameters = (inventory, price, item, tag)
                best_amount, best_price = \
                    self.find_leftovers(to_sell - 1, best_amount,
                                        best_price, parameters)

            else:
                self.history.append(Movement(item, - leftovers,
                                 inventory[to_sell - 1].price, tag))

        return best_amount, best_price


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
    # print_warehouse(wh)


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
    assert wh.try_sell('rice', 500, 15, 'Pear Shop') \
        == (42 + 100 + 90, 42 * 9 + 100 * 17 + 90 * 14)
    print_warehouse(wh)
    assert len(wh.history) == 10
    assert wh.find_inconsistencies() == set()

    wh = example_warehouse()
    assert wh.try_sell('rice', 500, 16, 'Pear Shop') \
        == (42 + 100 + 90 + 2, 42 * 9 + 100 * 17 + 90 * 14 + 2 * 158)
    assert len(wh.history) == 11
    assert wh.find_inconsistencies() == set()

    # uncomment to visually check the output:
    # print_warehouse(wh)

    wh = example_warehouse()
    assert wh.try_sell('rice', 500, 81, 'Pear Shop') \
        == (42 + 100 + 90 + 200, 42 * 9 + 100 * 17 + 90 * 14 + 200 * 158)
    assert len(wh.history) == 11
    assert wh.find_inconsistencies() == set()

    wh = example_warehouse()
    assert wh.try_sell('peas', 64, 10, 'Pea Shop') \
           == (64, 448)

    wh = Warehouse()
    wh.store('rice', 1, 1, '20000101', 'A')
    wh.try_sell('rice', 1, 1, 'A')
    assert wh.inventory['rice'] == []


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
        assert math.isclose(avg_prices[item], expected[item])

    assert wh.best_suppliers() \
        == {'UniCORN & co.', 'G. P. a C.', 'RICE Unlimited'}

    wh = Warehouse()
    wh.history = [Movement('rice', 1, 1, 'A'), Movement('rice', -1, 1, 'A')]
    wh.inventory = {'rice': [], }
    assert wh.average_prices() == {}

    wh.history = [Movement('rice', 1, 1, 'A'), Movement('rice', -1, 1, 'A')]
    wh.inventory = {}
    assert wh.best_suppliers() == {'A'}

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
               Package(2, 258, '19970102'),
               Package(1, 5, '19940203'),
               Package(1, 2, '19041012')],
      'rice': [Package(258, 258, '19990301'),
               Package(2562, 2, '19990211')],
      'barley': [Package(2, 1797, '19990306'),
                 Package(100860007, 3164012802, '19980204')]}
    assert wh.try_sell('peas', 33753867, 8405601, 'z') \
           == (33753867, 283721531989783)

    wh = Warehouse()
    wh.history = [Movement('peas', 2, 1123123, 'A'),
                  Movement('peas', 1, 2, 'B'),
                  Movement('peas', 1, 2123, 'B')]
    assert wh.best_suppliers() == {'A', 'B'}

    wh = Warehouse()
    wh.history = []
    wh.inventory = {'rice': [Package(2, 1, '20000101'),
                             Package(1, 2, '20000101'),
                             Package(1, 2, '20000101')]}
    assert wh.find_inconsistencies() == {('rice', 1, 2), ('rice', 2, 2)}

    wh = Warehouse()

    assert(wh.try_sell("lambo", 120, 300, "majoporše a.s.")) == (0, 0)

    wh.inventory["porche"] = []

    assert(wh.try_sell("porche", 12034, 121234, "majoporše a.s.")) == (0, 0)

    wh.inventory["lambo"] = [Package(50, 1000000000000, 'nigdy')]

    assert(wh.try_sell("lambo", 120, 300, "majoporše a.s.")) == (0, 0)

    wh.inventory = {'porche': [Package(100, 10, '53470731'),
                               Package(100, 10, '19520922'),
                               Package(70, 0, '53470731'),
                               Package(50, 1000, '53470731'),
                               Package(50, 0, '53470731')]}

    assert(wh.try_sell("porche", 150, 500, "majoporše a.s.")) == (150, 50000)

    wh.inventory["lambo"] = [Package(100, 10, 'nigdy'),
                             Package(100, 10, 'nigdy'),
                             Package(70, 10000, 'nigdy'),
                             Package(50, 100, 'nigdy'),
                             Package(50, 100, 'nigdy')]

    assert(wh.try_sell("lambo", 120, 300, "majoporše a.s.")) == (102, 30000)


if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
    test5()
wh = Warehouse()
# wh.history = [Movement('lambo', 100, 10, 'asd')]
# wh.inventory = {}
# 
# print(wh.find_inconsistencies())
# wh.history = [Movement('rice', 1, 1, 'A')]
# wh.inventory = {'rice': [Package(1, 1, '20000101')],}
# 
# print(wh.try_sell('rice', 2, 1, 'A'))
# 
# wh.inventory = {'rice': [Package(10, 15, '20000101'), Package(10, 15, '20000102')]}
# wh.history = []
# print_warehouse(wh)
# print(wh.try_sell('rice', 11, 187, 'A'))
# print_warehouse(wh)
# 

wh.inventory = {
      'potatoes': [Package(257163551, 3, '19990710'), Package(16843522, 17039629, '19990502'), Package(297, 65793, '19990401'), Package(738920197, 258, '19910202')],
      'rice': [Package(2, 2, '19990301'), Package(65793, 16842754, '19990221'), Package(2, 67174913, '19990101'), Package(400390, 1, '19990101')],
      }
print_warehouse(wh)
print(wh.try_sell('rice', 3366384796, 5378, 't'))
print_warehouse(wh)
