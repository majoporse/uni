/** Grade: @B
 **
 ** ---
 **
 ** x = OK, - = minor issues, ! = major issues
 **
 ** * [x] clearly describes solution to the problem
 ** * [x] correctly decomposes the problem
 ** * [!] doesn't have code duplication
 **   * you don't need to check yourself for the equality of the vectors, use the
 ** built-in comparison
 ** * [-] uses correct abstractions, algorithms and data structures
 **   * `std::lcm` is definitely not what you wanted, you were probably looking for
 ** something like `std::min` or `std::max`
 **   * substituting size from the index in a loop… Please don't, just fix it.
 **   * `std::bitset` would be ideal, but I'm not requiring it
 **
 ** ---
 **
 ** Summary (+1s, suggestions, rants, confessions, etc.):
 ** * n/a
 **
 ** ---
 **
 ** In case you have anything to discuss or want to clarify any of my comments
 ** from the review, feel free to reach out via mail or Discord. **/
#include <vector>
#include <array>
#include <array>
#include <cassert>
#include <map>
#include <cstdint>
#include <utility>
#include <iostream>
#include <numeric>

/* Vaším úkolem bude naprogramovat jednoduchý simulátor
 * jednorozměrného celulárního automatu. Implementace bude sestávat
 * ze dvou struktur, ‹automaton_state› a ‹automaton›, které jsou
 * popsané níže. Zadané rozhraní je nutné dodržet. */

/* Definujte strukturu, ‹automaton_state›, která reprezentuje stav
 * automatu definovaného na «kružnici», s buňkami číslovanými po
 * směru hodinových ručiček od indexu 0. Stav si můžete představit
 * takto:
 *
 *             ┌───┐
 *         ┌───┤ 1 ├───┐
 *         │ 1 ├───┤ 0 │
 *       ┌─┴─┬─┘ ▲ └─┬─┴─┐
 *       │ 0 │   ●   │ 0 │
 *       └─┬─┴─┐   ┌─┴─┬─┘
 *         │ 1 ├───┤ 1 │
 *         └───┤ 1 ├───┘
 *             └───┘
 *
 * Platným indexem je «libovolné celé číslo» – určuje o kolik
 * políček od indexu 0 se posuneme (kladná čísla po směru, záporná
 * proti směru hodinových ručiček).
 *
 * Jsou-li ‹s›, ‹t› hodnoty typu ‹automaton_state›, dále ‹i›, ‹n›
 * jsou hodnoty typu ‹int› a ‹v› je hodnota typu ‹bool›, tyto
 * výrazy musí být dobře utvořené:
 *
 *  • ‹automaton_state( s )› vytvoří nový stav, který je stejný jako
 *    stav ‹s›,
 *  • ‹automaton_state( n )› vytvoří nový stav o ‹n› buňkách, které
 *    jsou všechny nastaveny na ‹false› (pro ‹n ≤ 0› není
 *    definováno),
 *  • ‹s.size()› vrátí aktuální počet buněk stavu ‹s›,
 *  • ‹s.get( i )› vrátí hodnotu buňky na indexu ‹i›,
 *  • ‹s.set( i, v )› nastaví buňku na indexu ‹i› na hodnotu ‹v›,
 *  • ‹s.extend( n )› vloží ‹n› nových buněk nastavených na hodnotu
 *    ‹false›, a to tak, že nové buňky budou na indexech ⟦-1⟧ až
 *    ⟦-n⟧ (je-li ‹n› záporné, chování není definováno),
 *  • ‹s.reduce( n )› odstraní ‹n› buněk proti směru hodinových
 *    ručiček, počínaje indexem -1 (je-li ‹n ≥ s.size()› nebo je ‹n›
 *    záporné, chování není definováno),
 *  • ‹t = s› upraví stav ‹t› tak, aby byl stejný jako ‹s›,
 *  • ‹t == s› je ‹true› právě když jsou stavy ‹s› a ‹t› stejné,
 *  • ‹t != s› je ‹true› právě když se stavy ‹s› a ‹t› liší,
 *  • ‹t <= s› se vyhodnotí na ‹true› právě když pro všechny indexy
 *    ‹i› platí ‹s.get( i ) || !t.get( i )›,
 *  • ‹t < s› se vyhodnotí na ‹true› právě když ‹t <= s && t != s›.
 *
 * Je-li to možné, výrazy musí pracovat správně i v případech, kdy
 * jsou ‹s› a/nebo ‹t› konstantní. Metody ‹size›, ‹get› a ‹set› musí
 * pracovat v konstantním čase, vše ostatní v čase nejvýše
 * lineárním. */

struct automaton_state{
    
    std::vector<bool> _circle;
    
/** Should work with `default` too, shouldn't it? **/
    automaton_state(const automaton_state &s) {*this = s;}

/** ```suggestion:-0+0
 **     automaton_state(int n) : _circle(n, false) {}
 ** ``` **/
    automaton_state(int n) {_circle = std::vector<bool>(n, false);}

    void set(int i, int b) {_circle[i] = b;}

    int size()const {return static_cast<int>(_circle.size());}

