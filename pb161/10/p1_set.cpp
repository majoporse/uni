#include <cassert>
#include <ranges>
#include <set>
#include <algorithm>

/* Implementujte množinu libovolných celých čísel, s těmito
 * operacemi:
 *
 *  • sjednocení operátorem ‹|›,
 *  • průnik operátorem ‹&›,
 *  • rozdíl operátorem ‹-›,
 *  • uspořádání inkluzí relačními operátory.
 *
 * Všechny výše uvedené operace musí být nejvýše lineární v součtu
 * velikostí vstupních množin. Typ ‹set› doplňte metodami ‹add›
 * (přidá prvek) a ‹has› (ověří přítomnost prvku), které mají
 * nejvýše logaritmickou složitost. */

struct set{
    std::set<int> data;
    void add(int i) {data.emplace(i);}
    bool has(int i) const {return data.contains(i);}
    set(const set&) = default;
    set(std::set<int>&& new_data): data{new_data} {}
    set& operator=(const set&) = default;
    set() = default;
    friend set operator|(set a, const set&b) {
        a.data.insert(b.data.begin(), b.data.end());
        return a;
    }
    friend set operator&(const set&a, const set&b) {
        std::set<int> common_data;
        std::set_intersection(a.data.begin(),a.data.end(),
                              b.data.begin(),b.data.end(),
                              std::inserter(common_data, common_data.begin()));
        return {std::move(common_data)};
    }

    friend set operator-(const set &a, const set&b) {
        std::set<int> n_data;
        std::ranges::set_difference(a.data, b.data, std::inserter(n_data,n_data.begin()));
        return {std::move(n_data)};

    }

    friend bool operator==(const set &a, const set&b){
        std::set<int> res;
        std::ranges::set_symmetric_difference(a.data, b.data, std::inserter(res, res.begin()));
        return res.empty();
    }
    friend auto operator<=>(const set &a, const set&b) {
        if (a == b) return std::partial_ordering::equivalent;
        if (std::ranges::includes(a.data, b.data)) return std::partial_ordering::greater;
        if (std::ranges::includes(b.data, a.data)) return std::partial_ordering::less;
        return std::partial_ordering::unordered;
    }
};

int main()
{
    set a, b;
    a.add( 1 ), a.add( 2 ), a.add( 5 ), a.add( -3 );
    b.add( 1 ), b.add( -3 ), b.add( -1000 ), b.add( 1 << 20 );

    const set x = a, y = b;

    const set u = x | y;
    const set i = x & y;
    const set d = x - y;

    assert(  u.has( 1 ) );
    assert(  i.has( 1 ) );
    assert( !d.has( 1 ) );

    assert(  u.has( 2 ) );
    assert( !i.has( 2 ) );
    assert(  d.has( 2 ) );
    assert( !i.has( -1000 ) );
    assert(  u.has( -1000 ) );
    assert( !d.has( -1000 ) );
    assert(  u.has( 1 << 20 ) );
    assert( !i.has( 1 << 20 ) );

    assert( !( a <= b ) );
    assert( !( b <= a ) );
    assert( a <= u );
    assert( u >  a );
    assert( b <= u );
    assert( i <= u );
    assert( i <  u );
    assert( i <= a );
    assert( i <= b );
    assert( u == u );
    assert( d <= u );
    assert( d <= a );
    assert( !( d <= b ) );
    assert( u <= u );

    return 0;
}
