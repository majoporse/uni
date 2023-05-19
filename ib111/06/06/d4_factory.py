from typing import Dict, Tuple, Deque

# † V této ukázce si implementujeme jednoduchou „továrnu“ která
# vyrábí různé typy výrobků. Výrobek má název a seznam součástek
# (jiných výrobků), které k jeho výrobě potřebujeme. Továrna má
# sklad, kde má součástky uloženy (v různém množství), a «frontu»
# požadavků na výrobu. Mít mnoho součástek na skladě je drahé, proto
# se snažíme skladové zásoby minimalizovat.

# Nejprve si zadefinujeme potřebné typy, které budou popisovat stav
# továrny. Popis výrobků: každému výrobku (popsanému názvem)
# přiřadíme slovník, který popisuje, jaké součástky výroba vyžaduje a
# v jakém množství.

Products = Dict[str, Dict[str, int]]

# Datový typ ‹Warehouse› popisuje aktuální skladové zásoby: kolik
# kusů kterého výrobku máme uskladněno. Hodnoty zde uložené jsou
# vždy nezáporné.

Warehouse = Dict[str, int]

# Pracovní fronta ‹Queue› popisuje, jaké výrobky máme naplánované
# k výrobě, zatímco slovník ‹InFlight› popisuje, jak se projeví
# zpracování aktuální fronty na skladových zásobách: počítá nové
# výrobky naplánované k výrobě (kladná čísla), ale také rezervované
# součástky potřebné pro jejich výrobu (záporná čísla). Uvažme
# výrobek X, kterého výroba vyžaduje dvě součástky Y a jednu
# součástku Z. Když přidáme sedm kusů výrobku X do fronty – ‹('X',
# 7)› – musíme zároveň upravit slovník ‹InFlight›: hodnotu klíče
# ‹'X'› zvýšíme o 7, hodnotu klíče ‹'Y'› snížíme o 14 a hodnotu
# klíče ‹'Z'› snížíme o 7.

Queue = Deque[Tuple[str, int]]
InFlight = Dict[str, int]

# Tím je popis továrny kompletní: samotná továrna má tedy 4 složky:
# popis výrobků a jejich součástek, skladové zásoby, pracovní
# frontu a sumarizaci efektu fronty na skladové zásoby.

Factory = Tuple[Products, Warehouse, Queue, InFlight]


# Pro zjednodušení procedur, které budou s továrnou pracovat, si nejprve
# zadefinujeme jednoduchou funkci, která vytvoří továrnu ve výchozím stavu:
# skladové zásoby nastaví na 0 a stejně tak inicializuje slovník ‹in_flight›.
# Nebudeme tedy později muset řešit situaci, že nějaký klíč není v některém
# slovníku vůbec přítomen.

def setup_factory(dependencies: Products) -> Factory:
    warehouse: Warehouse = {}
    in_flight: InFlight = {}
    queue: Queue = Deque()
    for product, _ in dependencies.items():
        warehouse[product] = 0
        in_flight[product] = 0
    return (dependencies, warehouse, queue, in_flight)


# Nyní můžeme přistoupit k definici procedur, které budou stav
# továrny měnit: první procedura přidá požadavek na výrobu do fronty
# (a zároveň upraví slovník ‹InFlight›).

def queue_product(factory: Factory, product: str,
                  product_count: int) -> None:
    dependencies, warehouse, queue, in_flight = factory

    # Do fronty nejprve vložíme chybějící komponenty: tyto
    # potřebujeme vyrobit předtím, než můžeme přistoupit k výrobě
    # samotného výrobku ‹product›. Vkládat je budeme v takovém
    # množství, abychom přesně doplnili stávající skladové zásoby na
    # potřebný počet.

    for component, count in dependencies[product].items():
        have = warehouse[component] + in_flight[component]
        need = product_count * count
        if need > have:
            queue_product(factory, component, need - have)
        in_flight[component] -= need
        assert warehouse[component] + in_flight[component] >= 0

    # Poté můžeme vložit samotný požadavek na příslušný počet
    # vyžádaných výrobků.

    queue.append((product, product_count))
    in_flight[product] += product_count


# Kdykoliv během výroby může přijít požadavek na odeslání části
# skladových zásob jinam (buď zákazníkovi, nebo do jiné továrny).
# Kdykoliv se tak stane, hrozí, že nebudeme mít dostatek skladových
# zásob k výrobě některého již naplánovaného výrobku. Přeskládat
# frontu by bylo ale nákladné a nepraktické, proto chybějící
# komponenty zařadíme na konec fronty a s případným nedostatkem se
# vypořádáme později.

