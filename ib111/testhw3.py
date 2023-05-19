from math import floor

def new_arena(cols, rows):
    arena = []
    for row in range(rows):
        current_row = []
        for col in range(cols):
            current_row.append(True)
        arena.append(current_row)
    return arena

myarena = new_arena(6,6)

def allign_horizontally(arena, block):
    x_min = 0
    x_max = 0
    for (x,y) in block:
        if x < x_min:
            x_min = x
        if x > x_max:
            x_max = x
    return floor((len(arena)+1 - x_max - x_min )/2)



print(allign_horizontally(myarena, [(-2,0),(-1,0),(0,0)]))

a = [[True,True,True,True]]