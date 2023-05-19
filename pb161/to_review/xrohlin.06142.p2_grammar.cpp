#include <cassert>
#include <map>
#include <string>
#include <vector>
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

template <class Char = char>
class Grammar {
private:
    using String = std::basic_string<Char>;
    std::map<Char, std::vector<String>> m_rules;

public:
    static bool is_non_term(Char c) { return std::isupper(c); }
    static bool is_term(Char c) { return std::islower(c); }

    void add_rule(Char left, Char term) { m_rules[left].push_back(String({ term })); }
    void add_rule(Char left, Char term, Char non_term) { m_rules[left].push_back(String({ term, non_term })); }

    std::vector<String> generate(Char start, std::size_t size) const {
        if (size == 0)
            return {};
        std::vector<String> out;
        out.emplace_back(1, start);
        for (std::size_t i = 1; i <= size; i++)
            out = expand(out);

        std::vector<String> true_out;
        for (auto&& elem : out) 
            if (is_term(elem.back()))
                true_out.emplace_back(std::move(elem));
        
        return true_out;
    }

    std::vector<String> expand(const std::vector<String>& orig) const {
        std::vector<String> out;
        for (const auto& elem : orig) {
            if (!is_non_term(elem.back())) {
                out.push_back(elem);
                continue;
            }

            auto _rules = m_rules.find(elem.back());
            if (_rules == m_rules.end()) {
                out.push_back(elem);
                continue;
            }

            auto rules = _rules->second;

            for (const auto& rule : rules) {
                auto tmp = elem;
                tmp.pop_back();
                tmp.append(rule);
                out.push_back(tmp);
            }
        }
        return out;
    }
};

using grammar = Grammar<char>;

int main() {
    auto w = [](auto... words) /* helper function */
    {
        return std::vector<std::string> { words... };
    };

    grammar g;
    const grammar& cg = g;

    assert(cg.generate('A', 10) == w());
    g.add_rule('A', 'a');
    assert(cg.generate('A', 10) == w("a"));

    g.add_rule('A', 'b', 'A');
    assert(cg.generate('A', 3) == w("a", "ba", "bba"));

    g.add_rule('A', 'x', 'X');
    g.add_rule('X', 'x');
    assert(cg.generate('A', 3) == w("a", "ba", "bba", "bxx", "xx"));
    g.add_rule('X', 'x', 'X');
    assert(cg.generate('X', 3) == w("x", "xx", "xxx"));

    return 0;
}
