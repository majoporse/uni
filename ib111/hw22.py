from random import randint, seed
INVALID_POSITION = 0
EMPTY_POSITION = 1
ROUND_OVER = 2
PLAY_AGAIN = 3
pos = 0
seed(69)
## @B
## + rozumně sledovatelný kód
## + místy využívá pěkné, efektivní konstrukce
## - míst využívá nepěkné nebo neefektivní konstrukce
## - několik nevhodně pojmenovaných proměnných

def init(size, start):

    return ([start for i in range(size)]+[0],
            [start for i in range(size)]+[0])
## ~ pozor, + vynucuje kopii obou svých argumentů, efektivnější by bylo
## použít append

def play(our, their, position):

    if position not in range(0, len(our) - 1):
        return INVALID_POSITION
## zbytečně neefektivní; Python je hloupý a pokud je position mimo uvedené
## hranice, stejně por každou hodnotu z rozsahu zkontroluje, jestli
## se jí position náhodou nerovná -- obyčejná dvě porovnání by zde byla
## nesrovnatelně efektivnější
## EDIT: ještě mi to vrtalo hlavou -- a zjistila jsem, že pro celá čísla python
## _je_ dostatečně chytrý, aby nezkoušel všechny hodnoty, ale došel k závěru
## na základě několika matematických operací -- uvedený řádek tedy není zásadně
## méně efektivní než obyčejné porovnání -- nicméně porovnání není méně
## efektivní než toto a zároveň je výrazně srozumitelnější -- už jenom proto
## že je na první pohled zřejmé, co se děje a že opravdu jde o efektivní
## řešení; zároveň porovnání funguje efektivně i třeba s desetinnými čísly,
## se kterými už si range chytře neporadí

    if our[position] == 0:
        return EMPTY_POSITION

    shift = our[position]
    our[position] = 0
    length = 2 * len(our) - 1
## výstižnější by bylo pojmenovat tuto proměnnou třeba moves a název shift
## (nebo offset) si nechat místo i v následujícím kódu


    for i in range(position + 1, shift + 1 + position):
## efektivní indexování bez nutnosti kopírovat hrací plochu, výborně! :)


        last_number = (i % length) if i % length < len(our) else (i % length - len(our))
## number v názvu zní spíš, jako by šlo o hodnotu, nicméně proměnná představuje
## index do příslušné hrací plochy -- bylo by vhodné, aby název odrážel, že jde
## o index současného důlku


         
## bylo by pěkné zarovnat else pod =

        (our if i % length < len(our) else their)[last_number] += 1

    i = (shift + position) % length
## zde už jde (téměř) o index posledního důlku; název by to měl odrážet


    length_their = len(their)
    if i == len(our) - 1:
        return PLAY_AGAIN
## název proměnné je delší a o nic méně popisný než přímo len(their), navíc
## délku seznamu v Pythonu získáme efektivně okamžitě


    elif (i < len(our) and our[last_number] == 1)\
            and (their[length_their - 2 - last_number] != 0):
        our[last_number] = 0
## zbytečný else (elif) po return, stačí přímo if
## navíc zbytečné závorky


        our[-1] += 1 + ((their[length_their - 2 - i]))
        their[length_their - 2 - i] = 0
## zbytečné závorky (dvakrát)

    return ROUND_OVER

def random_choice(our):
    nonzero = [num for num in our[:-1] if num != 0]
    if not nonzero:
## pozor, slice vytváří kopii


        return
## raději explicitně return None -- to, že v Pythonu je None "defaultní"
## vrácená hodnota, není něco, čeho bys chtěl využívat


    random = randint(1, len(nonzero))
    numbers = 0
    position = 0
    while numbers < random:
## elegantnější by bylo si v nonzero pamatovat indexy, ne hodnoty
## a jenom vrátit index na pozici dané random

        if our[position] != 0:
            numbers += 1
        position += 1

    return position - 1

def run_random_game(size, start):
    our, their = init(size, start)

    theirbank = 0
## zbytečná proměnná, stačilo by v podmínce používat čistě their[-1],
## nemusel bys hodnotu pak nastavovat a v cyklu udržovat


    changes = False
## nevypovídající název -- měl by odrážet, že hodnota vyjadřuje, jestli
## na tahu právě je nebo není hráč, který hru začínal


    while sum(our) != theirbank:
        position = random_choice(our)
## ~ výstižnější by bylo nonzero_position


        while position is not None and play(our, their, position) == 3:
            position = random_choice(our)
        if position is None:
            break
        theirbank = their[-1]
        changes = not changes
        our, their = their, our
## místo 3 bys měl rozhodně použít definovanou globální konstantu!
## je žádoucí, aby program nebyl závislý na konkrétních hodnotách konstant,
## když v tomto případě samy o sobě nemají žádný význam (jiný než odlišit se
## od ostatních globálních konstant)


    if changes:
        our, their = their, our
## pěkné :)
    return sum(our), sum(their)

def main():
    # --- init ---
    assert init(6, 3) \
        == ([3, 3, 3, 3, 3, 3, 0], [3, 3, 3, 3, 3, 3, 0])

    assert init(9, 7) \
        == ([7, 7, 7, 7, 7, 7, 7, 7, 7, 0], [7, 7, 7, 7, 7, 7, 7, 7, 7, 0])

    # --- play ---

    our = [3, 0, 6, 0]
    their = [3, 3, 3, 0]
    assert play(our, their, -1) == INVALID_POSITION
    assert our == [3, 0, 6, 0]
    assert their == [3, 3, 3, 0]

    our = [3, 0, 6, 0]
    their = [3, 3, 3, 0]
    assert play(our, their, 0) == PLAY_AGAIN
    assert our == [0, 1, 7, 1]
    assert their == [3, 3, 3, 0]

    our = [3, 0, 6, 0]
    their = [3, 3, 3, 0]
    assert play(our, their, 1) == EMPTY_POSITION
    assert our == [3, 0, 6, 0]
    assert their == [3, 3, 3, 0]

    our = [3, 0, 6, 0]
    their = [3, 3, 3, 0]
    assert play(our, their, 2) == ROUND_OVER
    assert our == [4, 0, 0, 6]
    assert their == [4, 0, 4, 0]

    our = [3, 0, 6, 0]
    their = [3, 3, 3, 0]
    assert play(our, their, 3) == INVALID_POSITION
    assert our == [3, 0, 6, 0]
    assert their == [3, 3, 3, 0]

    # --- random_choice ---

    assert random_choice([1, 2, 3, 4, 0]) in [0, 1, 2, 3]

    assert random_choice([3, 3, 0, 3, 3, 7]) in [0, 1, 3, 4]

    assert random_choice([0, 0, 0, 1]) is None
    for i in range(10):
        for j in range (10):
            print(run_random_game(i,j))

if __name__ == '__main__':
    main()
