from typing import Dict, List, Optional, Set, Tuple

EMPTY = '   '
L_SHAPE = '└─ '
T_SHAPE = '├─ '
STRAIGHT = '│  '


class Person:
    def __init__(self, pid: int, name: str, birth_year: int):
        self.pid = pid
        self.name = name
        self.birth_year = birth_year
        self.parent: Optional['Person'] = None
        self.children: List['Person'] = []

    def is_valid(self) -> bool:
        return self.is_valid_rec()

    def is_valid_rec(self) -> bool:

        kids = self.children
        kid_names = [kid.name for kid in kids]
        if len(kid_names) > len(set(kid_names)):
            return False

        if self.name == "":
            return False

        for kid in kids:
            if self.birth_year >= kid.birth_year:
                return False
            if not kid.is_valid_rec():
                return False

        return True

    def draw(self, names_only: bool) -> None:
        self.draw_rec(names_only, None, '')

    def draw_rec(self, names_only: bool, in_between: Optional[bool],
                 previous: str) -> None:

        if names_only:
            print(self.name)
        else:
            print(f'{self.name} ({self.birth_year}) [{self.pid}]')

        if in_between is not None:
            if in_between:
                previous = previous + EMPTY
            else:
                previous = previous + STRAIGHT

        for (index, kid) in enumerate(self.children):
            in_between = index == len(self.children) - 1
            print(f"{previous}{L_SHAPE if in_between else T_SHAPE}", end='')
            kid.draw_rec(names_only, in_between, previous)

    def parents_younger_or_older(self, age: int, older: bool) -> Set[int]:
        result = set()
        for kid in self.children:
            difference = kid.birth_year - self.birth_year

            if difference > age if older \
               else difference < age:
                result.add(self.pid)

            result |= kid.parents_younger_or_older(age, older)

        return result

    def parents_younger_than(self, age_limit: int) -> Set[int]:
        return self.parents_younger_or_older(age_limit, False)

    def parents_older_than(self, age_limit: int) -> Set[int]:
        return self.parents_younger_or_older(age_limit, True)

    def childless(self) -> Set[int]:
        result = set()
        if self.children == []:
            result.add(self.pid)
        for kid in self.children:
            result |= kid.childless()
        return result

    def ancestors(self) -> List['Person']:
        result: List['Person'] = []
        person = self
        while person.parent is not None:
            result.append(person.parent)
            person = person.parent
        result.reverse()
        return result

    def order_of_succession(self, alive: Set[int]) -> Dict[int, int]:
        order_list = self.order_rec(alive)
        result = {}
        for (index, pid) in enumerate(order_list):
            result[pid] = index + 1
        return result

    def order_rec(self, alive: Set[int]) -> List[int]:
        result_list = []
        child_list = self.children

        for child in sorted(child_list, key=lambda x: x.birth_year):
            if child.pid in alive:
                result_list.append(child.pid)
            result_list.extend(child.order_rec(alive))

        return result_list

    def remove_extinct_branches(self, alive: Set[int]) -> None:
        self.remove_rec(alive, False)

    def remove_rec(self, alive: Set[int], check_self: bool) -> bool:
        new_children = []
        for child in self.children.copy():
            if not child.remove_rec(alive, True):
                new_children.append(child)
        self.children = new_children

        if self.children == [] and self.pid not in alive and check_self:
            return True

        return False


def check_valid_tree(names: Dict[int, str],
                     children: Dict[int, List[int]],
                     birth_years: Dict[int, int]) \
                     -> Tuple[Optional[int], bool]:

    name_set = set(names.keys())
    birth_years_set = set(birth_years.keys())

    children_list = [kid_pid for person in children
                     for kid_pid in children[person]]
    children_kids = set(children_list)

    children_all = set(children.keys()) | children_kids

    valid = name_set == birth_years_set and \
        children_all.issubset(name_set) and \
        len(children_list) == len(children_kids)

    oldest = []
    for person in names:
        if person not in children_kids:
            oldest.append(person)

    if len(oldest) != 1:
        return (None, valid)

    return (oldest[0], valid)


