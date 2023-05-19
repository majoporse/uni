from typing import List, Tuple

Block = List[Tuple[int, int]]

BLOCK_I, BLOCK_J, BLOCK_L, BLOCK_S, BLOCK_Z, BLOCK_T, BLOCK_O = range(7)
LEFT, RIGHT, ROTATE_CW, ROTATE_CCW, DOWN, DROP, QUIT, NEW_BLOCK = range(8)
CONTINUE, QUIT_GAME, NEXT_BLOCK = range(3)
WALL = "##"
SQUARE = "[]"
EMPTY = "  "

BLOCKS = {BLOCK_I: [(0, -1), (0, 0), (0, 1), (0, 2)],
          BLOCK_J: [(0, -1), (0, 0), (0, 1), (-1, 1)],
          BLOCK_L: [(0, -1), (0, 0), (0, 1), (1, 1)],
          BLOCK_S: [(-1, 1), (0, 1), (0, 0), (1, 0)],
          BLOCK_Z: [(1, 1), (0, 1), (0, 0), (-1, 0)],
          BLOCK_T: [(-1, 0), (0, 0), (1, 0), (0, 1)],
          BLOCK_O: [(0, 0), (0, 1), (1, 1), (1, 0)]}

Layer = List[bool]
Arena = List[Layer]
Anchor = Tuple[int, int]


def coords(block_type: int) -> Block:
    return BLOCKS[block_type]


def rotate(coords: Block, direction: int) -> Block:
    result = []
    direction_x = direction
    direction_y = - direction
    for (x, y) in coords:
        result.append((direction_y * y, direction_x * x))
    return result


def rotate_cw(coords: Block) -> Block:
    return rotate(coords, 1)


def rotate_ccw(coords: Block) -> Block:
    return rotate(coords, -1)


def new_arena(cols: int, rows: int) -> Arena:
    arena = []
    for row in range(rows):
        current_row = []
        for col in range(cols):
            current_row.append(True)
        arena.append(current_row)
    return arena


def is_occupied(arena: Arena, x: int, y: int) -> bool:
    if x <= len(arena[0]) - 1 and y <= len(arena) - 1 \
             and x >= 0 and y >= 0:
        return not arena[y][x]
    return True


def set_occupied(arena: Arena, x: int, y: int, occupied: bool) -> None:
    arena[y][x] = not occupied


def draw(arena: Arena, score: int) -> None:
    for row in arena:
        print(WALL, end='')
        for value in row:
            print(EMPTY if value else SQUARE, end='')
        print(WALL)
    for _ in range(len(arena[0]) + 2):
        print(WALL, end='')
    print()
    print('  Score:{:>{}}'.format(score, 2 * (len(arena[0]) - 3)))


def next_block() -> Block:
    return rotate_cw(coords(BLOCK_S))


def remove_block(arena: Arena, block: Block, anchor: Anchor) -> None:
    for (x, y) in block:
        set_occupied(arena, anchor[0]+x, anchor[1]+y, False)


def insert_block(arena: Arena, block: Block, anchor: Anchor) -> None:
    for (x, y) in block:
        set_occupied(arena, anchor[0] + x, anchor[1] + y, True)


def allign_anchor(arena: Arena, block: Block) -> Tuple[int, int]:
    x_min = 0
    x_max = 0
    y_min = 0
    for (x, y) in block:
        if x < x_min:
            x_min = x
        if x > x_max:
            x_max = x
        if y < y_min:
            y_min = y
    return (len(arena[0]) - 1 - x_max - x_min)//2, -y_min


