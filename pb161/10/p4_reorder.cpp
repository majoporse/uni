#include <algorithm>
#include <cassert>
#include <vector>
#include <ranges>
#include <numeric>
#include <type_traits>
#include <array>

/* Napište podprogram ‹reorder( s, weight )›, který pro zadanou
 * posloupnost ‹s› a funkci ‹weight› na místě přeuspořádá ‹s› tak,
 * že pro ⟦u < w⟧ budou prvky s váhou ⟦u⟧ předcházet prvkům s váhou
 * ⟦w⟧. Zároveň pro prvky se stejnou váhou platí, že se objeví ve
 * stejném pořadí, v jakém byly v původní posloupnosti ‹s›.
 *
 * Podprogram musí pracovat v čase nejvýše ⟦O(k⋅n)⟧ kde ⟦k⟧ je počet
 * různých vah, které se objeví na vstupu, a ⟦n⟧ je délka
 * posloupnosti ‹s›. Je také povoleno využít lineární množství
 * dodatečné paměti. */

void reorder(auto &a, auto fun){
    std::vector<int> indexes(a.size(), 0);
    std::iota(indexes.begin(), indexes.end(), 0 );

    std::vector<int> i_set;
    for (int i: indexes){
        auto x = fun(a[i]);
        auto it = std::ranges::lower_bound(i_set, i, [fun, &a, &x]( int j, int ) { return x > fun(a[j]); } );
        if (it == i_set.end() || fun(a[*it]) != x){
            i_set.insert(it, i);
        }
    }

    std::decay_t<decltype(a)> n;
    for (auto i: i_set){
        auto x = fun(a[i]);
        for (auto &elem : a){
            if (x == fun(elem))
                n.emplace_back(std::move(elem));
        }
    }
    a = std::move(n);
}

int main()
{
    std::vector a{ 1, 3, 4, 2 };

    reorder( a, []( int x ) { return x / 2; } );
    assert(( a == std::vector{ 1, 3, 2, 4 } ));
    reorder( a, []( int x ) { return -x / 2; } );
    assert(( a == std::vector{ 4, 3, 2, 1 } ));

    struct token
    {
        int value;

        token( int v ) : value( v ) {}

        token( const token & ) = delete;
        token( token && ) = default;

        token &operator=( const token & ) = delete;
        token &operator=( token && ) = default;

        bool operator==( const token & ) const = default;
    };

    struct weight
    {
        int value;
        weight( int v ) : value( v ) {}

        weight( const weight & ) = delete;
        weight( weight && ) = delete;

        weight &operator=( const weight & ) = delete;
        weight &operator=( weight && ) = delete;

        bool operator==( const weight &o ) const = default;
        auto operator<=>( const weight &o ) const = default;
    };

    std::vector< token > x, y;
    int ops = 0;
    int count = 1024 * 512;

    for ( int i = 0; i < count; ++i )
    {
        x.emplace_back( i );
        y.emplace_back( i );
    }

    auto one_way = [&]( const auto &t )
    {
        ++ops;
        return weight( -t.value / count );
    };

    auto two_way = [&]( const auto &t )
    {
        ++ops;
        return weight( -t.value / ( count / 2 ) );
    };

    reorder( x, one_way );
    assert( ops <= 4 * count );
    assert( x == y ); /* no change */
    ops = 0;

    reorder( x, two_way );
    assert( ops <= 8 * count );
    assert( x != y );
    ops = 0;

    assert( x.front().value == count / 2 );
    assert( x.back().value == count / 2 - 1 );
    assert( x[ count / 2 ].value == 0 );
    assert( x[ count / 2 - 1 ].value == count - 1 );

    return 0;
}
