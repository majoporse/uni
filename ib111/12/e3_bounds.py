from typing import Optional, Tuple


class Tree:
    def __init__(self, value: int, left: Optional['Tree'] = None,
                 right: Optional['Tree'] = None) -> None:
        self.value = value
        self.left = left
        self.right = right


# Napište čistou funkci ‹get_bounds›, která nalezne minimální a
# maximální hodnotu v zadaném neprázdném stromě.

def get_bounds(tree: Tree) -> Tuple[int, int]:
    pass


def main() -> None:
    assert get_bounds(Tree(1)) == (1, 1)
    assert get_bounds(Tree(1, Tree(2), Tree(3))) == (1, 3)
    assert get_bounds(Tree(-1, Tree(2), Tree(-3))) == (-3, 2)
    assert get_bounds(
        Tree(0, Tree(-1, Tree(-19, Tree(0)), Tree(5)),
             Tree(4, Tree(8, None, Tree(3)),
                  Tree(26, Tree(-3, Tree(19), Tree(5)),
                       Tree(2))))) == (-19, 26)
    assert get_bounds(
        Tree(-50, Tree(-1, Tree(-19, Tree(0)), Tree(5)),
             Tree(4, Tree(8, None, Tree(3)),
                  Tree(26, Tree(-3, Tree(19), Tree(5)),
                       Tree(2))))) == (-50, 26)
    assert get_bounds(
        Tree(100, Tree(-1, Tree(-19, Tree(0)), Tree(5)),
             Tree(4, Tree(8, None, Tree(3)),
                  Tree(26, Tree(-3, Tree(19), Tree(5)),
                       Tree(2))))) == (-19, 100)
    assert get_bounds(
        Tree(0, Tree(-1, Tree(-19, Tree(0)), Tree(5)),
             Tree(4, Tree(80, None, Tree(3)),
                  Tree(26, Tree(-3, Tree(19), Tree(5)),
                       Tree(-22))))) == (-22, 80)
    assert get_bounds(
        Tree(-1, Tree(-1, Tree(-19, Tree(-3)), Tree(-5)),
             Tree(-4, Tree(-8, None, Tree(-3)),
                  Tree(-26, Tree(-3, Tree(-19), Tree(-5)),
                       Tree(-2))))) == (-26, -1)


if __name__ == '__main__':
    main()
