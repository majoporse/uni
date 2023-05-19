#include <vector>
#include <cassert>
#include <tuple>
#include <numeric>
#include <ranges>

/* Předmětem tohoto příkladu jsou tzv. «řetězové zlomky». Typ
 * ‹fraction› bude reprezentovat racionální číslo, které lze:
 *
 *  • zadat posloupností koeficientů řetězového zlomku (přesněji
 *    popsáno níže) pomocí metody ‹set_coefficients( cv )› kde ‹cv›
 *    je vektor hodnot typu ‹int›,
 *  • sčítat (operátorem ‹+›),
 *  • násobit (operátorem ‹*›),
 *  • srovnávat (všemi relačními operátory, tzn. ‹==›, ‹!=›, ‹<›,
 *    ‹<=›, ‹>›, ‹>=›).
 *
 * Řetězový zlomek reprezentujej racionální číslo ⟦q₀⟧ jako součet
 * celého čísla ⟦a₀⟧ a převrácené hodnoty nějakého dalšího
 * racionálního čísla, ⟦q₁⟧, které je samo zapsáno pomocí řetězového
 * zlomku. Tedy
 *
 *  ⟦ q₀ = a₀ + 1/q₁
 *    q₁ = a₁ + 1/q₂
 *    q₂ = a₂ + 1/q₃ ⟧
 *
 * a tak dále, až než je nějaké ⟦qᵢ⟧ celé číslo, kterým sekvence
 * končí (pro racionální číslo se to jistě stane po konečném počtu
 * kroků). Hodnotám ⟦a₀, a₁, a₂, …⟧ říkáme «koeficienty» řetězového
 * zlomku – jeho hodnota je jimi jednoznačně určena.
 *
 * Rozmyslete si vhodnou reprezentaci vzhledem k zadanému rozhraní.
 * Je důležité jak to, které operace jsou požadované, tak to, které
 * nejsou. */

struct fraction{
    int nom, denom;

     friend bool operator==(const fraction &r, const fraction &l){
        return r.nom * l.denom == l.nom * r.denom;
    }

    friend bool operator!=(const fraction &r, const fraction &l){
        return r.nom * l.denom != l.nom * r.denom;
    }

    friend auto operator<=>(const fraction& r, const fraction &l) {
        return r.nom * l.denom <=> l.nom * r.denom ;
    }

    std::tuple<int, int> normal_fraction(std::vector<int> coefs){
        int nom = 1;
        int denom = *(--coefs.end());
        int old;
        for (auto rit = coefs.rbegin(); rit+1 != coefs.rend(); ++rit){
            old = nom;
            nom = denom;
            denom = denom * *(rit+1) + old;
        }
        return {denom, nom};
    }

    fraction & operator+=(const fraction &b){

        int lcm = std::lcm(denom, b.denom);
        nom = lcm / denom * nom + b.nom * lcm / b.denom;
        denom = lcm;

        return *this;
    }

    friend fraction operator+(fraction a, const fraction &b){
        a += b;
        return a;
    }

    fraction & operator*=(const fraction &b){

        int lgcd = std::gcd(denom, b.nom);
        int rgcd = std::gcd(b.denom, nom);

        nom = (nom / rgcd) * (b.nom / lgcd);
        denom = (denom / lgcd) * (b.denom / rgcd);
        return *this;
    }

    friend fraction operator*(fraction a, const fraction &b){
        a *= b;
        return a;
    }

    void set_coefficients(std::vector<int> nums){
        auto a = normal_fraction(nums);
        nom = std::get<0>(a);
        denom = std::get<1>(a);
    }

};

int main()
{
    std::vector< int > c_1{ 1 },
                       c_2{ 4, 2, 6, 7 },
                       c_3{ 3, 4, 12, 4 },
                       c_4{ 0, 2, 4 },
                       c_5{ 0, 4, 2, 6, 7 };

    fraction f_1, f_2, f_3, f_4, f_5;

    f_1.set_coefficients( c_1 );
    f_2.set_coefficients( c_2 );
    f_3.set_coefficients( c_3 );
    f_4.set_coefficients( c_4 );
    f_5.set_coefficients( c_5 );

    assert( f_2 > f_1 );
    assert( f_3 > f_1 );
    assert( f_3 < f_1 + f_1 + f_1 + f_1 );
    assert( f_4 < f_1 );
    assert( f_4 + f_4 + f_4 > f_1 );
    assert( f_2 * f_5 == f_1 );

    return 0;
}
