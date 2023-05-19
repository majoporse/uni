#include <cassert>
#include <cstdint>
#include <vector>
#include <array>
#include <variant>
#include <array>
#include <tuple>
#include <algorithm>

/* V této úloze budete programovat jednoduchý registrový stroj
 * (model počítače). Stroj bude mít libovolný počet celočíselných
 * registrů a paměť adresovatelnou po bajtech. Registry jsou
 * indexované od 1 po ‹INT_MAX›. Každá instrukce jmenuje dva
 * registry a jednu přímo zakódovanou hodnotu (angl. immediate).
 *
 * V každém registru je uložena hodnota typu ‹int32_t›, tzn.
 * velikost strojového slova jsou 4 slabiky (bajty). V paměti jsou
 * slova uložena tak, že nejvýznamnější slabika má nejnižší adresu
 * (tzv. MSB-first). Počáteční hodnoty registrů i paměti jsou nuly.
 *
 * Stroj má následovné instrukce (kdykoliv je ‹reg_X› použito
 * v popisu, myslí se tím samotný registr – jeho hodnota nebo
 * úložišě – nikoliv jeho index; sloupec ‹reg_2› má opačný význam,
 * vztahuje se k indexu uloženému v instrukci).
 *
 *  │ opcode │‹reg_2›│ description                                 │
 *  ├────────┼───────┼◅────────────────────────────────────────────┤
 *  │ ‹mov›  │  ≥ 1  │ kopíruj hodnotu z ‹reg_2› do ‹reg_1›        │
 *  │        │  = 0  │ nastav ‹reg_1› na ‹immediate›               │
 *  │ ‹add›  │  ≥ 1  │ ulož ‹reg_1 + reg_2› do ‹reg_1›             │
 *  │        │  = 0  │ přičti ‹immediate› do ‹reg_1›               │
 *  │ ‹mul›  │  ≥ 1  │ ulož ‹reg_1 * reg_2› do ‹reg_1›             │
 *  │ ‹jmp›  │  = 0  │ skoč na adresu uloženou v ‹reg_1›           │
 *  │        │  ≥ 1  │ skoč na ‹reg_1› je-li ‹reg_2› nenulové      │
 *  │ ‹load› │  ≥ 1  │ načti hodnotu z adresy ‹reg_2› do ‹reg_1›   │
 *  │ ‹stor› │  ≥ 1  │ zapiš hodnotu ‹reg_1› na adresu ‹reg_2›     │
 *  │ ‹halt› │  = 0  │ zastav stroj s výsledkem ‹reg_1›            │
 *  │        │  ≥ 1  │ totéž, ale pouze je-li ‹reg_2› nenulový     │
 *
 * Každá instrukce je v paměti uložena jako 4 slova (adresy slov
 * rostou zleva doprava). Vykonání instrukce, která není skokem,
 * zvýší programový čítač o 4 slova.
 *
 *  ┌────────┬───────────┬───────┬───────┐
 *  │ opcode │ immediate │ reg_1 │ reg_2 │
 *  └────────┴───────────┴───────┴───────┘
 *
 * Vykonání jednotlivé instrukce by mělo zabrat konstantní čas.
 * Paměť potřebná pro výpočet by měla být v nejhorším případě úměrná
 * součtu nejvyšší použité adresy a nejvyššího použitého indexu
 * registru. */

enum class opcode { mov, add, mul, jmp, load, stor, hlt };
struct mov{};
struct add{};
struct mul{};
struct jmp{};
struct load{};
struct stor{};
struct hlt{};

struct machine
{
    int32_t counter = 0;
    std::vector<int8_t> data;
    std::vector<int32_t> registers;

    int32_t immediate, reg_1, reg_2;
    bool operator()(mov){
        if (reg_2)
            registers[reg_1] = registers[reg_2];
        else
            registers[reg_1] = immediate;
        return true;
    }
    bool operator()(add){
        if (reg_2)
            registers[reg_1] += registers[reg_2];
        else
            registers[reg_1] += immediate;
        return true;
    }
    bool operator()(mul){
        if (reg_2)
            registers[reg_1] *= registers[reg_2]; 
        return true;
    }
    bool operator()(jmp){
        if (!reg_2 || (reg_2 && registers[reg_2]))
            counter = registers[reg_1];
        return true;
    }
    bool operator()(load){
        if (reg_2 > 0)
            registers[reg_1] = get(registers[reg_2]);
        return true;
    }
    bool operator()(stor){
        if (reg_2 > 0)
            set(registers[reg_2], registers[reg_1]);
        return true;
    }
    bool operator()(hlt) {
        return reg_2 && !registers[reg_2];
    }

    std::array<std::variant<mov, add, mul, jmp, load, stor, hlt>, 7> ops = {{mov{}, add{}, mul{}, jmp{}, load{}, stor{}, hlt{}}};


    /* Čtení a zápis paměti po jednotlivých slovech. */

    unsigned char get_char(std::int32_t i){
        return i < static_cast<std::int32_t>(data.size()) ? data[i] : 0;
    }

    std::int32_t get( std::int32_t addr ){
        return get_char(addr) << 24 | get_char(addr+1) << 16 | get_char(addr+2) << 8 | get_char(addr+3);
    }

    void set( std::int32_t addr, std::int32_t v ){
        if (static_cast<std::int32_t>(data.size()) <= addr)
            data.resize(addr + 4);
        for (int i = 0; i < 4; ++i, v >>= 8){
            data[addr + 4 - 1 - i] = v % 0b100000000;
        }
    }


    /* Spuštění programu, počínaje adresou nula. Vrátí hodnotu
     * uloženou v ‹reg_1› zadaném instrukcí ‹hlt›, která výpočet
     * ukončila. */

    std::int32_t run(){
        counter = 0;
        registers.clear();
        do{

            std::tie(immediate, reg_1, reg_2) = std::tuple(get(counter+4), get(counter + 8), get(counter + 12));

            if (std::int32_t max = std::max(reg_1, reg_2); max >= static_cast<std::int32_t>(registers.size()))
                registers.resize(max + 1);
            
            counter += 16;
        } while (std::visit(*this, ops[data[counter - 16 + 3]]));

        return registers[reg_1];
    }
};


int main()
{
    machine m;
    m.set( 0x00, static_cast< std::int32_t >( opcode::mov ) );
    m.set( 0x04, 7 );
    m.set( 0x08, 1 );
    m.set( 0x10, static_cast< std::int32_t >( opcode::hlt ) );
    m.set( 0x18, 1 );
    assert( m.run() == 7 );

    {
        machine x;
        x.set(0x00, static_cast<std::int32_t>(opcode::mov));
        x.set( 0x04, -INT32_MAX);
        auto a = x.get(0x04);
        assert(a == -INT32_MAX);
        x.set( 0x08, 123 ); //nastav reg 123 na -intmax

        x.set( 0x10, static_cast<std::int32_t>(opcode::mov));
        x.set( 0x14, 0x100);
        x.set( 0x18, 111 ); //nastav reg 111 na 0x100
    
        x.set( 0x100, INT32_MAX );
        x.set(0x20, static_cast<std::int32_t>(opcode::load));
        x.set(0x28, 69);
        x.set(0x2c, 111); //load z pamate na 0x100 do reg 69

        x.set(0x30, static_cast<std::int32_t>(opcode::add));
        x.set(0x38, 123);
        x.set(0x3c, 69);

        x.set( 0x40, static_cast< std::int32_t >( opcode::hlt ) );
        x.set( 0x48, 123);
        assert(x.run() == 0);
    }
    
    return 0;
}
