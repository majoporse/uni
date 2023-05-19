/** Grade: @B
 **
 ** ---
 **
 ** x = OK, - = minor issues, ! = major issues
 **
 ** * [-] clearly describes solution to the problem
 **   * from double, to double: I would definitely prefer some comments here and
 ** there
 ** * [x] correctly decomposes the problem
 ** * [-] doesn't have code duplication
 **   * careful about that plus/minus, I would like you to try to address that
 ** * [x] uses correct abstractions, algorithms and data structures
 **   * `1ULL << something`: please address that
 **
 ** ---
 **
 ** Summary (+1s, suggestions, rants, confessions, etc.):
 ** * n/a
 **
 ** ---
 **
 ** In case you have anything to discuss or want to clarify any of my comments
 ** from the review, feel free to reach out via mail or Discord. **/
#include <cassert>
#include <vector>
#include <compare>
#include <cmath>
#include <limits>
#include <tuple>
#include <iostream>

/* Tento úkol rozšiřuje ‹s1/f_natural› o tyto operace (hodnoty ‹m› a
 * ‹n› jsou typu ‹natural›):
 *
 *  • konstruktor, který přijme nezáporný parametr typu ‹double› a
 *    vytvoří hodnotu typu ‹natural›, která reprezentuje dolní
 *    celou část parametru,
 *  • operátory ‹m / n› a ‹m % n› (dělení a zbytek po dělení;
 *    chování pro ‹n = 0› není definované),
 *  • metodu ‹m.digits( n )› která vytvoří ‹std::vector›, který bude
 *    reprezentovat hodnotu ‹m› v soustavě o základu ‹n› (přitom
 *    nejnižší index bude obsahovat nejvýznamnější číslici),
 *  • metodu ‹m.to_double()› která vrátí hodnotu typu ‹double›,
 *    která co nejlépe aproximuje hodnotu ‹m› (je-li ⟦l = log₂(m) -
 *    52⟧ a ‹d = m.to_double()›, musí platit ‹m - 2ˡ ≤ natural( d )›
 *    a zároveň ‹natural( d ) ≤ m + 2ˡ›; je-li ‹m› příliš velké, než
 *    aby šlo typem ‹double› reprezentovat, chování je
 *    nedefinované).
 *
 * Převody z/na typ ‹double› musí být lineární v počtu bitů
 * operandu. Dělení může mít složitost nejvýše kvadratickou v počtu
 * bitů levého operandu. Metoda ‹digits› smí vůči počtu bitů ‹m›,
 * ‹n› provést nejvýše lineární počet «aritmetických operací» (na
 * hodnotách ‹m›, ‹n›). */



struct natural{
    std::vector<bool> data;

    natural()= default;
    natural(int num) { set_vec(num); }
    natural(double val){
        int exponent;
        double significand = std::frexp(val, &exponent);
        significand = scalb(significand, std::numeric_limits<double>::digits);
        exponent -= std::numeric_limits<double>::digits;
        long s = significand;
        if (exponent < 0){
            s = s >> -exponent;
            exponent = 0;
        }
        data = std::vector< bool >( exponent, false);
        set_vec(s);
    }

    friend std::strong_ordering shifted_spaceship(const natural &a, 
                                                  const natural &b, /*b is shifted*/ 
                                                  int shift){
        if (a.size() != b.size() + shift) return a.size() <=> b.size() + shift;

        for(int i = a.size() -1; i >= 0; --i){
/** ```suggestion:-1+0
 **             if (a.get(i) != b.get(i, shift)) {
 **                 return a.get(i) <=> b.get(i, shift);
 **             }
 ** ``` **/
            if (a.get(i) && ! b.get(i, shift)) return std::strong_ordering::greater;
            if (!a.get(i) && b.get(i, shift)) return std::strong_ordering::less; 
        }
        return std::strong_ordering::equivalent;
    }

    friend std::strong_ordering operator<=>(const natural &a, const natural &b){
        return shifted_spaceship(a, b, 0);
    }

