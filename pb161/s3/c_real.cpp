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

struct natural
{
    std::vector<bool> data;

    natural() = default;
    natural(int num) { set_vec(num); }
    natural(natural &&other) : data(std::move(other.data)) {}
    natural(const natural &other) = default;
    natural &operator=(const natural &other) = default;
    natural &operator=(natural &&other)
    {
        data = std::move(other.data);
        return *this;
    }
    natural(double val)
    {
        int exponent;
        double significand = std::frexp(val, &exponent);
        significand = scalb(significand, std::numeric_limits<double>::digits);
        exponent -= std::numeric_limits<double>::digits;
        long s = significand;
        if (exponent < 0)
        {
            s = s >> -exponent;
            exponent = 0;
        }
        data = std::vector<bool>(exponent, false);
        set_vec(s);
    }

    friend std::strong_ordering shifted_spaceship(const natural &a,
                                                  const natural &b, /*b is shifted*/
                                                  int shift)
    {
        if (a.size() != b.size() + shift)
            return a.size() <=> b.size() + shift;

        for (int i = a.size() - 1; i >= 0; --i)
        {
            if (a.get(i) && !b.get(i, shift))
                return std::strong_ordering::greater;
            if (!a.get(i) && b.get(i, shift))
                return std::strong_ordering::less;
        }
        return std::strong_ordering::equivalent;
    }

    friend std::strong_ordering operator<=>(const natural &a, const natural &b)
    {
        return shifted_spaceship(a, b, 0);
    }

    friend bool operator==(const natural &a, const natural &b) = default;

    void set_vec(long n)
    {
        for (; n > 0; n >>= 1)
        {
            if ((n % 2) == 1)
                data.push_back(true);
            else
                data.push_back(false);
        }
    }

    bool get(int i, int shift = 0) const
    {
        if ((i - shift) < 0 || (i - shift) >= size())
            return false;
        return data[i - shift];
    }

    int size() const
    {
        if (data.empty())
            return 0;
        return static_cast<int>(data.size());
    }