def build_family_tree(names: Dict[int, str],
                      children: Dict[int, List[int]],
                      birth_years: Dict[int, int]) -> Optional[Person]:

    oldest_pid, is_valid = check_valid_tree(names, children, birth_years)
    if oldest_pid is None or not is_valid:
        return None

    return build_rec(None, oldest_pid, names, children, birth_years)


def build_rec(parent: Optional[Person], pid: int, names: Dict[int, str],
              children: Dict[int, List[int]], birth_years:
              Dict[int, int]) -> Person:

    name = names[pid]
    birth_year = birth_years[pid]

    person = Person(pid, name, birth_year)
    if parent is not None:
        parent.children.append(person)
    person.parent = parent
    kids = children.get(pid, [])
    for kid_pid in kids:
        build_rec(person, kid_pid, names, children, birth_years)
    return person


def valid_family_tree(person: Person) -> bool:
    oldest_member = find_oldest(person)
    return oldest_member.is_valid()


def find_oldest(person: Person) -> Person:
    while person.parent is not None:
        person = person.parent
    return person


def test_one_person() -> None:
    adam = build_family_tree({1: "Adam"}, {}, {1: 1})
    assert isinstance(adam, Person)
    assert adam.pid == 1
    assert adam.birth_year == 1
    assert adam.name == "Adam"
    assert adam.children == []
    assert adam.parent is None

    assert adam.is_valid()
    assert adam.parents_younger_than(18) == set()
    assert adam.parents_older_than(81) == set()
    assert adam.childless() == {1}
    assert adam.ancestors() == []
    assert adam.order_of_succession({1}) == {}


def example_family_tree() -> Person:
    qempa = build_family_tree(
        {
            17: "Qempa'",
            127: "Thok Mak",
            290: "Worf",
            390: "Worf",
            490: "Mogh",
            590: "Kurn",
            611: "Ag'ax",
            561: "K'alaga",
            702: "Samtoq",
            898: "K'Dhan",
            429: "Grehka",
            1000: "Alexander Rozhenko",
            253: "D'Vak",
            106: "Elumen",
            101: "Ga'ga",
        },
        {
            17: [127, 290],
            390: [898, 1000],
            1000: [253],
            127: [611, 561, 702],
            590: [429, 106, 101],
            490: [390, 590],
            290: [490],
            702: [],
        },
        {
            1000: 2366,
            101: 2366,
            106: 2357,
            127: 2281,
            17: 2256,
            253: 2390,
            290: 2290,
            390: 2340,
            429: 2359,
            490: 2310,
            561: 2302,
            590: 2345,
            611: 2317,
            702: 2317,
            898: 2388,
        }
    )

    assert qempa is not None
    return qempa


