#include <algorithm>
#include <cassert>
#include <map>
#include <set>

/* † Budeme opět pracovat s orientovaným grafem – tentokrát budeme
 * hledat cykly. Existuje na výběr několik algoritmů, ty založené na
 * prohledávání do hloubky jsou nejjednodušší. Graf je zadaný jako
 * hodnota typu ‹std::multimap› – více se o této reprezentaci
 * dozvíte v ukázce ‹d5_bfs›.
 *
 * Čistá funkce ‹is_dag› nechť vrátí ‹false› právě když ‹g› obsahuje
 * cyklus. Pozor, graf nemusí být souvislý. */

using graph = std::multimap< int, int >;

bool has_cycle(const graph &g, int vertex, std::set<int> current_path)
{
    if (auto [_, inserted] = current_path.insert(vertex); !inserted) {
        return true;
    }

    for (auto [it, end] = g.equal_range(vertex); it != end; it++) {
        if (has_cycle(g, it->second, current_path)) {
            return true;
        }
    }

    return false;
}

bool is_dag(const graph &g)
{
    std::set<int> explored;
    std::set<int> current_path;

    for (auto it = g.begin(); it != g.end(); it = g.upper_bound(it->first)) {
        if (auto [_, inserted] = explored.insert(it->first); inserted
                && has_cycle(g, it->first, current_path)) {
            return false;
        }

        explored.insert(current_path.begin(), current_path.end());
    }

    return true;
}

int main()
{
    assert(  is_dag( graph{ { 1, 2 } } ) );
    assert( !is_dag( graph{ { 1, 1 } } ) );
    assert(  is_dag( graph{ { 1, 2 }, { 1, 3 }, { 2, 3 } } ) );

    graph g{ { 1, 2 }, { 1, 3 }, { 2, 4 }, { 2, 5 }, { 3, 4 } };
    assert( is_dag( g ) );

    graph h{ { 1, 2 }, { 1, 3 }, { 2, 4 }, { 2, 5 }, { 5, 1 } };
    assert( !is_dag( h ) );

    return 0;
}
