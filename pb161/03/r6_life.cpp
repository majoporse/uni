#include <set>
#include <utility>
#include <cassert>

/* The game of life is a 2D cellular automaton: cells form a 2D
 * grid, where each cell is either alive or dead. In each generation
 * (step of the simulation), the new value of a given cell is
 * computed from its value and the values of its 8 neighbours in the
 * previous generation. The rules are as follows:
 *
 * │ state │ alive neigh. │ result │
 * ├───────┼──────────────┼────────┤
 * │ alive │          0–1 │   dead │
 * │ alive │          2–3 │  alive │
 * │ alive │          4–8 │   dead │
 * │┄┄┄┄┄┄┄│┄┄┄┄┄┄┄┄┄┄┄┄┄┄│┄┄┄┄┄┄┄┄│
 * │  dead │          0–2 │   dead │
 * │  dead │            3 │  alive │
 * │  dead │          4-8 │   dead │
 *
 * An example of a short periodic game:
 *
 *  ┌───┬───┬───┐   ┌───┬───┬───┐   ┌───┬───┬───┐
 *  │   │   │   │   │   │ ○ │   │   │   │   │   │
 *  ├───┼───┼───┤   ├───┼───┼───┤   ├───┼───┼───┤
 *  │ ○ │ ○ │ ○ │ → │   │ ○ │   │ → │ ○ │ ○ │ ○ │
 *  ├───┼───┼───┤   ├───┼───┼───┤   ├───┼───┼───┤
 *  │   │   │   │   │   │ ○ │   │   │   │   │   │
 *  └───┴───┴───┘   └───┴───┴───┘   └───┴───┴───┘
 *
 * Write a function which, given a set of live cells, computes the
 * set of live cells after ‹n› generations. Live cells are given
 * using their coordinates in the grid, i.e. as ‹(x, y)› pairs.
 */

using cell = std::pair< int, int >;
using grid = std::set< cell >;

grid life( const grid &, int );

int main()
{
    assert( life( {}, 3 ).empty() );

    assert( life( { { 0, 0 } }, 1 ).empty() );
    grid block = { { 0, 0 }, { 1, 1 }, { 0, 1 }, { 1, 0 } };

    grid blinker_0 = { { 0, -1 }, { 0, 0 }, { 0, 1 } };
    grid blinker_1 = { { -1, 0 }, { 0, 0 }, { 1, 0 } };
    grid glider    = blinker_1;

    glider.emplace( 1, -1 );
    glider.emplace( 0, -2 );

    for ( int i = 0; i < 20; ++ i )
        assert( life( block, i ) == block );

    for ( int i = 0; i < 20; ++ i )
    {
        auto expect = i % 2 == 0 ? blinker_0 : blinker_1;
        assert( life( blinker_0, i ) == expect );
    }

    for ( int i = 0; i < 40; i += 4 )
    {
        grid expect;

        for ( auto [ x, y ] : glider )
            expect.emplace( x + i / 4, y + i / 4 );

        assert( life( glider, i ) == expect );
    }

    return 0;
}
