#include <vector>
#include <cassert>
#include <type_traits>
#include <tuple>

/* Napište funkce ‹map›, ‹zip› a ‹fold›. Pracovat budeme ve všech
 * případech s libovolnými kontejnery, o kterých je zaručeno, že
 *
 *  • mají (konstantní) metody ‹begin› a ‹end›, které vrací
 *  • vhodné iterátory, které
 *    ◦ mají prefixový a postfixový operátor ‹++›,
 *    ◦ operátory rovnosti ‹==›, ‹!=› a
 *    ◦ operátor dereference (unární ‹*›).
 *
 * Žádné jiné metody předpokládat nelze. */

/* Funkce ‹map› má parametry ‹f› (funkce) a kontejner ‹c› (s prvky
 * takového typu, aby je bylo možné předat funkci ‹f› jako
 * parametr). Výsledkem je ‹std::vector› hodnot, které vzniknou
 * voláním ‹f› na jednotlivé prvky kontejneru ‹c›. */

auto map(auto f, auto c){
    std::vector<decltype(f(*(c.begin())))> res;
    for (auto i : c)
        res.push_back(f(i));
    return res;
}

/* Funkce ‹zip› je podobná, ale ‹f› je funkce o dvou parametrech a
 * na vstupu jsou dva kontejnery ‹c› a ‹d› (nemusí být stejného
 * typu). První parametr funkce ‹f› nechť pochází z kontejneru ‹c›,
 * ten druhý pak z kontejneru ‹d›.
 *
 * Nemají-li kontejnery stejnou délku, přebývající hodnoty v tom
 * delším se ignorují. */

auto zip(auto f, auto c, auto d){
    std::vector<decltype(f(*(c.begin()), *(d.begin())))> res;
    for(auto [a, b] = std::tuple(c.begin(), d.begin()); a != c.end() && b != d.end() ;++a, ++b)
        res.push_back(f(*a, *b));
    return res;
}

/* Konečně funkce ‹fold› bude mít parametry ‹f›, ‹i› a ‹c›, kde ‹f›
 * je binární funkce, ‹i› je iniciální hodnota a ‹c› je vstupní
 * kontejner. Jsou-li c₀ … cₙ prvky ‹c›, výsledek funkce ‹fold› pak
 * odpovídá ‹f( … f( f( i, c₀ ), c₁ ), … cₙ )›. Je-li kontejner ‹c›
 * prázdný, výsledkem je ‹i›. Parametry funkce ‹f› mohou být obecně
 * různých typů, musí být ale kompatibilní s ‹i› a ‹c›. */

auto fold(auto f, auto i, auto c){
    auto res = f(i, *(c.begin()));
    for(auto ii = ++c.begin(); ii != c.end(); ++ii)
        res = f(res, *ii);
    return res;
}

int main()
{
    struct list
    {
        struct iterator
        {
            const int *ptr = nullptr;
            iterator( const int *p ) : ptr( p ) {}
            iterator &operator++() { ++ptr; return *this; }
            iterator  operator++( int ) { auto rv = *this; ++*this; return rv; }
            bool operator==( const iterator & ) const = default;
            int operator*() const { return *ptr; }
        };

        std::vector< int > _values;
        iterator begin() const { return { &*_values.begin() }; }
        iterator end()   const { return { &*_values.end() }; }
        list( std::initializer_list< int > v ) : _values( v ) {}
    };

    struct token {};

    using intv = std::vector< int >;
    using tokv = std::vector< token >;

    list a{ 1, 2, 3, 4, 5 };

    intv b = map( []( int x ) { return 2 * x; }, a );
    intv c = map( []( int x ) { return x * x; }, a );
    intv d = zip( []( int x, int y ) { return x * y; }, a, a );
    intv e = zip( []( int x, int y ) { return x * y; }, a, b );
    intv f = zip( []( int x, int y ) { return x * y; }, b, a );

    assert(( b == intv{ 2, 4, 6, 8, 10 } ));
    assert(( c == intv{ 1, 4, 9, 16, 25 } ));
    assert(( d == intv{ 1, 4, 9, 16, 25 } ));
    assert(( e == f ));

    b.pop_back();
    e = zip( []( int x, int y ) { return x * y; }, a, b );
    f = zip( []( int x, int y ) { return x * y; }, b, a );

    assert(( e == f ));
    assert(( f == intv{ 2, 8, 18, 32 } ));

    auto f1 = []( int x, token ) { return x + 1; };
    auto f2 = []( auto x, auto y ) { return x + y; };
    assert(( fold( f1, 3, tokv{ {}, {}, {} } ) == 6 ));
    assert(( fold( f2, 7, intv{ 1, 2 } ) == 10 ));

    return 0;
}
