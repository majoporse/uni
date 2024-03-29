#include <vector>
#include <tuple>
#include <cassert>

/* † Navrhněte typ, který se bude navenek chovat jako sekvenční
 * kontejner dvojic (‹std::tuple›) čísel, ale vnitřně bude data
 * uchovávat ve dvojici kontejnerů (‹std::vector›) celých čísel.
 * Požadované metody:
 *
 *  • ‹begin›, ‹end› a odpovídající zjednodušený iterátor s:
 *    ◦ operátory ‹==› a ‹!=›,
 *    ◦ prefixovým operátorem ‹++›,
 *    ◦ operátorem dereference (unární ‹*›),
 *    kde výsledek operátoru ‹*› musí být použitelný jako dvojice
 *    čísel, včetně ‹std::get› a přiřazení do jednotlivých složek.
 *  • ‹size›,
 *  • ‹push_back›,
 *  • ‹emplace_back› (se dvěma parametry typu ‹int›, nebo
 *    žádným parametrem),
 *  • ‹left› a ‹right› vrátí konstantní referenci na příslušný
 *    vnitřní kontejner (konstantní proto, aby nebylo jejich
 *    použitím možné porušit potřebné invarianty).
 *
 * Stačí, aby iterace fungovala pro nekonstantní hodnoty typu
 * ‹components› (naprogramovat konstantní i nekonstantní iteraci bez
 * duplikace kódu neumíme).
 *
 * Nápověda: zvažte, jak využít ‹std::tuple› s vhodnými parametry.
 * K vyřešení příkladu stačí už probrané konstrukce. */
struct component_iterator{
    std::vector<int> &a;
    std::vector<int> &b;
    int index;
    component_iterator(std::vector<int> &a, std::vector<int> &b, int index): a{a}, b{b}, index{index}{}

    std::tuple<int&, int&> operator*(){
        return {a[index], b[index]};
    }
    component_iterator operator++(){
        if (index + 1 == static_cast<int>(a.size()))
            index = -1;
        else 
            ++index;
        return *this;
    }
    friend bool operator==(const component_iterator &x, const component_iterator &y){
        return x.index == y.index;
    };
};

struct components{
    std::vector<int> a;
    std::vector<int> b;
    component_iterator begin(){
        return {a, b, 0};
    }

    component_iterator end(){
        return {a, b, -1};
    }

    unsigned size() const{return static_cast<unsigned>(a.size());}
    void push_back(std::tuple<int, int> n){
        auto [x, y] = n;
        a.push_back(x);
        b.push_back(y);
    }
    
    void emplace_back(int x, int y){
        a.push_back(x);
        b.push_back(y);
    }

    const std::vector<int> &left()const { return a; }
    const std::vector<int> &right()const { return b; }
};

int main()
{
    components x;
    const components &x_const = x;
    const auto &l = x_const.left();
    const auto &r = x_const.right();

    x.emplace_back( 1, 3 );
    assert(( l == std::vector{ 1 } ));
    assert(( r == std::vector{ 3 } ));
    assert(( *x.begin() == std::tuple{ 1, 3 } ));

    assert( x_const.size() == 1 );
    x.push_back( { 3, 3 } );
    unsigned i = 0;

    for ( auto [ a, b ] : x )
    {
        assert( a == 1 || a == 3 );
        assert( b == 3 );
        ++ i;
    }

    assert( x.size() == i );
    std::get< 0 >( *x.begin() ) = 3;
    assert(( l == std::vector{ 3, 3 } ));

    return 0;
}
