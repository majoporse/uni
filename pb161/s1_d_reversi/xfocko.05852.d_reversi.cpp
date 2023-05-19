/** Grade: @A **/
#include <tuple>
#include <vector>
#include <cassert>
#include <set>
#include <tuple>
#include <iostream>

#define EMPTY 0
#define WHITE 1
#define BLACK 2

#define WHITE_TURN true
#define BLACK_TURN false

/* Předmětem tohoto úkolu je hra Reversi (známá také jako Othello),
 * avšak ve třírozměrné verzi. Hra se tedy odehrává v kvádru, který
 * se skládá ze sudého počtu polí (krychlí) v každém ze tří
 * základních směrů (podle os ⟦x⟧, ⟦y⟧ a ⟦z⟧). Dvě taková pole můžou
 * sousedit stěnou (6 směrů), hranou (12 směrů) nebo jediným
 * vrcholem (8 směrů). Pole může být prázdné, nebo může obsahovat
 * černý nebo bílý hrací kámen.
 *
 * Hru hrají dva hráči (černý a bílý, podle barvy kamenů, které jim
 * patří) a pravidla hry jsou přímočarým rozšířením těch klasických
 * dvourozměrných:
 *
 *  • každý hráč má na začátku 4 kameny, rozmístěné kolem
 *    prostředního bodu kvádru (jedná se tedy o 8 polí, které
 *    tento bod sdílí), a to tak, že žádná dvě obsazená pole
 *    stejné barvy nesdílí stěnu, přičemž pole s nejmenšími
 *    souřadnicemi ve všech směrech obsahuje bílý kámen,
 *  • hráči střídavě pokládají nový kámen do volného pole; je-li na
 *    tahu bílý hráč, pokládá bílý kámen do pole, které musí být
 *    nepřerušeně spojeno¹ černými kameny s alespoň jedním
 *    stávajícím bílým kamenem (černý hráč hraje analogicky),
 *  • po položení nového kamene se barva všech kamenů, které leží
 *    na libovolné takové spojnici, změní na opačnou (tzn. přebarví
 *    se na barvu právě položeného kamene).
 *
 * Začíná bílý hráč. Hra končí, není-li možné položit nový kámen
 * (ani jedné barvy). Vyhrává hráč s více kameny na ploše. */


using position = std::tuple<int, int, int>;
using positions = std::set<position>;
using direction = position;

struct cube{
    std::vector<int> data;
    int xs, ys, zs;
    cube(int x, int y, int z): xs{x}, ys{y}, zs{z} {
        data = std::vector<int>(x*y*z, 0);
    }
    cube() = default;
    int &get(int x, int y, int z) {return data[x + y * xs + z * ys * xs];}
    const int &get(int x, int y, int z) const {return data[x + y * xs + z * ys * xs];}
/** I must've missed where you use it, but please be careful about the fact that you
 **  initialize the cube with zeroes and this just “drops” everything, it can lead
 ** to an inconsistent state. **/
    void clear(){data.clear();}
};
struct reversi
{
    cube play_space;
    bool _turn;
    int _xs, _ys, _zs;

    int _black_stones, _white_stones;

    std::vector<direction> directions;

    void init_directions(){
        for (int dz = -1; dz <= 1; ++dz){
            for (int dy = -1; dy <= 1; ++dy){
                for (int dx = -1; dx <= 1; ++dx){
                    if (dz == 0 && dy == 0 && dx == 0)
                        continue;
                    directions.emplace_back(dx, dy, dz);
                }
            }
        }
    }

    bool is_valid_position(int x, int y, int z) const{
    return  x >= 0 && x < _xs &&
            y >= 0 && y < _ys &&
            z >= 0 && z < _zs;
    }

    void init_stones(){
        
        int x = (_xs-1) / 2;
        int y = (_ys-1) / 2;
        int z = (_zs-1) / 2;
        bool t = WHITE_TURN;

        for (int dz = 0; dz <= 1; ++dz, t = !t){
            for (int dy = 0; dy <= 1; ++dy, t = !t){
                for (int dx = 0; dx <= 1; ++dx, t = !t){

                    (t ? _white_stones : _black_stones)++;
                    play_space.get(x + dx, y + dy, z + dz) = t ? WHITE : BLACK;
                }
            }
        }
    }

    int check_full_line(position pos, direction d, int turn) const {
        auto [dx, dy, dz] = d;
        auto [x, y, z] = pos;

        int my_stone = turn ? WHITE : BLACK;
        int opponent_stone = !turn ? WHITE : BLACK;
        int len = 0;
        int end;
        int init = play_space.get(x, y, z);
        x+=dx; y+=dy; z+=dz;

        if (init == EMPTY)
            end = my_stone;
        else 
            end = EMPTY;

        while (is_valid_position(x, y, z) &&
                play_space.get(x, y, z) == opponent_stone){
                ++len;
                x += dx;
                y += dy;
                z += dz;
        }

        if (!is_valid_position(x, y, z) || (len > 0 && play_space.get(x, y, z) != end))
            return 0;

        return len;
    }

    bool has_play(position pos, bool turn ) const{

        for (direction d : directions){
            if (check_full_line(pos, d, turn)!= 0)
                return true;
        }
        return false;
    }

