#include <map>
#include <vector>
#include <cassert>
#include <queue>
#include <set>


/* Rozhodněte, zda je zadaný neorientovaný graf bipartitní (tzn.
 * jeho vrcholy lze rozdělit do dvou množin ⟦A, B⟧ tak, že každá
 * hrana má jeden vrchol v ⟦A⟧ a jeden v ⟦B⟧). Protože graf je
 * neorientovaný, seznamy sousedů na vstupu jsou symetrické. */

using edges = std::vector< int >;
using graph = std::map< int, edges >;

/** Recenze
 ** Dekompozice: hloubka větvení je tady už docela velká.
 ** Délka kodu téměř na hraně. Ale pro tento konrétní
 ** algoritmus mi to přijde optimální, sám bych si nědělal pomocné
 ** fce.
 **
 ** Jména proměnných: spokojenost, zizag si budu pamatovat
 **
 ** Algoritmus: ok, já jsem hloupě spočítal zigzag signaturu u všech,
 ** až pak hledal nesrovnalost..
 **
 ** Řízení toku: v kodu pushuješ následníka jen v případě, že není
 ** visited, tj. podmínka po vybrání is visited je k ničemu
 **
 ** Hodně rychle jsem se v kodu zorientoval.
 ** Dobrá práce **/

bool is_bipartite( const graph &g ){
    if(g.empty()){
        return true;
    }
    std::map<int, bool>zigzag = {};
    std::set<int>visited = {};
    std::queue<int>q = {};

    for(auto &[key, val] : g){
        zigzag[key] = false;
        q.push(key);
    }
    
    while (!q.empty()){

        int cur = q.front();
        q.pop();

        if(visited.contains(cur))
            continue;

        visited.insert(cur);
        

        for (int p : g.at(cur)){
            
            if (visited.contains(p)){
                if (zigzag.at(cur) == zigzag.at(p))
                    return false;
                continue;
            }
            zigzag[p] = !zigzag.at(cur);
            q.push(p);

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