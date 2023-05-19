#include <cstdint>
#include <cassert>

/* Najděte nejmenší nezáporné číslo ⟦n⟧ takové, že 64-bitový zápis
 * čísla ‹word› lze získat zřetězením nějakého počtu binárně
 * zapsaných kopií ⟦n⟧. Protože potřebný zápis ⟦n⟧ může obsahovat
 * levostranné nuly, do výstupního parametru ‹length› uložte jeho
 * délku v bitech. Je-li možné ‹word› sestavit z různě dlouhých
 * zápisů nějakého ⟦n⟧, vyberte ten nejkratší možný.
 *
 * Příklad: pro ‹word = 0x100000001› bude hledané ⟦n = 1⟧, protože
 * ‹word› lze zapsat jako dvě kopie čísla 1 zapsaného do 32 bitů. */

/* Returns a number consisting of `size` ones in binary */
std::uint32_t bitmask(std::size_t size) {
    return (1ul << size) - 1;
}

bool is_periodic(std::uint64_t word, std::uint64_t pattern, std::size_t width) {
    for (std::size_t i = 0; i < 64 / width; i++) {
        if ((word & bitmask(width)) != pattern)
            return false;
        word >>= width;
    }

    return true;
}

std::uint64_t periodic(std::uint64_t word, int &length) {
    /* The width of the pattern in bits must be a power of 2, otherwise
     * we would not be able to fit a whole number of repetitions into
     * the 64-bit word, and it would therefore not be periodic. */
    for (std::size_t width = 1; width <= 32; width <<= 1) {
        std::uint32_t pattern = word & bitmask(width);
        if (is_periodic(word, pattern, width)) {
            length = width;
            return pattern;
        }
    }

    /* If we couldn't find a pattern, it means the word is not periodic,
     * so we can consider the whole word as a single "repetition". */
    length = 64;
    return word;
}

int main()
{
    int length;

    assert( periodic( 0x100000001u, length ) == 1 );
    assert( length == 32 );
    assert( periodic( 0x1212121212121212u, length ) == 0x12 );
    assert( length == 8 );
    assert( periodic( 0x1234123412341234u, length ) == 0x1234 );
    assert( length == 16 );
    assert( periodic( 0, length ) == 0 );
    assert( length == 1 );
    assert( periodic( 1, length ) == 1 );
    assert( length == 64 );

    return 0;
}