    natural &shift_plus(const natural &x, int shift)
    {
        bool bigger = size() > x.size() + shift;
        int send = !bigger ? size() : x.size() + shift;

        if (!bigger)
            data.resize(x.size() + shift);

        int end = size();

        bool carry = false;

        int i = 0;
        for (bool a, b; i < end; ++i)
        {
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

    natural &shift_minus(const natural &x /*shifted x has to be smaller*/, int shift)
    {
        int send = x.size() + shift;

        bool carry = false;
        int i = 0;
        int end = size();
        int last_i = -1;
        for (bool a, b; i < end; ++i)
        {
            if (i >= send && !carry)
            {
                last_i = size() - 1;
                break;
            }

            a = data[i];
            b = x.get(i, shift);

            data[i] = (a ^ b) ^ carry;
            if (data[i])
                last_i = i;
            carry = (!a && (b || carry)) || (a && b && carry);
        }
        data.resize(last_i + 1);
        return *this;
    }

    natural &operator+=(const natural &x)
    {
        shift_plus(x, 0);
        return *this;
    }

    natural &operator-=(const natural &x /*x has to be smaller*/)
    {
        return shift_minus(x, 0);
    }

    friend natural operator/(const natural &a, const natural &b)
    {

        if (a < b)
            return {0};
        natural res;
        res.data = std::vector<bool>(a.size() - b.size() + 1, false);
        natural tmp = a;
        for (int shift = a.size() - b.size(); shift >= 0; --shift)
        {
            if (shifted_spaceship(tmp, b, shift) != std::strong_ordering::less)
            {
                res.data[shift] = true;
                tmp.shift_minus(b, shift);
            }
            else if (res.data.back() == 0)
                res.data.pop_back();
        }
        return res;
    }

    friend natural operator+(const natural &a, const natural &b)
    {
        if (a.size() == 0)
            return b;
        if (b.size() == 0)
            return a;
        natural res;
        if (a.size() > b.size())
        {
            res = a;
            res.shift_plus(b, 0);
        }
        else
        {
            res = b;
            res.shift_plus(a, 0);
        }
        return res;
    }

    friend natural operator-(natural a /* a is bigger/equal */, const natural &b)
    {
        a -= b;
        return a;
    }

    friend natural operator*(const natural &a, const natural &b)
    {
        if (a.size() == 0 || b.size() == 0)
        {
            return {0};
        }

        natural res;
        const natural &s = !(a.size() > b.size()) ? a : b;
        const natural &l = a.size() > b.size() ? a : b;

        for (int shift = s.size() - 1; shift >= 0; --shift)
        {
            if (!s.get(shift))
                continue;
            res.shift_plus(l, shift);
        }
        return res;
    }

    friend natural operator%(const natural &a, const natural &b)
    {
        return a - (b * (a / b));
    }

    natural power(int i) const
    {

        natural tmp = *this;
        natural res{1};
        while (i > 0)
        {
            if (i % 2 == 1)
            {
                res = res * tmp;
                --i;
            }
            else
            {
                tmp = tmp * tmp;
                i /= 2;
            }
        }
        return res;
    }
    double get_significand(int s) const
    {
        double res = 0;
        for (int i = size() - 1; s >= 0 && i >= 0; --i, --s)
        {
            if (!data[i])
                continue;
            res += 1ULL << s;
        }
        return res;
    }

    double to_double() const
    {
        int significand_size = std::numeric_limits<double>::digits;
        double exponent = size() - 1 - significand_size;

        double significand = get_significand(significand_size);
        return significand * std::pow(2, exponent);
    }

    std::vector<natural> digits(const natural &base)
    {
        std::vector<natural> powers = {1};
        while (powers.back() < *this)
        {
            powers.emplace_back(powers.back() * base);
        }
        if (powers.back() > *this)
            powers.pop_back();
        natural tmp = *this;
        std::vector<natural> res;
        for (auto [rit, count] = std::tuple{powers.rbegin(), 0}; rit != powers.rend(); ++rit, count = 0)
        {
            res.emplace_back(tmp / *rit);
            tmp = tmp - res.back() * *rit;
        }
        return res;
    }
};

/* Předmětem této úlohy je naprogramovat typ ‹real›, který
 * reprezentuje reálné číslo s libovolnou přesností a rozsahem.
 *
 * Z hodnot:
 *
 *  • ‹a›, ‹b› typu ‹real›,
 *  • ‹k› typu ‹int›
 *
 * nechť je lze utvořit tyto výrazy, které mají vždy přesný
 * výsledek:
 *
 *  • ‹a + b›, ‹a - b›, ‹a * b›, ‹a / b›,
 *  • ‹a += b›, ‹a -= b›, ‹a *= b›, ‹a /= b›,
 *  • ‹a == b›, ‹a != b›, ‹a < b›, ‹a <= b›, ‹a > b›, ‹a >= b›,
 *  • ‹-a› – opačná hodnota,
 *  • ‹a.abs()› – absolutní hodnota,
 *  • ‹a.reciprocal()› – převrácená hodnota (není definováno pro 0),
 *  • ‹a.power( k )› – mocnina (včetně záporné).
 *
 * Výrazy, které nemají přesnou explicitní (číselnou) reprezentaci
 * jsou parametrizované požadovanou přesností ‹p› typu ‹real›:
 *
 *  • ‹a.sqrt( p )› – druhá odmocnina,
 *  • ‹a.exp( p )› – exponenciální funkce (se základem ⟦e⟧),
 *  • ‹a.log1p( p )› – přirozený logaritmus ⟦\ln(1 + a)⟧, kde
 *    ⟦a ∈ (-1, 1)⟧.
 *
 * Přesností se myslí absolutní hodnota rozdílu skutečné (přesné) a
 * reprezentované hodnoty. Pro aproximaci odmocnin je vhodné použít
 * Newtonovu-Raphsonovu metodu (viz ukázka z prvního týdne). Pro
 * aproximaci transcendentálních funkcí (exponenciála a logaritmus)
 * lze s výhodou použít příslušných mocninných řad. Nezapomeňte
 * ověřit, že řady v potřebné oblasti konvergují. Při určování
 * přesnosti (počtu členů, které je potřeba sečíst) si dejte pozor
 * na situace, kdy členy posloupnosti nejprve rostou a až poté se
 * začnou zmenšovat.
 *
 * Konečně je-li ‹d› hodnota typu ‹double›, nechť jsou přípustné
 * tyto konverze:
 *
 *  • ‹real x( d )›, ‹static_cast< real >( d )›,
 *
 * Poznámka: abyste se vyhnuli problémům s nejednoznačnými
 * konverzemi, je vhodné označit konverzní konstruktory a operátory
 * pro hodnoty typu ‹double› klíčovým slovem ‹explicit›. */

struct real
{
    natural nom;
    natural denom;
    bool is_negative = false;

    real(natural nom, natural denom) : nom(nom), denom(denom) { reduce(); }
    real(const real &other) = default;
    real() : denom{1} {}
    real &operator=(const real &other) = default;
    real(double d)
    {
        if (d < 0)
        {
            is_negative = true;
            d = -d;
        }
        int exponent;
        double significand = std::frexp(d, &exponent);
        significand = scalb(significand, std::numeric_limits<double>::digits);
        exponent -= std::numeric_limits<double>::digits;

        nom = {significand * (exponent > 0 ? std::pow(2, exponent) : 1)};
        denom = {exponent > 0 ? 1 : std::pow(2, std::abs(exponent))};
        reduce();
    }

    real abs()
    {
        real new_real = *this;
        new_real.is_negative = false;
        return new_real;
    }

    real reciprocal() const
    {
        real new_real = *this;
        std::swap(new_real.nom, new_real.denom);
        return new_real;
    }

    void reduce()
    {
        natural gcd_var = gcd(nom, denom);
        nom = nom / gcd_var;
        denom = denom / gcd_var;
    }

    real operator-() const
    {
        real new_real = *this;
        new_real.is_negative = !new_real.is_negative;
        return new_real;
    }
    real operator+=(const real &other)
    {

        natural nl = nom * other.denom;
        natural nr = other.nom * denom;
        if (is_negative == other.is_negative)
        {
            nom = nl + nr;
        }
        else if (nl > nr)
        {
            nom = nl - nr;
        }
        else
        {
            nom = nr - nl;
            is_negative = nl != nr;
        }
        denom = denom * other.denom;
        reduce();
        return *this;
    }

    real operator-=(const real &other)
    {
        return *this += -other;
    }

    real operator*=(const real &other)
    {
        nom = nom * other.nom;
        denom = denom * other.denom;
        is_negative = is_negative != other.is_negative;
        reduce();
        return *this;
    }

    real operator/=(const real &other)
    {
        return *this *= other.reciprocal();
    }

    friend real operator+(real a, const real &b)
    {
        a += b;
        return a;
    }

    friend real operator-(real a, const real &b)
    {
        a -= b;
        return a;
    }

    friend real operator*(real a, const real &b)
    {
        a *= b;
        return a;
    }

    friend real operator/(real a, const real &b)
    {
        a /= b;
        return a;
    }

    double to_double() const
    {
        return nom.to_double() / denom.to_double();
    }
    friend bool operator==(const real &a, const real &b) { return a.nom == b.nom && a.denom == b.denom; }
    friend bool operator!=(const real &a, const real &b) { return !(a == b); }
    friend std::strong_ordering operator<=>(const real &a, const real &b)
    {
        if (a.is_negative && !b.is_negative)
            return std::strong_ordering::less;
        if (!a.is_negative && b.is_negative)
            return std::strong_ordering::greater;
        if (a.is_negative && b.is_negative)
            return b.nom * a.denom <=> a.nom * b.denom;
        return a.nom * b.denom <=> b.nom * a.denom;
    }

    real power(int k)
    {
        real new_real = k > 0 ? real{nom.power(k), denom.power(k)} : real{denom.power(-k), nom.power(-k)};
        new_real.is_negative = this->is_negative && k % 2 != 0;
        new_real.reduce();
        return new_real;
    }

    real sqrt(real l)
    {
        real x = *this;
        real y = real{1, 2} * (x + 1);

        while ((x - y).abs() > l)
        {
            x = y;
            y = real{1, 2} * (x + *this / x);
        }

        return y;
    }

    natural gcd(natural a, natural b)
    {

        while (b != 0)
        {
            natural temp = std::move(b);
            b = a % temp;
            a = temp;
            if (a == 0)
                return b;
        }
        return a;
    }

    real exp(real x)
    {
        real sum = 1;
        real term = 1;
        for (real i = 1; term.abs() * 10 > x; i += 1)
        {
            term *= *this / i;
            sum += term;
        }
        return sum;
    }

    real log1p(real p){
        real x = *this;
        real term = x;
        real sum = x;
        int i = 2;
        while (term.abs() > p)
        {
            term *= -x * real{i - 1, i};
            sum += term;
            i += 1;
        }
        return sum;
    }

    natural lcm(natural n1, natural n2)
    {
        return (n1 * n2) / gcd(n1, n2);
    }
};

int main()
{
    real zero = 0;
    real one = 1;
    real ten = 10;
    real half = one / 2;

    real eps = ten.power(-3);

    real pi(3.14159265);
    real sqrt2(1.41421356);
    real e(2.71828182);
    real l_half(0.40546511);

    assert((one.exp(eps) - e).abs() < eps);
    assert(zero.log1p(eps).abs() < eps);
    assert((half.log1p(eps) - l_half).abs() < eps);
    assert(static_cast<real>(1.0) == one);
    assert(one + -one == zero);
    assert(one * ten == ten);
    {
        real zero{0};
        real one{1};
        real two{2};
        real three{3};
        real ten{10};
        real eps = ten.power(-2);
        real eps_10 = eps / ten;
        real pi = real(314159265) / real(100000000);
        real sqrt2 = real(141421356) / real(100000000);
        real e = real(271828182) / real(100000000);
        real lhalf = real(40546511) / real(100000000);
        real half = one / two;
        auto a = (two.sqrt(eps) - sqrt2).to_double();
        assert((two.sqrt(eps) - sqrt2).abs() < eps);
        assert(a);
    }
    {
        int i = 10;
        real x{real(-11) / real(13)};
        assert(x.power(i - 2) > x.power(i));
    }
    {
        real small_1{0};
        real big_1{real(0x7fffffff - 1) / real(13)};
        real big_2{big_1 * big_1 + big_1};
        real big_3{big_2 * big_2 + small_1};
        real a{};
        real b{};
        real small_2{0};
        a = a + big_3;
        assert(a == a + big_3 - big_3);
        assert(a - big_3 == b);
    }
    {
        real x{ real( -11 ) / real( 13 )};
        real y{ real( 11 ) / real( 13 )};
        real z{ real( 13 ) / real( 11 )};
        real u{ real( 13 ) / real( -11 )};
        assert(x.power( 1 - 2 ) < x.power( 1 ));
    }
    {
        real x{ real( -11 ) / real( 13 )};
        real y{ real( 11 ) / real( 13 )};
        real z{ real( 13 ) / real( 11 )};
        real u{ real( 13 ) / real( -11 )};
        int i = 1;
        assert (y.power( i ) < y.power( i - 2 ));
        assert (y.power( i ) < y.power( i - 1 ));
        assert (z.power( i - 2 ) < z.power( i ));
        assert (z.power( i - 1 ) < z.power( i ));
        assert (x.power( i - 2 ) < x.power( i ));
        assert (x.power( i ) < x.power( i - 1 ));
        assert (u.power( i ) < u.power( i - 2 ));
    }

    return 0;
}
