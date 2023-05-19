#include <cassert>
#include <set>
#include <tuple>
#include <initializer_list>

/* Navrhněte typ ‹numset›, kterého hodnoty budou reprezentovat
 * množiny čísel. Jsou-li ‹ns₁›, ‹ns₂› hodnoty typu ‹numset› a dále
 * ‹i›, ‹j› jsou hodnota typu ‹int›, požadujeme následující operace:
 *
 *  • ‹ns₁.add( i )› – vloží do ‹ns₁› číslo ‹i›,
 *  • ‹ns₁.del( i )› – odstraní z ‹ns₁› číslo ‹i›,
 *  • ‹ns₁.del_range( i, j )› – odstraní z ‹ns₁› všechna čísla,
 *    která spadají do uzavřeného intervalu ⟦⟨i, j⟩⟧,
 *  • ‹ns₁.merge( ns₂ )› – přidá do ‹ns₁› všechna čísla přítomná
 *    v ‹ns₂›,
 *  • ‹ns₁.has( i )› – rozhodne, zda je ‹i› přítomné v ‹ns₁›.
 *
 * Složitost:
 *
 *  • ‹del_range› a ‹merge› musí mít nejvýše lineární složitost,
 *  • ostatní operace nejvýše logaritmickou. */

struct numset{
    std::set<int> nums;

    bool add(int i){
        return std::get<1>(nums.insert(i));
    }

    bool del(int i){
        return nums.erase(i) > 0;
    }

    void del_range(int x, int y){
        nums.erase(nums.lower_bound(x), nums.upper_bound(y));
    }

    void merge(const numset ns){
        for (int i : ns.nums)
            add(i);
    }

    bool has(int i) const{
        return nums.contains(i);
    }
};

int main()
{
    numset a, b, test;
    const numset &x = a, &y = b;

    for ( int n : { 1, 3, 5, 7, 11, 17 } )
        assert( a.add( n ) );
    for ( int n : { 2, 4, 8, 16 } )
        assert( b.add( n ) );
    for ( int n : { 1, 2, 3, 4, 5, 6 } )
        assert( test.add( n ) );
    test.del_range(3,5);

    assert(  x.has( 1 ) );
    assert(  x.has( 7 ) );
    assert( !x.has( 2 ) );
    assert(  y.has( 2 ) );
    assert( !y.has( 7 ) );

    assert(  a.del( 7 ) );
    assert( !x.has( 7 ) );
    assert( !a.del( 7 ) );
    assert( !a.has( 7 ) );
    assert( !a.add( 1 ) );
    assert(  a.add( 7 ) );

    a.del_range( 3, 8 );
    assert( !x.has( 3 ) );
    assert( !x.has( 5 ) );
    assert( !x.has( 7 ) );

    a.merge( y );
    assert( a.has(  1 ) );
    assert( a.has(  2 ) );
    assert( a.has(  4 ) );
    assert( a.has(  8 ) );
    assert( a.has( 11 ) );
    assert( a.has( 17 ) );

    return 0;
}
