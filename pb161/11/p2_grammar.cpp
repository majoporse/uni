#include <cassert>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <algorithm>

/* Regulární gramatika má pravidla tvaru ⟦A → xB⟧ nebo ⟦A → x⟧ kde
 * ⟦A⟧, ⟦B⟧ jsou neterminály a ⟦x⟧ je terminál. */

/* Navrhněte typ ‹grammar›, kterého hodnoty lze implicitně sestrojit
 * a který má tyto 2 metody:
 *
 *  • ‹add_rule›, které lze předat 2 nebo 3 parametry:
 *    a. jeden znak, který reprezentuje levou stranu (velké písmeno
 *       anglické abecedy) a
 *    b. jeden terminál (malé písmeno), nebo jeden terminál a jeden
 *       neterminál,
 *  • ‹generate›, která přijme 2 parametry: startovní neterminál a
 *  kladné celé číslo, které reprezentuje maximální délku slova;
 *  výsledkem bude seznam (‹std::vector›) všech řetězců (slov),
 *  které lze takto vygenerovat, a to v lexikografickém pořadí. */

class grammar{
public:
    std::map<char, std::set<std::string>> rules;
    void add_rule( char a, char b, char c = '\0' ){
        rules[a].insert(std::string{b} + c);
    }
    void generate_rec( char a, int b, std::vector<std::string> &res, std::string s = "") const{
        if (b == 0)
            return;
        --b;
        if (!rules.contains(a))
            return;

        for (auto &r : rules.at(a)){
            if (r[1] == '\0'){
                res.emplace_back(s + r[0]);
            } else {
                generate_rec(r[1], b, res, s + r[0]);
            }
        }
    }

    std::vector<std::string> generate( char a, int b ) const{
        std::vector<std::string> res;
        generate_rec(a,b,res);
        return res;
    }
};

int main()
{
    auto w = []( auto... words ) /* helper function */
    {
        return std::vector< std::string >{ words... };
    };

    grammar g;
    const grammar &cg = g;

    assert( cg.generate( 'A', 10 ) == w() );
    g.add_rule( 'A', 'a' );
    assert( cg.generate( 'A', 10 ) == w( "a" ) );

    g.add_rule( 'A', 'b', 'A' );
    assert( cg.generate( 'A', 3 ) == w( "a", "ba", "bba" ) );

    g.add_rule( 'A', 'x', 'X' );
    g.add_rule( 'X', 'x' );
    assert( cg.generate( 'A', 3 ) == w( "a", "ba", "bba", "bxx", "xx" ) );
    g.add_rule( 'X', 'x', 'X' );
    assert( cg.generate( 'X', 3 ) == w( "x", "xx", "xxx" ) );

    return 0;
}
