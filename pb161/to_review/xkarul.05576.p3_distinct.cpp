#include <cassert>
#include <vector>
#include <algorithm>
#include <iterator>

/* Napište čistou, generickou funkci ‹distinct( s )›, která spočítá,
 * kolik různých prvků se objevuje ve vzestupně seřazené
 * posloupnosti ‹s›. Zadaná posloupnost je hodnota typu, který
 * poskytuje metody ‹begin› a ‹end›; výsledné iterátory lze
 * efektivně (v konstantním čase) posouvat o libovolný počet pozic
 * (např. funkcí ‹std::next›) a lze také efektivně získat vzdálenost
 * dvou iterátorů (např. funkcí ‹std::distance›). Prvky nemusí být
 * možné kopírovat, ale lze je libovolně srovnávat a přesouvat.
 *
 * Funkce musí pracovat v čase nejvýše ⟦O(k⋅\log(n))⟧, kde ⟦k⟧ je
 * počet různých prvků (výsledek volání ‹distinct›) a ⟦n⟧ je délka
 * vstupní posloupnosti. */

int distinct(auto&& cont){
    auto it = cont.begin();
    int i = 0;
    int count = 0;
    while (it != cont.end()){
        it++;
        auto old = it;
        it = std::upper_bound(cont.begin(), cont.end(), cont[i]);
        i += std::distance(old, it) + 1;
        count++;
    }
    return count;
}

int distinct(auto& cont){
    auto it = cont.begin();
    int i = 0;
    int count = 0;
    while (it != cont.end()){
        it++;
        auto old = it;
        it = std::upper_bound(cont.begin(), cont.end(), cont[i]);
        i += std::distance(old, it) + 1;
        count++;
    }
    return count;
}

int main()
{
    assert(( distinct( std::vector{ 1, 1, 2, 2 } ) == 2 ));
    assert(( distinct( std::vector{ 1, 3, 3, 4 } ) == 3 ));

    struct token
    {
        int value;
        int *ops;

        token( int v, int &ops ) : value( v ), ops( &ops ) {}

        token( const token & ) = delete;
        token( token && ) = default;

        token &operator=( const token & ) = delete;
        token &operator=( token && ) = default;

        bool operator==( const token &o ) const
        {
            ++ *ops;
            return value == o.value;
        }

        auto operator<=>( const token &o ) const
        {
            ++ *ops;
            return value <=> o.value;
        }
    };

    std::vector< token > x;
    int ops = 0;

    for ( int i = 0; i < 1024; ++i )
        x.emplace_back( i / 128, ops );

    assert( distinct( x ) == 8 );
    assert( ops <= 160 );

    return 0;
}
