#include <cassert>
#include <ranges>
#include <vector>
#include <iterator>
#include <algorithm>

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
void intervals(auto begin, auto end, auto inserter){
    std::vector<std::tuple<int, int>> rangees;
    /**
     ** Even though this isn't wrong, it'd be better
     ** to use the vector's iterator range constructor
     ** to fill the rangees vector. You'd save some
     ** lines + have better readability by doing:
     **     std::vector<std::tuple<int, int>> rangees(begin, end);
     **/
    for(;begin != end; ++begin){
        rangees.emplace_back(*begin);
    }

    /**
     ** Is it really necessary to define the projection lambda?
     ** Imo it would be sufficient to define comparison function
     ** [](auto& s1, auto& s2) { return std::get<0>(s1) < std::get<0>(s2); }
     ** I don't know how this is performance-wise, however it seems a bit more
     ** readable to me.
     **
     ** + consider taking the tuple by reference `auto x -> auto& x`
     **/
    std::ranges::sort(rangees, {}, [](auto x) { return std::get<0>(x); });
    std::vector<int> res;
    for (auto [from, to] : rangees){
        /**
         ** My advice would be to wrap the whole for loop body (always)
         ** in curly braces as it might be confusing and result
         ** in some mistakes if (in team project) somebody
         ** would want to add some code into the for loop
         ** they might not notice the braces are missing.
         ** Adding the braces could save some time spent debugging
         **/
        for (; from != to; ++from)
            if (res.empty() || res.back() < from)
                res.push_back(from);
    }
    /**
     ** I appreciate the usage of ranges, however this could've
     ** been done by a simple range-based for loop
     **
     ** for (auto x : res) {
     **     *inserter++ = x;
     ** }
     ** This imo better says what it's supposed to do and a potential reader does not need to know
     ** what `generate_n` does
     **/
    std::ranges::generate_n(inserter, res.size(), [&res, i = 0]() mutable {return res[i++]; });
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
