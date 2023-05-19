#include <vector>
#include <cassert>

/* Na vstupu dostanete posloupnost celočíselných hodnot (jako
 * instanci kontejneru ‹std::vector›). Vaším úkolem je rozdělit je
 * na kratší posloupnosti tak, že každá posloupnost je nejkratší
 * možná, ale zároveň je její součet alespoň ‹sum›. Výjimku tvoří
 * poslední posloupnost, pro kterou nemusí nutně existovat potřebné
 * prvky.
 *
 * Pořadí prvků musí být zachováno, tzn. zřetězením všech
 * posloupností na výstupu musí vzniknout původní posloupnost
 * ‹numbers›. */

auto minsum( const std::vector< int > &numbers, int sum ){
    std::vector< std::vector< int > > res = {};
    auto it = numbers.begin();

    while ( it != numbers.end()){
        std::vector< int > cur = {};

        for (int count = 0; it < numbers.end(); ++it){
            cur.emplace_back(*it);
            count += *it;

            if (count >= sum){
                
                ++it;
                break;
            }
        }
        res.push_back(cur);
    }

    return res;
}

int main()
{
    assert(( minsum( std::vector{ 1, 2 }, 1 ) ==
               std::vector{ std::vector{ 1 }, { 2 } } ));
    assert(( minsum( std::vector{ 1, 2, 3, 4 }, 3 ) ==
             std::vector{ std::vector{ 1, 2 }, { 3 }, { 4 } } ));

    return 0;
}
