#include <vector>
#include <string>
#include <cassert>
#include <string_view>

/* Napište čistou funkci, která spočítá naivní rozdělení textu na
 * jednotlivá slova.¹ Budeme uvažovat pouze bílé vs nebílé znaky
 * (kódové body), a za slova budeme považovat libovolnou neprázdnou
 * sekvenci nebílých znaků. Unicode obsahuje tyto bílé znaky
 * (označené vlastností ‹White_Space›):
 *
 * > ‹U+0009› – ‹U+000D›, ‹U+0020›, ‹U+0085›, ‹U+00A0›, ‹U+1680›,
 * > ‹U+2000› – ‹U+200A›, ‹U+2028›, ‹U+2029›, ‹U+202F›, ‹U+205F›,
 * > ‹U+3000›.
 *
 * Dále budeme považovat za bílé i znaky ‹U+200B›, ‹U+2060›, které
 * logicky (ale ne vizuálně) slova oddělují (tyto znaky vlastností
 * ‹White_Space› označeny nejsou).
 *
 * Vstupem funkce je pohled na text, výstupem funkce je seznam
 * (‹std::vector›) pohledů, které vymezují jednotlivá identifikovaná
 * slova. */

std::vector< std::u32string_view > words( std::u32string_view sv){
    using namespace std::literals;
    std::u32string_view a = U"\u0009\u000D\u0020\u0085\u00A0\u1680\u2000\u200A\u2028\u2029\u202F\u205F\u3000\u200B\u2060\u2008\n\v"sv;
    std::vector< std::u32string_view > v;
    std::size_t last_pos = sv.find_first_not_of(a, 0);

    for (std::size_t pos = last_pos; (pos = pos == std::string_view::npos ? pos : sv.find_first_of(a, pos)) != std::string_view::npos; last_pos = pos){
        v.emplace_back(sv.substr(last_pos, pos - last_pos));
        pos = sv.find_first_not_of(a, pos);
    }
    if (last_pos != std::string_view::npos)
        v.emplace_back(sv.substr(last_pos, last_pos - sv.size() + 1));
    return v;
}

/* ¹ Skutečná segmentace textu je «velmi» složitá a prakticky jediná
 *   možnost je použít stávající knihovny, pro C++ např. ICU4C
 *   (balík knihoven, který má dohromady cca 100MiB a jen hlavičkové
 *   soubory mají cca 120 tisíc řádků). */

int main()
{
    using uvec = std::vector< std::u32string_view >;

    assert(( words( U"lorem ipsum dolor" ) ==
             uvec{ U"lorem", U"ipsum", U"dolor" } ));
    assert(( words( U"hello, world" ) == uvec{ U"hello,", U"world" } ));
    assert(( words( U"hello  world" ) == uvec{ U"hello", U"world" } ));
    assert(( words( U"hello\nworld\n" ) == uvec{ U"hello", U"world" } ));
    assert(( words( U" hello \n world" ) == uvec{ U"hello", U"world" } ));
    assert(( words( U"hello world" ) == uvec{ U"hello", U"world" } ));
    assert(( words( U"hello world" ) == uvec{ U"hello", U"world" } ));
    assert(( words( U"lorem\tipsum\vdolor" ) ==
             uvec{ U"lorem", U"ipsum", U"dolor" } ));
    assert(( words( U"lorem ipsum​dolor" ) ==
             uvec{ U"lorem", U"ipsum", U"dolor" } ));

    return 0;
}