def test_example() -> None:
    qempa = example_family_tree()
    assert qempa.name == "Qempa'"
    assert qempa.pid == 17
    assert qempa.birth_year == 2256
    assert qempa.parent is None
    assert len(qempa.children) == 2

    thok_mak, worf1 = qempa.children
    assert worf1.name == "Worf"
    assert worf1.pid == 290
    assert worf1.birth_year == 2290
    assert worf1.parent == qempa
    assert len(worf1.children) == 1

    mogh = worf1.children[0]
    assert mogh.name == "Mogh"
    assert mogh.pid == 490
    assert mogh.birth_year == 2310
    assert mogh.parent == worf1
    assert len(mogh.children) == 2

    worf2 = mogh.children[0]
    assert worf2.name == "Worf"
    assert worf2.pid == 390
    assert worf2.birth_year == 2340
    assert worf2.parent == mogh
    assert len(worf2.children) == 2

    alex = worf2.children[1]
    assert alex.name == "Alexander Rozhenko"
    assert alex.pid == 1000
    assert alex.birth_year == 2366
    assert alex.parent == worf2
    assert len(alex.children) == 1

    assert qempa.is_valid()
    assert alex.is_valid()
    assert valid_family_tree(qempa)
    assert valid_family_tree(alex)

    thok_mak.name = ""
    assert not qempa.is_valid()
    assert alex.is_valid()
    assert not valid_family_tree(qempa)
    assert not valid_family_tree(alex)
    thok_mak.name = "Thok Mak"

    thok_mak.birth_year = 2302
    assert not qempa.is_valid()
    assert alex.is_valid()
    assert not valid_family_tree(qempa)
    assert not valid_family_tree(alex)
    thok_mak.birth_year = 2281

    assert qempa.parents_younger_than(12) == set()
    assert qempa.parents_younger_than(15) == {590}
    assert qempa.parents_younger_than(21) == {290, 590}

    assert qempa.parents_older_than(48) == set()
    assert qempa.parents_older_than(40) == {390}

    assert thok_mak.parents_younger_than(21) == set()
    assert thok_mak.parents_older_than(40) == set()

    assert qempa.childless() == {101, 106, 253, 429, 561, 611, 702, 898}
    assert thok_mak.childless() == {611, 561, 702}

    assert alex.ancestors() == [qempa, worf1, mogh, worf2]
    assert thok_mak.ancestors() == [qempa]
    assert qempa.ancestors() == []

    alive = {17, 101, 106, 127, 253, 290, 390, 429,
             490, 561, 590, 611, 702, 898, 1000}
    succession = {
        101: 14,
        106: 12,
        127: 1,
        253: 9,
        290: 5,
        390: 7,
        429: 13,
        490: 6,
        561: 2,
        590: 11,
        611: 3,
        702: 4,
        898: 10,
        1000: 8,
    }

    assert qempa.order_of_succession(alive) == succession

    alive.remove(17)
    assert qempa.order_of_succession(alive) == succession

    alive -= {127, 290, 490, 590}
    assert qempa.order_of_succession(alive) == {
        561: 1,
        611: 2,
        702: 3,
        390: 4,
        1000: 5,
        253: 6,
        898: 7,
        106: 8,
        429: 9,
        101: 10,
    }

    assert mogh.order_of_succession(alive) == {
        390: 1,
        1000: 2,
        253: 3,
        898: 4,
        106: 5,
        429: 6,
        101: 7,
    }


def draw_example() -> None:
    qempa = example_family_tree()
    print("První příklad:")
    qempa.draw(False)

    print("\nDruhý příklad:")
    qempa.children[1].children[0].draw(True)

    alive1 = {101, 106, 253, 429, 561, 611, 702, 898}
    alive2 = {101, 106, 253, 390, 898, 1000}
    for alive in alive1, alive2:
        print(f"\nRodokmen po zavolání remove_extinct_branches({alive})\n"
              "na výchozí osobě:")
        qempa = example_family_tree()
        qempa.remove_extinct_branches(alive)
        qempa.draw(True)

    print(f"\nRodokmen po zavolání remove_extinct_branches({alive})\n"
          "na osobě jménem Mogh:")
    qempa = example_family_tree()
    qempa.children[1].children[0].remove_extinct_branches(alive2)
    qempa.draw(True)


if __name__ == '__main__':
    test_one_person()
    test_example()
    draw_example()  # uncomment to run
#     root = build_family_tree(
#       {1: 'Adam', 2: 'Eva', 3: 'Kain'},
#       {1: [2, 3], 2: [3]},
#       {1: 1, 2: 2, 3: 3})
#     print(root)
#     root = build_family_tree(
#       {9351: 'Torak', 7426: 'Marab', 8081: "Ko'lek"},
#       {9351: [7426, 8081]},
#       {9351: 2140, 7426: 2161, 8081: 2232})
#     root.children[1].remove_extinct_branches(set())
#     root.draw(False)
