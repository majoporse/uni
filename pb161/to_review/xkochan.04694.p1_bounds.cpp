#include <cassert>
#include <cstdint>
#include <map>
#include <variant>

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

struct implicit {};
struct bounds {
    using bound = std::variant<implicit, unbounded, int64_t>;

    std::map<int, std::pair<bound, bound>> bounds_map;
    int64_t implicit_lower{INT64_MIN}, implicit_upper{INT64_MAX};
    void set_lower(auto k, auto b) {
        auto [l, r] = bounds_map[k];
        bounds_map[k] = {b, r};
    }
    void set_upper(auto k, auto b) {
        auto [l, r] = bounds_map[k];
        bounds_map[k] = {l, b};
    }
    void set_default_lower(auto b) { implicit_lower = b; }
    void set_default_upper(auto b) { implicit_upper = b; }
    bool valid(auto k, auto i) {
        auto [l, r] = bounds_map[k];

        bool correct_lower;
        if (std::holds_alternative<unbounded>(l)) correct_lower = true;
        if (std::holds_alternative<implicit>(l))
            correct_lower = i >= implicit_lower;
        if (auto *v = std::get_if<int64_t>(&l)) correct_lower = i >= *v;

        if (std::holds_alternative<unbounded>(r)) return correct_lower;
        if (std::holds_alternative<implicit>(r))
            return correct_lower && i <= implicit_upper;
        if (auto *v = std::get_if<int64_t>(&r)) return correct_lower && i <= *v;
        assert(false);
    }
};

int main() {
    bounds a;
    a.set_lower(0, -10);
    a.set_upper(0, unbounded{});
    assert(a.valid(0, 0));
    assert(a.valid(0, -9));
    assert(a.valid(0, 21351));
    assert(!a.valid(0, -21351));

    a.set_upper(1, 100);
    assert(a.valid(1, -13213));

    assert(a.valid(2, (1ll << 62) + 1));
    assert(a.valid(2, (1ll << 62) * -1));

    bounds b;
    b.set_default_lower(-5);
    b.set_default_upper(15);
    assert(!b.valid(0, 65));
    assert(b.valid(0, -2));

    return 0;
}
