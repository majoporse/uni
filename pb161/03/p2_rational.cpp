#include <cassert>
#include <numeric>
#include <compare>
/* V tomto příkladu budeme programovat jednoduchá racionální čísla
 * (taková, že je lze reprezentovat dvojicí celých čísel typu
 * ‹int›). Hodnoty typu ‹rat› lze:
 *
 *  • vytvořit čistou funkcí ‹make_rat( p, q )› kde ‹p›, ‹q› jsou
 *    hodnoty typu ‹int› (čitatel a jmenovatel) a ‹q > 0›,
 *  • použít jako operandy základních aritmetických operací:
 *    ◦ sčítání ‹+›,
 *    ◦ odečítání (‹-›),
 *    ◦ násobení (‹*›) a
 *    ◦ dělení (‹/›),
 *  • libovolně srovnávat (‹==›, ‹!=›, ‹<=›, ‹<›, ‹>›, ‹>=›).
 *
 * Vzpomeňte si, jak se jednotlivé operace nad racionálními čísly
 * zavádí. Jsou-li ⟦a = p₁/q₁⟧ a ⟦b = p₂/q₂⟧ zlomky v základním
 * tvaru, můžete se u libovolné operace ⟦a ⋄ b⟧ spolehnout, že
 * žádný ze součinů ⟦p₁⋅q₂⟧, ⟦p₂⋅q₁⟧, ⟦p₁⋅p₂⟧ a ⟦q₁⋅q₂⟧ nepřeteče
 * rozsah ‹int›-u. */

struct rat{

    int nom, denom;

    friend bool operator==(const rat &r, const rat &l){
        return r.nom * l.denom == l.nom * r.denom;
    }

    friend bool operator!=(const rat &r, const rat &l){
        return r.nom * l.denom != l.nom * r.denom;
    }

    friend auto operator<=>(const rat& r, const rat &l) {
        return r.nom * l.denom <=> l.nom * r.denom ;
    }

    rat & operator+=(const rat &r){
        int lcm = std::lcm(denom, r.denom);
        nom = (lcm / denom) * nom + (lcm / r.denom) * r.nom;
        denom = lcm;

        if (nom == denom){
            nom = 1;
            denom = 1;
        }

        return *this;
    }

    rat &operator-=(const rat &r){

        int lcm = std::lcm(denom, r.denom);
        nom = (lcm / denom) * nom - (lcm / r.denom) * r.nom ;
        denom = lcm;
        
        if (nom == denom){
            nom = 1;
            denom = 1;
        }
        return *this;
    }

    rat &operator*=(const rat &r){
        int lgcd = std::gcd(denom, r.nom);
        int rgcd = std::gcd(r.denom, nom);

        nom = (nom / rgcd) * (r.nom / lgcd);
        denom = (denom / lgcd) * (r.denom / rgcd);

        if (nom == denom){
            nom = 1;
            denom = 1;
        }
        
        return *this;
    }

    rat &operator/=(const rat &r){
        rat reversed = {r.denom, r.nom};
        *this *= reversed;
        return *this;
    }
    

    friend rat operator+( rat l, const rat &r){
        l += r;
        return l;
    }

    friend rat operator-( rat l, const rat &r){
        l -= r;
        return l;
    }

    friend rat operator*(rat l, const rat &r){
        l *= r;
        return l;
    }

    friend rat operator/(rat l, const rat &r){
        l /= r;
        return l;
    }
};

rat make_rat( int nom, int denom ){
    rat res = {nom, denom};
    return res;
}

int main()
{
    rat one = make_rat( 1, 1 ),
        half = make_rat( 1, 2 ),
        three_halves = make_rat( 3, 2 ),
        minus_half = make_rat( -1, 2 ),
        third = make_rat( 1, 3 ),
        two = make_rat( 2, 1 ),
        minus_sixth = make_rat( -1, 6 );

    assert( half < one );
    assert( one < three_halves );
    assert( half < three_halves );

    assert( one + one == two );
    assert( two / two == one );
    assert( one * two == two );
    assert( one != two );
    assert( !( one == two ) );
    assert( !( one != one ) );
    assert( third * ( one + two ) == one );
    assert( half + half == one );
    assert( half + one == three_halves );
    assert( one < one + one );
    assert( minus_half + minus_half < minus_half );
    assert( minus_half < half );
    assert( minus_half + half == one - one );
    assert( minus_half * minus_half == half / two );
    assert( three_halves + minus_half == one );
    assert( half + third < one );
    assert( minus_half < minus_sixth );
    assert( minus_half + third == minus_sixth );

    return 0;
}
