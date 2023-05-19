#include <tuple>
#include <vector>
#include <set>
#include <cassert>

/* Naprogramujte proceduru ‹intervals›, která z posloupnosti ⟦k⟧
 * dvojic (zleva uzavřených, zprava otevřených intervalů) vytvoří
 * vzestupně seřazenou posloupnost ⟦n⟧ prvků tak, že každá hodnota,
 * která spadá do některého vstupního intervalu, se ve výstupní
 * posloupnosti objeví právě jednou.
 *
 * Procedura ‹intervals› bude mít rozhraní podobné standardním
 * algoritmům:
 *
 *  • vstupem bude dvojice (rozsah) iterátorů, které zadávají
 *    sekvenci dvojic–intervalů (‹std::tuple›),
 *  • a výstupní iterátor, do kterého zapíše výslednou posloupnost.
 *
 * Můžete předpokládat, že prvky (a tedy i intervaly zadané jako
 * jejich dvojice) lze kopírovat a přiřazovat. Algoritmus by měl mít
 * složitost ⟦O(n + k⋅\log(k))⟧. */

void intervals(auto begin, auto end, auto out)
{
    std::set<int> output;
    for (decltype(begin) it = begin; it != end ; ++it) {
        auto [from, to] = *it;
        for (int i = from; i < to; ++i) {
            output.insert(i);
        }
    }
    for (auto num : output) {
        *out = num;
        out++;
    }

}

int main()
{
    using interval = std::tuple< int, int >;
    std::vector< interval > iv{ { 0, 3 }, { 7, 8 }, { 2, 3 }, { 1, 5 } };

    std::vector< int > vals;

    intervals( iv.cbegin(), iv.cend(), std::back_inserter( vals ) );
    assert(( vals == std::vector{ 0, 1, 2, 3, 4, 7 } ));

    iv.pop_back();

    intervals( iv.cbegin(), iv.cend(), std::back_inserter( vals ) );
    assert(( vals == std::vector{ 0, 1, 2, 3, 4, 7, 0, 1, 2, 7 } ));

    return 0;
}
