# Napište (čistou) funkci ‹survivors›, ktorá ze vstupního seznamu
# ‹objects› spočítá nový seznam, který bude obsahovat všechny prvky
# z ‹objects›, které jsou dostatečně vzdálené (dále než ‹radius›) od
# bodu ‹center›.
#
# Můžete si představit, že funkce implementuje herní mechaniku, kdy
# v bodě ‹center› nastala exploze tvaru koule, která zničila vše
# uvnitř poloměru ‹radius›, a funkce ‹survivors› vrátí všechny
# objekty, které explozi přežily.
#
# Prvky parametru ‹objects› a parametr ‹center› jsou uspořádané
# trojice, které reprezentují body v prostoru.

def distance(a, b):
    x, y, z = a
    x1, y1, z1 = b
    return ((x-x1)**2+(y-y1)**2+(z-z1)**2)**(1/2)

def survivors(objects, center, radius):
    survived = []
    for i in (objects):
        if distance(i, center) > radius:
            survived.append(i)
    return survived
                       
        
def main():
    assert survivors([(1, 0, 0), (2, 1, 1)], (0, 0, 0), 1) \
        == [(2, 1, 1)]
    assert survivors([(3, 2, 3)], (0, 0, 0), 1) == [(3, 2, 3)]
    assert survivors([(1, 1, 1), (0, 0, 1), (2, 0, 0)],
                     (0, 0, 0), 2) \
        == []
    assert survivors([], (0, 0, 0), 25) == []
    assert survivors([(4, 1, 1), (-2, 1, 1), (4, 4, 4)], (1, 1, 1), 3) \
        == [(4, 4, 4)]
    assert survivors([(0, 0, 1), (2, 0, 0), (1, 2, 1), (3, 0, 0)],
                     (1, 0, 1), 2) \
        == [(3, 0, 0)]
    assert survivors([(0, 3, 1), (2, 2, 0), (0, 2, 1), (3, 0, 1)],
                     (1, -2, 1), 4) \
        == [(0, 3, 1), (2, 2, 0), (0, 2, 1)]


if __name__ == "__main__":
    main()