def check_position(arena: Arena, block: Block,
                   anchor: Anchor, num: int) -> bool:
    anchor_x, anchor_y = anchor

    previous_options = {ROTATE_CW: rotate_ccw(block),
                        ROTATE_CCW: rotate_cw(block)}
    directions = {LEFT: (anchor_x-1, anchor_y),
                  RIGHT: (anchor_x+1, anchor_y),
                  DOWN: (anchor_x, anchor_y+1)}

    prev_block = previous_options.get(num, block)
    direction_x, direction_y = directions.get(num, anchor)
    old_position = []

    for (x1, y1) in prev_block:
        old_position.append((x1 + anchor_x, y1 + anchor_y))

    for (x, y) in block:
        # if occupied then it must be in itself if it's not return false
        # exception for checking for new_block
        if is_occupied(arena, x + direction_x, y + direction_y):
            if num == NEW_BLOCK:
                return False
            elif (x + direction_x, y + direction_y) not in old_position:
                return False
    return True


def get_drop_anchor(arena: Arena, block: Block, anchor: Anchor) -> Anchor:
    anchor_x, anchor_y = anchor
    position = []
    for (x, y) in block:
        position.append((anchor_x+x, anchor_y+y))
    while True:
        for (x, y) in block:
            if anchor_y + y == len(arena) - 1:
                return(anchor_x, anchor_y)
            if (anchor_x + x, anchor_y + y + 1) in position:
                continue
            elif is_occupied(arena, anchor_x + x, anchor_y + y + 1):
                return (anchor_x, anchor_y)
        anchor_y += 1


def remove_layer(arena: Arena, layer: int) -> None:
    arena.pop(layer)
    new_layer = [True for _ in range(len(arena[0]))]
    arena.insert(0, new_layer)   # neviem ako mi to preslo veritou lol


def strike(arena: Arena) -> int:  # Laci_Strike😎
    strikes = 0
    length = -len(arena)
    for i in range(0, length, -1):
        while False in arena[i] and True not in arena[i]:
            strikes += 1
            remove_layer(arena, i)
    return strikes


def poll_event() -> int:
    return int(input("what's your next move?"))


def do_poll_event(arena: Arena, block: Block, num: int, anchor: Anchor) \
        -> Tuple[Block, Anchor, int]:
    anchor_x, anchor_y = anchor
    anchors = {LEFT: (anchor_x-1, anchor_y),
               RIGHT: (anchor_x+1, anchor_y),
               DOWN: (anchor_x, anchor_y+1)}

    new_anchor = anchors.get(num, anchor)
    new_block = block

    if num == ROTATE_CCW or num == ROTATE_CW:
        new_block = rotate_ccw(block) if num == ROTATE_CCW \
                    else rotate_cw(block)

    if num in range(5):
        if check_position(arena, new_block, anchor, num):
            remove_block(arena, block, (anchor_x, anchor_y))
            insert_block(arena, new_block, new_anchor)
            return new_block, new_anchor, CONTINUE
        return block, anchor, CONTINUE if num < 4 else NEXT_BLOCK

    if num == DROP:
        new_x, new_y = get_drop_anchor(arena, block, anchor)
        remove_block(arena, block, (anchor_x, anchor_y))
        insert_block(arena, block, (new_x, new_y))
        return block, anchor, NEXT_BLOCK

    if num == QUIT:
        return block, anchor, QUIT_GAME
    return block, anchor, QUIT_GAME


def insert_new_block(arena: Arena, block: Block) -> Tuple[Block, Anchor, int]:
    x, y = allign_anchor(arena, block)
    if check_position(arena, block, (x, y), NEW_BLOCK):
        insert_block(arena, block, (x, y))
        return block, (x, y), CONTINUE
    return block, (x, y), QUIT_GAME


def play(arena: Arena) -> int:
    score = 0
    block = next_block()
    block, anchor, status = insert_new_block(arena, block)
    draw(arena, score)
    while status != QUIT_GAME:
        block, anchor, status = do_poll_event(arena, block,
                                              poll_event(), anchor)
        if status == NEXT_BLOCK:
            strikes = strike(arena)
            score += strikes ** 2
            block = next_block()
            block, anchor, status = insert_new_block(arena, block)
        draw(arena, score)
    return score