    friend bool operator==(const natural &a, const natural &b) = default;


    void set_vec(long n){
        for (; n > 0; n >>= 1){
/** You're joking, right?
 **
 ** ```suggestion:-3+0
 **             data.push_back((n % 2) == 1);
 ** ``` **/
            if ((n % 2) == 1)
                data.push_back(true);
            else
                data.push_back(false);
        }
    }

    bool get(int i, int shift = 0) const{
/** You could totally do
 **
 **     return 0 <= (i - shift) && (i - shift) < size() && data[i - shift];
 **
 ** However since it is “an edge-case”, I'm willing to miss it ;) **/
        if ((i - shift) < 0 || (i - shift) >= size()) return false;
        return data[i - shift];
    }


    int size()const{
/** Is there an issue with casting `unsigned` zero to `int`? :thonk: **/
        if (data.empty())
            return 0;
        return static_cast<int>(data.size());
    }

    natural &shift_plus(const natural &x, int shift){
        bool bigger = size() > x.size() + shift;
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

/** You have »very« similar `plus` and `minus`, do you think that you could try to
 ** avoid the code duplication somehow? :P **/
    natural &shift_minus(const natural &x /*shifted x has to be smaller*/, int shift){
        int send = x.size() + shift;

        bool carry = false;
        int i = 0;
        int end = size();
        int last_i = -1;
        for (bool a, b; i < end; ++ i){
            if (i >= send && !carry){
                last_i = size() -1;
                break;
            }

            a = data[i];
            b = x.get(i, shift);

            data[i] = (a ^ b) ^ carry;
            if (data[i]) last_i = i;
            carry = (!a && (b || carry)) || (a && b && carry);
        }
        data.resize(last_i + 1);
        return *this;
    }

    natural &operator+=(const natural &x){
        shift_plus(x, 0);
        return *this;
    }

    natural &operator-=(const natural &x /*x has to be smaller*/){
        return shift_minus(x, 0);
    }

    friend natural operator/(const natural&a, const natural &b){

        if (a < b)
            return {0};
        natural res;
        res.data = std::vector<bool>( a.size() - b.size() + 1, false);
        natural tmp = a;
        for (int shift = a.size() - b.size(); shift >= 0; --shift){
            if (shifted_spaceship(tmp, b, shift) != std::strong_ordering::less){
                res.data[shift] = true;
                tmp.shift_minus(b, shift);
            }else if (res.data.back() == 0)
                res.data.pop_back();
        }
        return res;
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
        const natural &s = !(a.size() > b.size()) ? a : b;
        const natural &l = a.size() > b.size() ? a : b;

        for (int shift = s.size() -1; shift >= 0; --shift){
            if (!s.get(shift))
                continue;
            res.shift_plus(l, shift);
        }
        return res;
    }

    friend natural operator%(const natural &a, const natural &b){
/** I would recommend you looking into computing division and modulo at the same
 ** time… This works, but is not very efficient :/ **/
        return a - (b*(a/b));
    }

    natural power(int i)const{
        
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
    double get_significand(int s){
        double res = 0;
        for (int i = size() - 1; s >= 0 && i >= 0; --i, --s){
            if (!data[i])
                continue;
/** You need to be very careful here, cause you can easily cause an undefined
 ** behavior. Do you know why?
 **
 ** And if you think it's not the case, please reach out and explain. **/
            res += 1ULL << s;
        }
        return res;
    }

    double to_double(){
        int significand_size = std::numeric_limits<double>::digits;
        double exponent = size() - 1 - significand_size;

        double significand = get_significand(significand_size);
        return significand * std::pow(2, exponent);
    }

    std::vector<natural> digits(const natural &base){
/** Could you try having »one« variable of type `natural` and just keep it shifting?
 **  I believe that you should be able to get it to the exponent you need and then
 ** just go down… **/
        std::vector< natural > powers = {1};
        while (powers.back() < *this) {powers.emplace_back(powers.back() * base);}
        if (powers.back() > *this)
            powers.pop_back();
        natural tmp = *this;
        std::vector< natural >res;
        for (auto [rit, count] = std::tuple{powers.rbegin(), 0}; rit != powers.rend(); ++rit, count = 0) {
            res.emplace_back( tmp / *rit);
            tmp = tmp - res.back() * *rit;
        }
        return res;
        // natural biggest = base.power(data.size() / base.data.size());
        // natural tmp = *this;
        // std::vector< natural >res;
        // for (; biggest > 0; biggest = biggest / base) {
        //     res.emplace_back( tmp / biggest);
        //     tmp = tmp - res.back() * biggest;
        // }
        // return res;
    }

};

// std::vector< natural > digi(double i, int base){
//     std::vector< double > res;
//     for (;i > 0; i = std::floor(i/base)){
//         res.push_back(fmod(i, base));
//     }
//     std::vector< natural > a;
//     while (!res.empty()) { a.emplace_back(res.back()); res.pop_back();}
//     return a;
// }

int main()
{
    // natural zero;
    // assert( zero + zero == zero );
    // assert( zero * zero == zero );
    // assert( zero - zero == zero );
    // natural one( 1 );
    // assert( one + zero == one );
    // assert( one.power( 2 ) == one );
    // natural x2(2);
    // natural x7(7);
    // natural x14(14);
    // natural x9(9);
    // natural x5(5);
    // natural x3(3);
    // natural x35(35);
    // natural x45(45);
    // natural x28(28);
    // natural x10(10);
    // natural x20(20);
    // natural x27(27);
    // assert(x7 * one == x7);
    // assert(x7 * x2 == x14);
    // assert(x14 - x7 == x7);
    // assert(x7 * x5 == x35);
    // assert(x14 * x2 == x28);
    // assert(x20 - x10 == x10);
    // assert(x3.power(2) == x9);
    // assert(x3.power(3) == x27);
    // assert(x7 + x7 == x14);
    // assert(x7 + x7 + x7 + x7 == x28);
    // assert(x28 - x14 == x14);
    // assert(x10 + x10 == x20);
    // assert(x45 - x35 == x10);
    // assert(x27 - x20 == x7);
    // assert(natural{2} * natural{1} == natural{1 * 2});
    
    // for (int i = 0; i < 500; ++i)
    //     assert(natural{510} - natural{i} == natural{510-i});
    // assert(natural{50} / natural{7} == natural{50/7});
    // for (int i = 1; i < 50; ++i){
    //     for (int j = 50; j < 60; ++j)
    //         assert(natural{j} / natural{i} == natural{j/i});
    // }
    // int a = 1;
    // double b = 1.7542;
    // for (;a < 10000; ++a, ++b){
    //     assert(natural{a} == natural{b});
    //     assert(natural{natural{std::pow(2, 300)}.to_double()} == natural{std::pow(2, 300)});
    //     assert(natural{a}.to_double() == natural{b}.to_double());
    // }
// == digi(std::pow(2, 50) + i, 10)
    // natural{123}.digits(10);
    // for (int i = 0; i < 10000; ++i)
    //     assert(natural{std::pow(2, 50) + i}.digits(1000) == digi(std::pow(2, 50) + i, 1000));

    // for(int i = 0; i < 10000; ++i)
    //     assert(natural{std::pow(2, 52) + i} % natural{5} == natural{std::fmod(std::pow(2, 52) + i, 5)});

    // for (int i = 0; i < 1000; ++i){
    //     for (int j = 1; j < 100; ++j)
    //         assert(natural{i} / natural{j} == natural{i / j});
    // }

    // for(double i = std::pow(2, 40); i < std::pow(2, 40) + 100; ++i){
    //     assert(std::fabs( natural{i}.to_double() - i ) < 1e-10);
    // }
    // natural m( 2.1 ), n( 2.9 );
    // assert( m == n );
    // assert( m / n == 1 );
    // assert( m % n == 0 );
    // assert( m.digits( 10 ).size() == 1 );
    // assert( m.to_double() == 2.0 );
    return 0;
}
