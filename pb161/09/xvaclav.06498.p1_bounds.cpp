#include <tuple>
#include <map>
#include <cstdint>
#include <cassert>
#include <variant>
#include <optional>

/* Implementujte třídu ‹bounds›, která si bude pro každý zadaný
 * celočíselný klíč pamatovat rozsah povolených hodnot. Přitom mez
 * typu ‹unbounded› bude znamenat, že v daném směru není hodnota
 * příslušná danému klíči nijak omezena. */

struct unbounded {};

/* Samotná třída bounds bude mít metody:
 *
 *  • ‹set_lower( k, b )› nastaví spodní mez ‹b› pro klíč ‹k› (‹b›
 *    je buď 64b celé číslo, nebo hodnota ‹unbounded{}›),
 *  • ‹set_upper( k, b )› obdobně, ale horní mez,
 *  • ‹set_default_lower( b )› nastaví implicitní dolní mez (platí
 *    pro klíče, kterým nebyla nastavena žádná jiná),
 *  • ‹set_default_upper( b )› obdobně, ale horní mez,
 *  • ‹valid( k, i )› vrátí ‹true› právě když hodnota ‹i› spadá do
 *    mezí platných pro klíč ‹k›.
 *
 * Všechny takto zadané intervaly jsou oboustranně otevřené. */

struct bounds{
    std::map<int, std::tuple<std::optional<int64_t>,std::optional<int64_t>>> key_bounds;
    std::optional<int64_t> defl, defu;

    /** Quite a bit of code duplication here.
     ** Some suggestions:
     ** - If you are using the std::variant<...> type in multiple places,
     **    why not use `auto` instead? (or even better, declare a type alias
     **    via `using` and then use that in each of the function signatures.)
     ** - Instead of using std::optional to signify whether a particular bound
     **    exists or is unbounded, why not just store the variant directly?
     **    I personally think it would improve code readability a lot.
     **    Additionally, you could swap `int64_t` and `unbounded` within the
     **    `variant` type, which would make `unbounded` the default value when
     **    it has not been written to yet, making your code a lot cleaner
     **    and easier to write for you - since that is what the assignment requested.
     **/
    void set_lower(int k, std::variant<int64_t, unbounded> b){
        std::get<0>(key_bounds[k]) = b.index() == 0 ? std::get<int64_t>(b) : std::optional<int>{}; 
    }
    void set_upper(int k, std::variant<int64_t, unbounded> b){
        std::get<1>(key_bounds[k]) = b.index() == 0 ? std::get<int64_t>(b) : std::optional<int>{}; 
    }
    void set_default_lower(std::variant<int64_t, unbounded> a){
        defl = a.index() == 0 ? std::get<int64_t>(a) : std::optional<int>{};
    }
    void set_default_upper(std::variant<int64_t, unbounded> a){
        defu = a.index() == 0 ? std::get<int64_t>(a) : std::optional<int>{};
    }
    bool valid(int k, int64_t i){
        std::optional<int64_t> l, r;
        if (key_bounds.contains(k))
            std::tie(l, r) = key_bounds[k];
        else
            std::tie(l, r) = std::tie(defl, defu);
        return i >= l.value_or(defl.value_or(i)) && i <= r.value_or(defu.value_or(i));
    }
    
};

int main()
{
    bounds a;
    a.set_lower( 0, -10 );
    a.set_upper( 0, unbounded{} );
    assert( a.valid( 0, 0 ) );
    assert( a.valid( 0, -9 ) );
    assert( a.valid( 0, 21351 ) );
    assert( !a.valid( 0, -21351 ) );

    a.set_upper( 1, 100 );
    assert( a.valid( 1, -13213 ) );

    assert( a.valid( 2, ( 1ll << 62 ) + 1 ) );
    assert( a.valid( 2, ( 1ll << 62 ) * -1 ) );

    bounds b;
    b.set_default_lower( -5 );
    b.set_default_upper( 15 );
    assert( !b.valid( 0, 65 ) );
    assert( b.valid( 0, -2 ) );

    return 0;
}
