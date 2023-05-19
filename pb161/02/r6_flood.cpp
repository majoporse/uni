#include <vector>
#include <cassert>

/* In this exercise, we will implement a simple flood fill: in its
 * most common formulation, this is an algorithm which:
 *
 *  1. is given a bitmap (a rectangular grid of pixels),
 *  2. a starting position in the grid,
 *  3. a fill colour,
 *
 * and changes the entire contiguous single-colour area that
 * contains the starting position to use the fill colour.
 *
 * We will do a monochromatic version of the same (pixels are either
 * white or black, or rather 0 or 1) and instead of modifying the
 * input grid, or building a new one, we will simply count how many
 * cells change colour. Example (empty cells are the ones with value
 * 0, shaded cells have value 1; the starting position was 1, 3):
 *
 *   ┌───┬───┬───┬───┬───┬───┐  ┌───┬───┬───┬───┬───┬───┐
 * 0 │   │   │   │░░░│   │   │  │░░░│░░░│░░░│░░░│   │   │
 *   ├───┼───┼───┼───┼───┼───┤  ├───┼───┼───┼───┼───┼───┤
 * 1 │   │░░░│   │░░░│   │   │  │░░░│░░░│░░░│░░░│   │   │
 *   ├───┼───┼───┼───┼───┼───┤  ├───┼───┼───┼───┼───┼───┤
 * 2 │   │░░░│░░░│░░░│░░░│░░░│  │░░░│░░░│░░░│░░░│░░░│░░░│
 *   ├───┼───┼───┼───┼───┼───┤  ├───┼───┼───┼───┼───┼───┤
 * 3 │   │ × │   │░░░│   │   │  │░░░│░×░│░░░│░░░│░░░│░░░│
 *   ├───┼───┼───┼───┼───┼───┤  ├───┼───┼───┼───┼───┼───┤
 * 4 │░░░│░░░│░░░│   │░░░│░░░│  │░░░│░░░│░░░│░░░│░░░│░░░│
 *   ├───┼───┼───┼───┼───┼───┤  ├───┼───┼───┼───┼───┼───┤
 * 5 │   │   │   │   │░░░│   │  │░░░│░░░│░░░│░░░│░░░│   │
 *   └───┴───┴───┴───┴───┴───┘  └───┴───┴───┴───┴───┴───┘
 *     0   1   2   3   4   5      0   1   2   3   4   5
 *
 * Notice that the flood also proceeds along diagonals (i.e. from
 * position (2, 3) to (3, 4) and then further to (4, 3)). The grid
 * is given as a single, flat vector and a width. You can assume
 * that the size of the vector is evenly divisible by the given
 * ‹width›. The ‹x0› and ‹y0› give the starting position, while the
 * last argument, ‹fill›, the colour (0 or 1) to use. */

using grid = std::vector< bool >;

int flood( const grid &pixels, int width,
           int x0, int y0, bool fill );

int main()
{
    // clang-tidy: -modernize-use-bool-literals

    grid small{ 0, 0, 1,
                1, 1, 1,
                1, 0, 0 };

    assert( flood( small, 3, 0, 0, true  ) == 2 );
    assert( flood( small, 3, 1, 0, true  ) == 2 );
    assert( flood( small, 3, 2, 0, true  ) == 0 );
    assert( flood( small, 3, 2, 0, false ) == 5 );
    assert( flood( small, 3, 1, 2, true  ) == 2 );

    grid ex{ 0, 0, 0, 1, 0, 0, 0,
             0, 1, 0, 1, 0, 0, 0,
             0, 1, 1, 1, 1, 1, 1,
             0, 0, 0, 1, 0, 0, 0,
             1, 1, 1, 0, 1, 1, 1,
             0, 0, 0, 0, 1, 1, 1 };

    assert( flood( ex, 7, 1, 3, true  ) == 17 );
    assert( flood( ex, 7, 1, 3, false ) ==  0 );
    assert( flood( ex, 7, 1, 3, false ) ==  0 );
    assert( flood( ex, 7, 5, 0, true  ) ==  6 );

    return 0;
}
