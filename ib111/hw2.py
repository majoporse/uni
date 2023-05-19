from random import choice
INVALID_POSITION = 0
EMPTY_POSITION = 1
ROUND_OVER = 2
PLAY_AGAIN = 3


def init(size, start):
    return ([start for i in range(size)]+[0],
            [start for i in range(size)]+[0])


def play(our, their, position):

    if position < 0 or position > len(our) - 2:
        return INVALID_POSITION

    if our[position] == 0:
        return EMPTY_POSITION

    offset = our[position]
    our[position] = 0
    length = 2 * len(our) - 1

    for i in range(position + 1, offset + position + 1):

        current_position = (i % length) if i % length < len(our)\
                           else i % length - len(our)

        (our if i % length < len(our) else their)[current_position] += 1

    last_position = (offset + position) % length
    if last_position == len(our) - 1:
        return PLAY_AGAIN

    if last_position < len(our) and our[current_position] == 1\
            and their[len(their) - current_position - 2] != 0:
        our[current_position] = 0
        our[-1] += 1 + their[len(their) - last_position - 2]
        their[len(their) - last_position - 2] = 0

    return ROUND_OVER


def random_choice(our):
    nonzero_position = [num for num in range(len(our)-1) if our[num] != 0]
    if not nonzero_position:
        return None
    return choice(nonzero_position)


def run_random_game(size, start):
    our, their = init(size, start)
    flipped = False
    position = random_choice(our)
    while position is not None:
        if play(our, their, position) != PLAY_AGAIN:
            flipped = not flipped
            our, their = their, our
        position = random_choice(our)
    if flipped:
        our, their = their, our
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


if __name__ == '__main__':
    main()
