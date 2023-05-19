#include <set>
#include <cassert>
#include <cstdio>
#include <vector>

/* Napište funkci ‹kernel›, která spočítá rozklad¹ množiny celých
 * čísel ‹s› podle jádra funkce ‹f›. Jádrem funkce myslíme relaci
 * ekvivalence, kde jsou v relaci právě všechny vzory ⟦x⟧ daného
 * obrazu ⟦f(x)⟧. Formálněji ⟦(x, y) ∈ \ker f ↔ f(x) = f(y)⟧.
 *
 * Můžete předpokládat, že návratový typ funkce ‹f› je ‹int›.
 * Časová složitost nesmí být horší, než O(n⋅logn). */

auto kernel( const std::set< int > &set, auto fun){
    std::vector<std::set<int>> res;
    // if (set.empty())
    //     return std::set<std::set<int>> {};


    std::set< int > new_grp;
    for (int thing : set){
        bool added = false;
        auto a = fun(thing);
        for (auto & re : res){
            if (a == fun(*re.begin())){
                re.emplace(thing);
                added = true;
            }
        }
        if (!added)
            res.emplace_back(std::set<int>{thing});
    }
    std::set<std::set<int>> r;
    for (auto s : res)
        r.emplace(std::move(s));
    return r;
}

/* ¹ Rozkladem množiny ⟦X⟧ podle ekvivalence ⟦R⟧ myslíme systém
 *   množin ⟦S⟧, který tuto relaci respektuje: je-li ⟦ [a] = { b ∈ X
 *   | (a, b) ∈ R } ⟧, potom ⟦ S = { [a] | a ∈ X } ⟧. */

int main()
{
    using s_int = std::set< int >;
    using ss_int = std::set< s_int >;
    s_int in{ 1, 2, 3, 4, 5 };
    ss_int div2_k{ { 1 }, { 2, 3 }, { 4, 5 } };
    auto div2 = []( int i ) { return i / 2; };

    assert( kernel( in, div2 ) == div2_k );

    s_int a{ 1, 2, 3, 4 },
          b{ 1, 2, 3, 4, 5, 6, 7, 8 },
          c{ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16 };

    int calls = 0, a_calls = 0, b_calls = 0, c_calls = 0;
    auto mod4 = [&]( int v ) { ++ calls; return v % 4; };

    assert( kernel( a, mod4 ).size() == 4 );
    std::swap( calls, a_calls );
    assert(( kernel( b, mod4 ) ==
             ss_int{ { 4, 8 }, { 1, 5 }, { 2, 6 }, { 3, 7 } } ));
    std::swap( calls, b_calls );
    assert( kernel( c, mod4 ).size() == 4 );
    std::swap( calls, c_calls );

    std::fprintf( stderr, "%d %d %d\n", a_calls, b_calls, c_calls );
    assert( b_calls / a_calls <= 4 );
    assert( c_calls / b_calls <= 4 );
    assert( c_calls / a_calls <= 10 );

    return 0;
}
