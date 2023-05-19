#include <map>
#include <set>
#include <cassert>

/* † Budeme opět pracovat s orientovaným grafem – tentokrát budeme
 * hledat cykly. Existuje na výběr několik algoritmů, ty založené na
 * prohledávání do hloubky jsou nejjednodušší. Graf je zadaný jako
 * hodnota typu ‹std::multimap› – více se o této reprezentaci
 * dozvíte v ukázce ‹d5_bfs›.
 *
 * Čistá funkce ‹is_dag› nechť vrátí ‹false› právě když ‹g› obsahuje
 * cyklus. Pozor, graf nemusí být souvislý. */

using graph = std::multimap< int, int >;

bool dfs(const graph g, int pos, std::set<int> &visited, std::set<int> &path){
    
    visited.insert(pos);
    path.insert(pos);
    
    for (auto it = g.lower_bound(pos),
              it2 = g.upper_bound(pos); it != it2; ++it){
            int neigh = (*it).second;

            if  (!visited.contains(neigh) && dfs(g, neigh, visited, path))
                    return true;

            else if (path.contains(neigh))
                return true;
    }

    path.erase(pos);
    return false;
}

bool is_dag( const graph &g ){
    std::set<int>visited;
    
    for (auto it = g.begin(); it != g.end(); ++it) {

        if (visited.contains((*it).first))
            continue;

        for (auto it2 = g.upper_bound((*it).first); it != it2; ++it){
            
            if (visited.contains((*it).second))
                continue;

            std::set<int>path = {};
            if (dfs(g, (*it).first, visited, path))
                return false;
        }
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
