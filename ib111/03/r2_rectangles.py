# Napište (čistou) funkci, která jako parametr dostane seznam
# obdélníků a vrátí seznam obdélníků, které se překrývají s nějakým
# jiným. Obdélník samotný je reprezentovaný dvěma body (levým dolním
# a pravým horním rohem, a má nenulovou výšku i šířku). Obdélníky
# budeme zapisovat jako dvojice dvojic – ‹((0, 0), (1, 2))›
# například reprezentuje tento obdélník:
#
#           ┌───┐(1, 2)
#           │   │
#           │   │
#     (0, 0)└───┘
#
# Mohl by se Vám hodit predikát, který je pravdivý, když se dva
# obdélníky překrývají:

def has_overlap(a, b):
    ax1,ay1 = a[0]
    ax2,ay2 = a[1]
    bx1,by1 = b[0]
    bx2,by2 = b[1]
    
    return (bx1 or bx2 in range(ax1, ax2+1) and by1 or by2 in range(ay1,ay2+1))\
           and (bx2 or by1 not in  range(ax1, ax2+1) and by2 or by1 not in  range(ay1,ay2+1))
            
    
        
    


def filter_overlapping(rectangles):
    pass


def main():
    r1 = ((1, 1), (2, 2))
    r2 = ((0, 0), (2, 2))
    r3 = ((-2, -2), (-1, -1))
    r4 = ((10, 15), (25, 35))
    
    has_overlap(r1, r2)

#     assert filter_overlapping([]) == []
#     assert filter_overlapping([r1]) == []
#     assert filter_overlapping([r1, r1]) == [r1, r1]
#     assert filter_overlapping([r1, r2]) == [r1, r2]
#     assert filter_overlapping([r2, r1]) == [r2, r1]
# 
#     assert filter_overlapping([r3, r2, r1, r4]) == [r2, r1]
#     assert filter_overlapping([r2, ((1, 10), (10, 20))]) == []
#     assert filter_overlapping([((15, 0), (17, 8)),
#                                ((1, 10), (10, 20))]) == []
#     l2 = [((0, 0), (2, 2)),
#           ((1, 1), (10, 10)),
#           ((9, 9), (11, 11))]
#     assert filter_overlapping(l2) == l2


if __name__ == "__main__":
    main()
