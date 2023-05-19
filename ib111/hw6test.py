def kokoc():
    with open('kakuro.txt') as file:
        lines = file.readlines()
        for i in range(len(lines.copy())):
            lines[i] = lines[i].split()
            for j, elem in enumerate(lines[i]):
                if elem == '.':
                    lines[i][j] = 0
                elif elem == '\\':
                    lines[i][j] = -1
                else:
                    lines[i][j] = [int(a) if a != '' else 0 for a in elem.split('\\') ] 
        print(lines)
kokoc()

# [['\\', '11\\', '8\\', '\\', '\\', '7\\', '16\\'],
#  ['\\16', '.', '.', '11\\', '\\4', '.', '.'],
#  ['\\7', '.', '.', '.', '7\\13', '.', '.'],
#  ['\\', '15\\', '21\\12', '.', '.', '.', '.'],
#  ['\\12', '.', '.', '.', '.', '4\\', '6\\'],
#  ['\\13', '.', '.', '\\6', '.', '.', '.'],
#  ['\\17', '.', '.', '\\', '\\6', '.', '.']]

res = {
        (11, (1, 0), False, 2),
        (8, (2, 0), False, 2),
        (7, (5, 0), False, 3),
        (16, (6, 0), False, 3),
        (16, (0, 1), True, 2),
        (11, (3, 1), False, 3),
        (4, (4, 1), True, 2),
        (7, (0, 2), True, 3),
        (7, (4, 2), False, 3),
        (13, (4, 2), True, 2),
        (15, (1, 3), False, 3),
        (21, (2, 3), False, 3),
        (12, (2, 3), True, 4),
        (12, (0, 4), True, 4),
        (4, (5, 4), False, 2),
        (6, (6, 4), False, 2),
        (13, (0, 5), True, 2),
        (6, (3, 5), True, 3),
        (17, (0, 6), True, 2),
        (6, (4, 6), True, 2)}
my_res = {(7, (4, 2), False, 3), (7, (0, 2), True, 3),
     (4, (5, 4), False, None), (11, (1, 0), False, 2),
     (13, (4, 2), True, None), (4, (4, 1), True, None),
     (11, (3, 1), False, 3), (21, (2, 3), False, None),
     (6, (6, 4), False, None), (6, (4, 6), True, None),
     (15, (1, 3), False, None), (17, (0, 6), True, 2),
     (6, (3, 5), True, None), (7, (5, 0), False, 3),
     (8, (2, 0), False, 2), (12, (2, 3), True, None),
     (12, (0, 4), True, 4), (16, (6, 0), False, 3),
     (16, (0, 1), True, 2), (13, (0, 5), True, 2)}
    