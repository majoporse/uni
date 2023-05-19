/** Grade: @A
 **
 ** ---
 **
 ** x = OK, - = minor issues, ! = major issues
 **
 ** * [-] clearly describes solution to the problem
 **   * It's a bit harder to follow the “flow”, since, for example, you have
 ** multiple overloads of `operator+` and also a helper function for that. I would
 ** be careful about it.
 ** * [x] correctly decomposes the problem
 ** * [x] doesn't have code duplication
 ** * [x] uses correct abstractions, algorithms and data structures
 **
 ** ---
 **
 ** Summary (+1s, suggestions, rants, confessions, etc.):
 ** * Please try to set up a clang-format for yourself, it creates a bit of noise at
 **  some places.
 **
 ** ---
 **
 ** In case you have anything to discuss or want to clarify any of my comments
 ** from the review, feel free to reach out via mail or Discord. **/
#include <cassert>
#include <vector>
#include <compare>

/* Vaším úkolem je tentokrát naprogramovat strukturu, která bude
 * reprezentovat libovolně velké přirozené číslo (včetně nuly). Tyto
 * hodnoty musí být možné:
 *
 *  • sčítat (operátorem ‹+›),
 *  • odečítat (‹x - y› je ovšem definováno pouze za předpokladu ‹x ≥ y›),
 *  • násobit (operátorem ‹*›),
 *  • libovolně srovnávat (operátory ‹==›, ‹!=›, ‹<›, atd.),
 *  • mocnit na kladný exponent typu ‹int› metodou ‹power›,
 *  • sestrojit z libovolné nezáporné hodnoty typu ‹int›.
 *
 * Implicitně sestrojená hodnota typu ‹natural› reprezentuje nulu.
 * Všechny operace krom násobení musí být nejvýše lineární vůči
 * «počtu dvojkových cifer» většího z reprezentovaných čísel.
 * Násobení může mít v nejhorším případě složitost přímo úměrnou
 * součinu ⟦m⋅n⟧ (kde ⟦m⟧ a ⟦n⟧ jsou počty cifer operandů). */

struct natural{
    std::vector<bool> data;

    natural()= default;
    natural(int num) { set_vec(num); }

    friend std::strong_ordering operator<=>(const natural &a, const natural &b){
        if (a.size() != b.size()) return a.size() <=> b.size();
        for(int i = a.size() -1; i >= 0; --i){
/** ```suggestion:-1+0
 **             if (a.get(i) != b.get(i)) return a.get(i) <=> b.get(i);
 ** ```
 **
 ** It should work the same way, you don't have to be explicit to that extent. **/
            if (a.get(i) && ! b.get(i)) return std::strong_ordering::greater;
            if (!a.get(i) && b.get(i)) return std::strong_ordering::less; 
        }
        return std::strong_ordering::equivalent;
    }

    friend bool operator==(const natural &a, const natural &b) = default;


    void set_vec(int n){
        for (; n > 0; n >>= 1){
/** Come on!
 **
 ** ```suggestion:-3+0
 **             data.push_back(n % 2 == 1);
 ** ``` **/
            if ((n % 2) == 1)
                data.push_back(true);
            else
                data.push_back(false);
        }
    }

    bool get(int i, int shift = 0) const{
        if ((i - shift) < 0 || (i - shift) >= size()) return false;
        return data[i - shift];
    }


    int size()const{
/** ```suggestion:-2+0
 **         return static_cast<int>(data.size());
 ** ```
 **
 ** It's same… **/
        if (data.empty())
            return 0;
        return static_cast<int>(data.size());
    }

    natural &shift_plus(const natural &x, int shift){
        bool bigger = size() > x.size() + shift;
/** If you can still tell me how does this thing get wrapped in parentheses… **/
        int send = !bigger ? size() : x.size() + shift;

        if (!bigger)
            data.resize(x.size() + shift);

        int end = size();

        bool carry = false;
        
        int i = 0;
        for (bool a, b; i < end; ++ i){
            if (i >= send && bigger && !carry) 
                break;
            a = data[i];
            b = x.get(i, shift);

            data[i] = (a ^ b) ^ carry;
            carry = (a && b) || ((a ^ b) && carry);
        }
        if (carry)
            data.push_back(true);
        return *this;
    }

    natural &operator+=(const natural &x){
        shift_plus(x, 0);
        return *this;
    }

    natural &operator-=(const natural &x){
        bool carry = false;
        int a, b;
        int last_i = -1;

        for (int i = 0; i < size(); ++ i){
            a = get(i);
            b = x.get(i);

            data[i] = (b ^ a) ^ carry;
            if (get(i)) last_i = i;
            carry = (!a && (b || carry)) || (a && b && carry);
        }
        data.resize(last_i + 1);

        return *this;
    }

    friend natural operator+(const natural &a, const natural &b){
        if (a.size() == 0)
            return b;
        if (b.size() == 0)
            return a;
        natural res;
        if (a.size() > b.size()){
            res = a;
            res.shift_plus(b, 0);
        } else {
            res = b;
            res.shift_plus(a, 0);
        }
        return res;
    }

    friend natural operator-(natural a/* a is bigger/equal */, const natural &b){
        a -= b;
        return a;
    }
    

    friend natural operator*(const natural &a, const natural &b){
        if (a.size() == 0 || b.size() == 0){
            return {0};
        }

        natural res;
/** ```suggestion:-1+0
 **         const auto&[l, s] = (a.size() > b.size()) ? std::tie(a, b) : std::tie(b,
 **  a);
 ** ``` **/
        const natural &s = !(a.size() > b.size()) ? a : b;
        const natural &l = a.size() > b.size() ? a : b;

        for (int shift = s.size() -1; shift >= 0; --shift){
            if (!s.get(shift))
                continue;
            res.shift_plus(l, shift);
        }
        return res;
    }

    natural power(int i){
        
        natural tmp = *this;
        natural res{1};
        while (i > 0){
            if (i % 2 == 1){
                res = res * tmp; 
                --i;
            } else {
                tmp = tmp * tmp; 
                i /= 2;
            }
        }
        return res;
    }

};

int main()
{
    natural zero;
    assert( zero + zero == zero );
    assert( zero * zero == zero );
    assert( zero - zero == zero );
    natural one( 1 );
    assert( one + zero == one );
    assert( one.power( 2 ) == one );
    natural x2(2);
    natural x7(7);
    natural x14(14);
    natural x9(9);
    natural x5(5);
    natural x3(3);
    natural x35(35);
    natural x45(45);
    natural x28(28);
    natural x10(10);
    natural x20(20);
    natural x27(27);
    assert(x7 * one == x7);
    assert(x7 * x2 == x14);
    assert(x14 - x7 == x7);
    assert(x7 * x5 == x35);
    assert(x14 * x2 == x28);
    assert(x20 - x10 == x10);
    assert(x3.power(2) == x9);
    assert(x3.power(3) == x27);
    assert(x7 + x7 == x14);
    assert(x7 + x7 + x7 + x7 == x28);
    assert(x28 - x14 == x14);
    assert(x10 + x10 == x20);
    assert(x45 - x35 == x10);
    assert(x27 - x20 == x7);
    assert(natural{2} * natural{1} == natural{1 * 2});
    

    return 0;
}
