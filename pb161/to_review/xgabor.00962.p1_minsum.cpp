#include <vector>
#include <cassert>

/* Na vstupu dostanete posloupnost celočíselných hodnot (jako
 * instanci kontejneru ‹std::vector›). Vaším úkolem je rozdělit je
 * na kratší posloupnosti tak, že každá posloupnost je nejkratší
 * možná, ale zároveň je její součet alespoň ‹sum›. Výjimku tvoří
 * poslední posloupnost, pro kterou nemusí nutně existovat potřebné
 * prvky.
 *
 * Pořadí prvků musí být zachováno, tzn. zřetězením všech
 * posloupností na výstupu musí vzniknout původní posloupnost
 * ‹numbers›. */

int sum_range(const std::vector< int >& numbers, int from, int to)
{
    int sum = 0;
    for (int i = from; i <= to; i++) {
        sum += numbers.at(i);
    }
    return sum;
}

std::vector<int> range_vec(const std::vector< int >& numbers, int from, int to)
{
    std::vector<int> vec = {};
    for (int i = from; i <= to; i++)
    {
        vec.push_back(numbers.at(i));
    }
    return vec;
}

auto minsum(const std::vector< int >& numbers, int sum)
{
    std::vector< std::vector<int> > seqs = {};
    unsigned int i = 0, j = 0;

    while (i < numbers.size() && j < numbers.size() )
    {
        while (sum_range(numbers, i, j) < sum && j < numbers.size() - 1)
        {
            j++;
        }
        seqs.push_back(range_vec(numbers, i, j));
        i = j + 1;
    }
    return seqs;
}

int main()
{
    assert(( minsum( std::vector{ 1, 2 }, 1 ) ==
               std::vector{ std::vector{ 1 }, { 2 } } ));
    assert(( minsum( std::vector{ 1, 2, 3, 4 }, 3 ) ==
             std::vector{ std::vector{ 1, 2 }, { 3 }, { 4 } } ));
    return 0;
}
