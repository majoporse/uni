#include <cassert>
#include <vector>
#include <initializer_list>
#include <type_traits>

/* Napište čistou, generickou funkci ‹combine( s, f )› kde ‹s› je
 * neprázdný indexovatelný kontejner (má tedy metodu ‹size› a lze
 * jej indexovat celými čísly) hodnot libovolného typu, a ‹f› je
 * binární asociativní funkce, kde:
 *
 *  • velikost výsledku funkce ‹f› může mít libovolnou monotonní
 *    závislost na velikosti vstupů (např. může platit ⟦|f(u, v)| =
 *    |u| + |v|⟧),
 *  • podobně libovolná (ale stále monotonní) je délka výpočtu
 *    funkce ‹f› v závislosti na velikostech parametrů.
 *
 * Vaším úkolem je pomocí ‹f› sestavit z celé posloupnosti ‹s›
 * jedinou hodnotu, a to tak, aby se minimalizoval celkový potřebný
 * čas.
 *
 * Příklad: Je-li ‹f› lineární (jak ve velikosti výsledku, tak
 * v čase výpočtu) a prvky ‹s› mají velikost 1, celková složitost 
 * volání ‹combine› by neměla přesáhnout ⟦O(n⋅log(n))⟧. Příkladem
 * takové funkce ‹f› je spojení dvou hodnot typu ‹std::vector› za
 * sebe.
 *
 * Příklad: Je-li ‹f› kvadratická (opět ve velikosti výsledku i
 * čase), celková složitost by měla být nejvýše ⟦O(n²⋅log(n))⟧.
 * Zde by ‹f› mohl být například tenzorový součin. */

auto combine(const auto &s, auto f){
    std::vector<std::decay_t<decltype(s[0])>> res1;

    for (std::size_t i = 0; 2*i < s.size() - 1; ++i){
        if (i == s.size() - 2) 
            res1.push_back(s[2*i]);
        res1.push_back(f(s[2*i], s[2*i+1]));
    }

    while (res1.size() > 1){
        auto copy = std::move(res1);
        res1.clear();
        for (std::size_t i = 0; 2*i < copy.size(); ++i){
            if (i == copy.size() - 1){
                res1.push_back(s[2*i]);
                break;
            }
            res1.push_back(f(copy[2*i], copy[2*i+1]));
        }
    }
    return res1[0];
}

int main()
{
    int ops = 0, a_ops = 0, b_ops = 0, c_ops = 0;

    auto concat = [&]( auto v, const auto &w )
    {
        ops += v.size();

        for ( auto x : w )
        {
            ++ ops;
            v.push_back( x );
        }

        return v;
    };

    using v_int = std::vector< int >;
    using vv_int = std::vector< v_int >;

    struct lv_int
    {
        lv_int( const std::initializer_list< v_int > &v ) : data( std::move( v ) ) {}
        lv_int( const lv_int & ) = delete;

        auto begin() const { return data.begin(); }
        auto end()   const { return data.end(); }
        auto operator[]( int i ) const { return data[ i ]; }
        auto size() const { return data.size(); }
    private:
        vv_int data;
    };

    const lv_int a{ { 1 }, { 2 }, { 3 }, { 4 } };
    const vv_int b{ { 1 }, { 2 }, { 3 }, { 4 },
                    { 5 }, { 6 }, { 7 }, { 8 } };
    const lv_int c{ { 1 }, { 2 }, { 3 }, { 4 },
                    { 5 }, { 6 }, { 7 }, { 8 },
                    { 7 }, { 6 }, { 5 }, { 4 },
                    { 3 }, { 2 }, { 1 }, { 0 } };

    assert(( combine( a, concat ) == std::vector{ 1, 2, 3, 4 } ));
    std::swap( ops, a_ops );
    combine( b, concat );
    std::swap( ops, b_ops );
    combine( c, concat );
    std::swap( ops, c_ops );

    assert( b_ops / a_ops <= 4 );
    assert( c_ops / b_ops <= 4 );
    assert( c_ops / a_ops <= 10 );

    return 0;
}
