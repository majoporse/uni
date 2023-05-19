#include <map>
#include <vector>
#include <cassert>

/* Rozhodněte, zda je zadaný neorientovaný graf bipartitní (tzn.
 * jeho vrcholy lze rozdělit do dvou množin ⟦A, B⟧ tak, že každá
 * hrana má jeden vrchol v ⟦A⟧ a jeden v ⟦B⟧). Protože graf je
 * neorientovaný, seznamy sousedů na vstupu jsou symetrické. */

using edges = std::vector<int>;
using graph = std::map<int, edges>;

bool DFS(const graph& g, int vertex, std::map<int, int>& colors)
{
    for (auto next : g.at(vertex))
    {
        if (colors[next] == 0)
        {
            colors[next] = -colors[vertex];
            if (!DFS(g, next, colors))
            {
                return false;
            }
        }
        else if (colors[next] != -colors[vertex])
        {
            return false;
        }
    }

    return true;
}

bool is_bipartite(const graph &g)
{
    std::map<int, int> colors;

    for (const auto& [vertex, e] : g)
    {
        colors.insert({vertex, 0}); // 0 = unvisited, 1 = red, -1 = blue
    }

    for (const auto& [vertex, e] : g)
    {
        if (colors[vertex] == 0)
        {
            colors[vertex] = 1;
            if (!DFS(g, vertex, colors))
            {
                return false;
            }
        }
    }

    return true;
}

int main()
{
    assert(  is_bipartite( graph() ) );
    assert(  is_bipartite( graph{ { 1, {} } } ) );
    assert(  is_bipartite( graph{ { 1, { 2 } }, { 2, { 1 } } } ) );
    assert(  is_bipartite( graph{ { 1, {} }, { 2, {} } } ) );

    graph g{ { 1, { 2, 3 } }, { 2, { 1, 3 } }, { 3, { 1, 2 } } };
    assert( !is_bipartite( g ) );

    graph h{ { 1, { 2 } }, { 2, { 1, 3 } }, { 3, { 2 } } };
    assert( is_bipartite( h ) );

    graph i{ { 1, { 2, 3 } }, { 2, { 1 } }, { 3, { 1 } } };
    assert( is_bipartite( i ) );

    graph j{ { -1, { -2 } }, { -2, { -1 } },
             { 1, { 2, 3 } }, { 2, { 1, 3 } }, { 3, { 1, 2 } } };
    assert( !is_bipartite( j ) );

    return 0;
}
