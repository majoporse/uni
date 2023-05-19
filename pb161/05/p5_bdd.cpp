#include <cassert>
#include <memory>
#include <map>
#include <vector>

/* Binární rozhodovací diagram je úsporná reprezentace booleovských
 * funkcí více parametrů. Lze o nich uvažovat jako o orientovaném
 * acyklickém grafu s dodatečnou sémantikou: každý vrchol je buď
 * «proměnná» (parametry) a má dva následníky, kteří určí, jak
 * pokračovat ve vyhodnocení funkce, je-li daná proměnná pravdivá
 * resp. nepravdivá. Krom proměnných existují dva další uzly, které
 * již žádné následníky nemají, a reprezentují výsledek vyhodnocení
 * funkce; označujeme je jako 0 a 1. */

/* Implementujte tyto metody:
 *
 *  • konstruktor má jeden parametr typu ‹char› – název proměnné,
 *    kterou reprezentuje kořenový uzel,
 *  • ‹one› vrátí „pravdivý“ uzel (tzn. uzel 1),
 *  • ‹zero› vrátí „nepravdivý“ uzel (tzn. uzel 0),
 *  • ‹root› vrátí počáteční (kořenový) uzel,
 *  • ‹add_var› přijme ‹char› a «vytvoří» uzel pro zadanou
 *    proměnnou; k jedné proměnné může existovat více než jeden uzel
 *  • ‹add_edge› přijme rodiče, hodnotu typu ‹bool› a následníka,
 *  • ‹eval› přijme map z ‹char› do ‹bool› a vyhodnotí
 *    reprezentovanou funkci na parametrech popsaných touto mapou
 *    (tzn. bude procházet BDD od kořene a v každém uzlu se rozhodne
 *    podle zadané mapy, až než dojde do koncového uzlu).
 *
 * Chování není definováno, obsahuje-li BDD uzel, který nemá
 * nastavené oba následníky. */

struct bdd_node{
    char name = '_';
    bdd_node *t = nullptr;
    bdd_node *f = nullptr;

    bdd_node(char c) :name{c}{}
};

struct bdd{
    std::unique_ptr< bdd_node > r;
    std::vector< std::unique_ptr< bdd_node > > nodes;

    bdd(char c): r{std::make_unique< bdd_node >(c)}{
        nodes.push_back(std::make_unique< bdd_node > ('0'));
        nodes.push_back(std::make_unique< bdd_node > ('1'));
    }

    bdd_node *one(){return nodes[1].get();}
    bdd_node *zero(){return nodes[0].get();}
    bdd_node *root(){return r.get();}

    bdd_node *add_var(char c){
        nodes.push_back(std::make_unique< bdd_node >(c));
        return nodes.back().get();
    }

    void add_edge(bdd_node *cur, bool b, bdd_node *succ) {
        (b ? cur->t : cur->f) = succ;
    }

    bool eval(std::map<char, bool> keys)const{
        bdd_node *cur = r.get();
        while(cur->t != nullptr && cur->f != nullptr){
            cur = (keys[cur->name] ? cur->t : cur->f);
        }
        return cur->name == '1';
    }

};

int main()
{
    bdd b( 'z' );
    const bdd &cb = b;

    auto tt = b.one();
    auto ff = b.zero();

    auto x1 = b.add_var( 'x' );
    auto x2 = b.add_var( 'x' );
    auto y1 = b.add_var( 'y' );
    auto y2 = b.add_var( 'y' );
    auto z =  b.root();

    auto eval = [&]( bool x, bool y, bool z )
    {
        using m = std::map< char, bool >;
        return cb.eval( m{ { 'x', x }, { 'y', y }, { 'z', z } } );
    };

    b.add_edge( z,  true,  y1 );
    b.add_edge( z,  false, y2 );
    b.add_edge( y1, false, ff );
    b.add_edge( y1, true,  tt );
    b.add_edge( y2, false, x1 );
    b.add_edge( y2, true,  x2 );
    b.add_edge( x1, true,  ff );
    b.add_edge( x1, false, tt );
    b.add_edge( x2, false, ff );
    b.add_edge( x2, true,  tt );

    assert(  eval( 0, 0, 0 ) );
    assert( !eval( 0, 0, 1 ) );
    assert( !eval( 0, 1, 0 ) );
    assert(  eval( 0, 1, 1 ) );
    assert( !eval( 1, 0, 0 ) );
    assert( !eval( 1, 0, 1 ) );
    assert(  eval( 1, 1, 0 ) );
    assert(  eval( 1, 1, 1 ) );

    return 0;
}