    bool avalible_play(bool turn) const{
        int my_stone = turn ? WHITE : BLACK;

        for (int z = 0; z < _zs; ++z){
            for (int y = 0; y < _ys; ++y){
                for (int x = 0; x < _xs; ++x){
                    
                if(play_space.get(x, y, z) == my_stone && has_play({x, y, z}, turn))
                    return true;
                }
            }
        }
        return false;
    }

    bool playable(position pos) const{
        auto [x, y, z] = pos;
        return is_valid_position(x, y, z) && play_space.get(x, y, z) == EMPTY
               && has_play(pos, _turn);
    }

    void fill_line(position pos, direction d, int len){
        auto [x, y, z] = pos;
        auto [dx, dy, dz] = d;
        int colour = _turn ? WHITE : BLACK;
        int opponent_colour = !_turn ? WHITE : BLACK;
        int &player_count = _turn ? _white_stones : _black_stones;
        int &oopponent_count = !_turn ? _white_stones : _black_stones;
        x+=dx; y+=dy; z+=dz;

        for (;len > 0 ; --len, x += dx, y += dy, z += dz){
            if (play_space.get(x, y, z) == opponent_colour)
                oopponent_count--;
            play_space.get(x, y, z) = colour;
            player_count++;
        }
    }

    bool fill_position(position pos){
        int len = 0;
        (_turn ? _white_stones : _black_stones)++;

        for (direction d : directions){
            if ((len = check_full_line(pos, d, _turn)) != 0)
                fill_line(pos, d, len);
        }
        return false;
    }

    /* Metoda ‹start› začne novou hru na ploše zadané velikosti.
     * Případná rozehraná partie je tímto voláním zapomenuta. Po
     * volání ‹start› je na tahu bílý hráč. */

    void start( int x_size, int y_size, int z_size ){
        play_space.clear();
        _black_stones = 0;
        _white_stones = 0;
        _xs = x_size;
        _ys = y_size;
        _zs = z_size;
        play_space = cube{x_size, y_size, z_size};

        init_directions();
        init_stones();
        _turn = WHITE_TURN;
    }

    /* Metoda ‹size› vrátí aktuální velikost hrací plochy. */

    std::tuple< int, int, int > size() const{
        return {_xs, _ys, _zs};
    }

    /* Metoda ‹play› položí kámen na souřadnice zadané parametrem.
     * Barva kamene je určena tím, který hráč je právě na tahu.
     * Byl-li tah přípustný, metoda vrátí ‹true› a další volání
     * položí kámen opačné barvy. V opačném případě se hrací plocha
     * nezmění a stávající hráč musí provést jiný tah. */

    /* Není určeno, co se má stát v případě, že hra ještě nezačala,
     * nebo již skončila (tzn. nebyla zavolána metoda ‹start›, nebo
     * by metoda ‹finished› vrátila ‹true›). */

    bool play( int x, int y, int z ){
        position pos = {x, y, z};

        if (!playable(pos))
            return false;

        
        fill_position(pos);
        play_space.get(x, y, z) = _turn ? WHITE : BLACK;
        _turn = !_turn;
        return true;
    }

    /* Nemůže-li aktivní hráč provést platný tah, zavolá metodu
     * ‹pass›. Tato vrátí ‹true›, jedná-li se o korektní přeskočení
     * tahu (má-li hráč k dispozici jakýkoliv jiný platný tah,
     * «musí» nějaký provést – volání ‹pass› v takovém případě vrátí
     * ‹false› a aktivní hráč se nemění).
     *
     * Platí stejná omezení na stav hry jako u metody ‹play›. */

    bool pass(){
        if (avalible_play(_turn))
            return false;

        _turn = !_turn;
        return true;
    }

    /* Metoda-predikát ‹finished› vrací ‹true› právě tehdy,
     * nemůže-li ani jeden z hráčů provést platný tah a hra tedy
     * skončila. Výsledek volání není určen pro hru, která dosud
     * nezačala (nedošlo k volání metody ‹start›). */

    bool finished() const{
        return !avalible_play(WHITE_TURN) && !avalible_play(BLACK_TURN);       
    }

    /* Metodu ‹result› je povoleno zavolat pouze v případě, že hra
     * skončila (tzn. volání ‹finished› by vrátilo ‹true›). Její
     * návratovou hodnotou je rozdíl v počtu kamenů mezi bílým a
     * černým hráčem – kladné číslo značí výhru bílého hráče,
     * záporné výhru černého hráče a nula značí remízu. */

    int result() const{
        return _white_stones - _black_stones;
    }
};

/* ¹ Uvažujme dvojicí polí (krychlí) ⟦A⟧, ⟦B⟧ a úsečku ⟦u⟧, která
 *   spojuje jejich středy, a která prochází středem stěny, hrany
 *   nebo vrcholem pole ⟦A⟧. Nepřerušeným spojením myslíme všechna
 *   pole, které úsečka ⟦u⟧ protíná, vyjma ⟦A⟧ a ⟦B⟧ samotných.
 *   Dvojici polí, pro které potřebná úsečka ⟦u⟧ neexistuje, nelze
 *   nepřerušeně spojit. */


int main()
{
        reversi r;
    r.start( 4, 4, 4 );
    assert( !r.play( 2, 2, 2 ) );
    assert( r.play( 3, 3, 3 ) );
    assert( !r.play( 3, 3, 3 ) );
    return 0;
}