    int get(int i)const{
/** May I interest you in an operation called _modulo_? **/
        while (i < 0) i += size();
/** Cool, you can do similar thing a line above… just do something like
 **
 **     (size() + (i % size())) % size() **/
        return _circle[i % size()];
    }

/** I think you can also use `.resize` for both, but it's fine. **/
    void extend(int size) {_circle.insert(_circle.end(), size, false);}

    void reduce(int i) {_circle.erase(_circle.end() - i, _circle.end());}

    automaton_state &operator=(const automaton_state &s) = default;

    friend bool operator==(const automaton_state &s, const automaton_state &ss){
/** In other words:
 **
 **     return s._circle == ss._circle; **/
        for (int i = 0; i < s.size(); ++i)
            if (s.get(i) != ss.get(i)) return false;

        return s.size() == ss.size();
    }

    friend auto operator!=(const automaton_state &s, const automaton_state &ss){
        return !(s == ss);
    }

    friend auto operator<=(const automaton_state &s, const automaton_state &ss){
/** Are you »sure« that's what you want? **/
        int lcm = std::lcm(s.size(), ss.size());
        for (int i = 0; i < lcm; ++i)
            if (!ss.get(i) && s.get(i)) 
                return false;

        return true;
    }

    friend bool operator<(const automaton_state &s, const automaton_state &ss){
        return s <= ss && s != ss;
    }

};

/* Struktura ‹automaton› reprezentuje samotný automat. Třída si
 * udržuje interní stav, na kterém provádí výpočty (tzn. například
 * volání metody ‹step()› změní tento interní stav).
 *
 * Následovné výrazy musí být dobře utvořené (kde ‹a›, ‹b› jsou
 * hodnoty typu ‹automaton›, ‹s› je hodnota typu ‹automaton_state›,
 * a konečně ‹n› a ‹rule› jsou hodnoty typu ‹int›):
 *
 *  • ‹automaton( rule, n )› sestrojí automat s ‹n› buňkami
 *    nastavenými na ‹false› (chování pro ‹n ≤ 0› není definováno),
 *    a s pravidlem ‹rule› zadaným tzv. Wolframovým kódem (chování
 *    je definováno pouze pro ‹rule› v rozsahu 0 až 255 včetně),
 *  • ‹automaton( rule, s )› sestrojí nový automat a nastaví jeho
 *    vnitřní stav tak, aby byl stejný jako ‹s› (význam parametru
 *    ‹rule› je stejný jako výše),
 *  • ‹a.state()› umožní přístup k internímu stavu, a to tak, že je
 *    možné jej měnit, není-li samotné ‹a› konstantní (např.
 *    ‹a.state().set( 3, true )› nastaví buňku interního stavu
 *    s indexem 3 na hodnotu ‹true›),
 *  • ‹a = b› nastaví automat ‹a› tak, aby byl stejný jako automat
 *    ‹b› (zejména tedy upraví nastavené pravidlo a vnitřní stav),
 *  • ‹a.step()› provede jeden krok výpočtu na vnitřním stavu (jeden
 *    krok nastaví všechny buňky vnitřního stavu na další generaci),
 *  • ‹a.reset( s )› přepíše vnitřní stav kopií stavu ‹s›.
 *
 * Hodnoty, které vstupují do výpočtu nové generace buňky podle
 * zadaného Wolframova kódu, čteme po směru hodinových ručiček (tzn.
 * ve směru rostoucích indexů).
 *
 * Krok výpočtu musí mít nejvýše lineární (časovou i paměťovou)
 * složitost. */

struct automaton{
    automaton_state _state;
    std::vector<bool> _rules;

    
    automaton( int rule, int n ): _state{automaton_state(n)}
                                        {to_vec(rule);}

    automaton( int rule, automaton_state s):_state{automaton_state(s)}
                                                  {to_vec(rule);}

/** Eh… If you know it's always one byte, you could probably use a `bitset` for it,
 ** not that you need it at all. **/
    void to_vec(int r){
        _rules = std::vector<bool>(8, false);
        for (int i = 0; r > 0; ++i, r >>= 1) {
            if (r % 2 == 1) _rules[i] = true;
        }
    }

    automaton_state &state() {return _state;}

    const automaton_state &state()const {return _state;}

    automaton &operator=(const automaton &a) = default;

    void step(){
        automaton_state new_state(_state.size());

        for(int i = 0; i < _state.size(); ++i){
            int cur = _state.get(i-1) * 4 + _state.get(i) * 2 + _state.get(i+1);
            new_state.set(i, _rules[cur]);
        }
        _state = new_state;
    }

    void reset(automaton_state s) {_state = s;}
};

int main()
{
    automaton_state s( 3 );
    const auto &s_const = s;

    assert( s.size() == 3 );
    assert( !s_const.get( 0 ) );
    s.set( 0, true );
    assert( s_const.get( 0 ) );

    automaton a( 0, s );
    const auto &a_const = a;
    a.step();
    assert( !a_const.state().get( 0 ) );
    a.state().set( 0, true );
    assert( a_const.state().get( 0 ) );
    a.step();
    assert( !a_const.state().get( 0 ) );

    return 0;
}
