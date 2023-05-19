#include <string>
#include <cassert>
#include <algorithm>
#include <ranges>
#include <string_view>

/* V tomto příkladu budeme pracovat s textem. Procedura ‹rewrap›
 * dostane odkaz (referenci) na řetězec, který obsahuje text složený
 * ze slov oddělených mezerami (U+0020) nebo znaky nového řádku
 * (U+000A). Dva nebo více znaků konce řádku těsně za sebou chápeme
 * jako oddělovač odstavců.
 *
 * Dále dostane celočíselný počet sloupců (znaků) ‹cols›, který
 * určují, jak dlouhý může být jeden řádek. Procedura pak
 * přeformátuje vstupní řetězec tak, aby:
 *
 *  1. bylo zachováno rozdělení na odstavce,
 *  2. jednotlivý řádek textu nepřesáhl ‹cols›,
 *  3. zachová celistvost slov (tzn. smí měnit pouze mezery a znaky
 *     nového řádku),
 *  4. každý řádek byl nejdelší možný.
 *
 * Můžete předpokládat, že žádné slovo není delší než ‹cols› a že
 * každá mezera sousedí po obou stranách se slovem. */

void rewrap( std::u32string &str, int cols ){
    std::size_t pos = 0, last_pos = 0, last_nl = 0;
    std::size_t next_space = 0,  next_nl = 0;

    while ((pos = next_space < next_nl ? next_space : next_nl) != std::string::npos){
        
        
        if (pos - last_nl > static_cast<std::size_t>(cols)){
            str[last_pos] = U'\n';
            last_nl = last_pos;
        } else if (last_pos > 0)
            str[last_pos] = U' ';
        
        last_pos = pos;
        next_space = str.find(U' ', pos + 1);
        next_nl = str.find(U'\n', pos + 1);

        if (str[next_nl + 1] == U'\n')
             next_nl = str.find(U'\n', next_nl + 2);
    }
}

int main()
{
    std::u32string s = U"lorem ipsum dolor sit amet\n";

    rewrap( s, 5 );
    assert( s == U"lorem\nipsum\ndolor\nsit\namet\n" );
    rewrap( s, 6 );
    assert( s == U"lorem\nipsum\ndolor\nsit\namet\n" );
    rewrap( s, 20 );
    assert( s == U"lorem ipsum dolor\nsit amet\n" );
    rewrap( s, 30 );
    assert( s == U"lorem ipsum dolor sit amet\n" );

    s = U"no\n\nway\n";
    rewrap( s, 100 );
    assert( s == U"no\n\nway\n" );

    return 0;
}
