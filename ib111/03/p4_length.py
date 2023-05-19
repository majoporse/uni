# Napište čistou funkci, která dostane na vstup seznam bodů v rovině
# (tj. seznam dvojic čísel) a vrátí délku lomené čáry, která těmito
# body prochází (tzn.  takové, která vznikne spojením každých dvou
# sousedních bodů seznamu úsečkou).

# Například seznam ‹[(0, 0), (1, 0), (1, 1), (2, 1)]› definuje tuto
# lomenou čáru:
#
#       (1, 1) ┌───▶(2, 1)
#              │
#    (0, 0)╶───┘(1, 0)
#
# složenou ze tří segmentů (úseček) velikosti 1. Její délka je 3.


def point_distance(a, b):
    x, y = a
    x1, y1 = b
    return ((x-x1)**2+(y-y1)**2)**(1/2)


def length(points):
    distance = 0
    for i in range(len(points)-1):
        distance += point_distance((points[i]), (points[i+1]))
    return distance


def main():
    assert length([(0, 1), (1, 1), (1, 2)]) == 2
    assert length([(0, 0)]) == 0
    assert length([]) == 0
    assert length([(3, 5), (3, 15), (4, 15), (4, 0), (0, 0)]) == 30
    assert length([(0, 0), (3, 4)]) == 5
    assert length([(0, 0), (3, 4), (3, 7)]) == 8


if __name__ == "__main__":
    main()