def ship_product(factory: Factory, product: str,
                 count: int) -> bool:
    _, warehouse, _, in_flight = factory
    if warehouse[product] < count:
        return False
    warehouse[product] -= count
    expected_total = warehouse[product] + in_flight[product]
    if expected_total < 0:
        queue_product(factory, product, -expected_total)
    return True


# Poslední procedura zpracuje nejstarší požadavek ve frontě: použije
# skladové zásoby komponent k výrobě požadovaného počtu výrobku.
# Je-li fronta prázdná, procedura vrátí ‹False› a nic neudělá.

# Přes veškeré naše úsilí se ale může stát, že na skladě není
# dostatek komponent, protože některé mohly být od vložení požadavku
# do fronty odeslány ze skladu pryč. V takové situaci vyrobíme tolik
# kusů, kolik nám skladové zásoby dovolují a zbytek vložíme na konec
# fronty.

# Všimněte si také práci se slovníkem ‹in_flight›: protože jsme
# z fronty odstranili celý požadavek na ⟦n⟧ kusů, musíme upravit
# ‹in_flight› tak, aby odpovídal změně «stavu fronty», bez ohledu na
# to, kolik kusů produktu se nakonec povede vyrobit. Naproti tomu
# změna ve stavu skladových zásob musí odrážet skutečně vyrobený
# počet kusů.

def build_product(factory: Factory) -> bool:
    dependencies, warehouse, queue, in_flight = factory
    if len(queue) == 0:
        return False

    product, product_count = queue.popleft()
    in_flight[product] -= product_count
    can_build = product_count

    for component, count in dependencies[product].items():
        can_build = min(can_build, warehouse[component] // count)
    for component, count in dependencies[product].items():
        warehouse[component] -= can_build * count
        in_flight[component] += product_count * count

    warehouse[product] += can_build
    if can_build < product_count:
        queue_product(factory, product, product_count - can_build)

    return True


# Zbývá implementaci továrny otestovat. Za povšimnutí stojí, že
# procedury, zejména takové, které pracují se složitějším stavem, se
# testují o něco hůře, než čisté funkce.

def main() -> None:  # demo
    factory = setup_factory({'algorithm': {'idea': 1, 'coffee': 3},
                             'theorem': {'coffee': 7, 'goat': 1},
                             'coffee': {'beans': 1, 'water': 1},
                             'beans': {}, 'water': {},
                             'goat': {}, 'idea': {}})
    _, warehouse, _, in_flight = factory

    assert not build_product(factory)
    queue_product(factory, 'theorem', 3)
    assert warehouse['theorem'] == 0
    assert warehouse['coffee'] == 0
    assert warehouse['goat'] == 0
    assert in_flight['algorithm'] == 0
    assert in_flight['coffee'] == 0
    assert in_flight['theorem'] == 3

    for i in ['water', 'beans', 'goat', 'coffee']:
        assert build_product(factory)
    assert warehouse['goat'] == 3
    assert warehouse['coffee'] == 21
    assert in_flight['goat'] == -3
    assert in_flight['coffee'] == -21

    assert build_product(factory)
    assert warehouse['theorem'] == 3
    assert warehouse['goat'] == 0
    assert warehouse['coffee'] == 0
    assert in_flight['goat'] == 0
    assert in_flight['coffee'] == 0

    queue_product(factory, 'idea', 2)
    queue_product(factory, 'algorithm', 3)
    assert not ship_product(factory, 'idea', 1)
    assert build_product(factory)  # the two ideas
    assert ship_product(factory, 'idea', 1)

    for i in ['water', 'beans', 'coffee', 'idea']:
        assert build_product(factory)
    assert warehouse['idea'] == 2
    assert warehouse['coffee'] == 9
    assert build_product(factory)  # first batch of algorithms
    assert warehouse['coffee'] == 3
    assert warehouse['idea'] == 0
    assert warehouse['algorithm'] == 2
    assert build_product(factory)  # missing idea
    assert warehouse['idea'] == 1
    assert build_product(factory)  # algorithm
    assert warehouse['algorithm'] == 3
    assert warehouse['idea'] == 0


if __name__ == '__main__':
    main()
