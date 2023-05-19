#include <set>
#include <vector>
#include <cassert>

/* Rozložte zadaný neorientovaný graf na souvislé komponenty
 * (výsledné komponenty budou reprezentované množinou svých
 * vrcholů). Graf je zadaný jako symetrická matice sousednosti.
 * Vrcholy jsou očíslované od 1 do ⟦n⟧, kde ⟦n⟧ je velikost vstupní
 * matice.
 *
 * V grafu je hrana ⟦{u, v}⟧ přítomna právě tehdy, je-li na řádku
 * ⟦u⟧ ve sloupci ⟦v⟧ hodnota ‹true›. */

using graph = std::vector< std::vector< bool > >;

using component = std::set< int >;
using components = std::set< component >;

/** Recenze
 ** Dekompozice - ok
 ** Jména proměnných - je co zlepšit, viz. dále
 ** Mám problém se zorientovat ve splěti iterátorů
 ** Algoritmus - spokojenost
 ** Dekompozice ok
 ** Hodí se pár komentářů, ale celkově to ujde
 ** Zbytek v kodu **/

/** Co znamená i? pojmenoval bych například vertice
 ** osobně bych nereturnoval vstupně výstupní proměnnou, ale ok **/
component dfs(int i,const graph &g, std::set< int > &res, std::vector< bool > &visited)
{
     visited[i] = true;
     res.insert(i+1);

     for(auto it = g[i].begin(); it != g[i].end(); ++it){
          int cur = it - g[i].begin();

          if(!g[i][cur])
               continue;

          if (!visited[cur]){
               dfs(cur, g, res, visited);
          }
     }
     return res;
}

components decompose( const graph &g ){
     
     /** = {} zbytečné **/
     components res = {};
     /** false je default, není třeba psát **/
     std::vector< bool > v(g.size(), false);
     /** nechápu existenci této proměnné, stačí používat v **/
     std::vector< bool > &visited = v;
     
     for (std::size_t i = 0; i < g.size(); ++i){
          if (v[i]) {
               continue;
          }
          std::set<int> cur = {};
          /** nechápu existenci této proměnné, stačí používat cur **/
          std::set<int> &curl = cur;
          res.insert(dfs(i, g, curl, visited));
     }
     return res;
}

int main()
{
    graph g_1{ { 0, 1, 1, 0 },
               { 1, 0, 0, 0 },
               { 1, 0, 0, 0 },
               { 0, 0, 0, 0 } },

          g_2{ { 0, 1, 0, 0 },
               { 1, 0, 1, 0 },
               { 0, 1, 0, 1 },
               { 0, 0, 1, 0 } },

          g_3{ { 0, 1, 0, 0 },
               { 1, 0, 0, 0 },
               { 0, 0, 0, 1 },
               { 0, 0, 1, 0 } },

          g_4{ { 0, 0, 0, 0 },
               { 0, 0, 0, 1 },
               { 0, 0, 0, 0 },
               { 0, 1, 0, 0 } },

          g_5{ { 0, 0, 0, 0 },
               { 0, 0, 0, 0 },
               { 0, 0, 0, 0 },
               { 0, 0, 0, 0 } },

          g_6{ { 0, 1, 1, 0 },
               { 1, 0, 1, 0 },
               { 1, 1, 0, 0 },
               { 0, 0, 0, 0 } },

          g_7{ { 0, 1, 1, 1 },
               { 1, 0, 1, 1 },
               { 1, 1, 0, 1 },
               { 1, 1, 1, 0 } };

    components c_1{ { 1, 2, 3 }, { 4 } },
               c_2{ { 1, 2, 3, 4 } },
               c_3{ { 1, 2 }, { 3, 4 } },
               c_4{ { 1 }, { 2, 4 }, { 3 } },
               c_5{ { 1 }, { 2 }, { 3 }, { 4 } },
               c_6{ { 1, 2, 3 }, { 4 } },
               c_7{ { 1, 2, 3, 4 } };

    assert( decompose( g_1 ) == c_1 );
    assert( decompose( g_2 ) == c_2 );
    assert( decompose( g_3 ) == c_3 );
    assert( decompose( g_4 ) == c_4 );
    assert( decompose( g_5 ) == c_5 );
    assert( decompose( g_6 ) == c_6 );
    assert( decompose( g_7 ) == c_7 );

    return 0;

    // clang-tidy: -modernize-use-bool-literals
}
