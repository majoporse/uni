#include <utility>
#include <cassert>
 
/* Vrátíme se k již známému příkladu s bankovním účtem, který
 * tentokrát rozšíříme o práci s výjimkami – konkrétně pokus o výběr
 * z účtu, na kterém není dostatečný zůstatek, skončí výjimkou. Dále
 * přidáme třídu ‹investment›, která je „duální“ k půjčce: při
 * sestrojení «odečte» peníze z účtu, bude se pravidelně
 * zhodnocovat, a při zničení vrátí investované peníze na původní
 * účet. */

struct insufficient_funds{};

/* Typ ‹account› nechť má metody ‹balance›, ‹deposit› and
 * ‹withdraw›. Startovní zůstatek je 0 a musí zůstat za všech
 * okolností nezáporný. Jakýkoliv pokus o jeho snížení pod nulu musí
 * skončit výjimkou ‹insuficient_funds›. */

struct account{
    double money = 0;
    
    int balance()const {return money;}
    
    void deposit(double moneys){
        money += moneys;
    }

    void withdraw(int to_withdraw){
        if (money - to_withdraw < 0)
            throw insufficient_funds();
        money -= to_withdraw;
    }
};

/* Konečně typ ‹investment›, kterého konstruktor má 3 parametry:
 *
 *  • odkaz (referenci) na hodnotu typu ‹account›,
 *  • sumu, kterou hodláme investovat,
 *  • roční úrok (jako celé číslo v promile).
 *
 * Při sestrojení musí z cílového účtu odebrat potřebné prostředky a
 * při zničení je musí vrátit, včetně nahromaděných úroků. Metoda
 * ‹next_year› připočítá příslušný úrok. */

struct investment{
    bool valid = true;
    /** way of style, but setting sum to zero effectively invalidates investment, no need for extra parm **/
    account &acc;
    /** this is actually very bad, move ** requires ** pointer to account, otherwise ya just copying it **/
    int sum;
    int yearly_ratio;
    investment(account &acc, int sum, int yearly_ratio):acc{acc}, sum{sum}, yearly_ratio{yearly_ratio}{
        acc.withdraw(sum);
    }
    void next_year(){
        sum = sum * (yearly_ratio + 1000) / 1000;
    }
    investment &operator=(investment &&other){
    /** use bracket inicializer, it's simpler **/
        acc = other.acc;
        /** this is copy!! money generator, ako pravic na vychodze **/
        sum = other.sum;
        yearly_ratio = other.yearly_ratio;
        other.valid = false;
        /** same thing with other.sum = 0 **/
        return *this;
    }
    investment(const investment &) = delete;
    /** copy assigment needs to be deleted as well **/
    investment(investment &&) = default;
    /** this really shouldn't be defaulted **/
    ~investment(){
        if (valid)
            acc.deposit(sum);
    }
};

int main()
{
    /* create an account and deposit some money into it */
    account a; a.deposit( 100 );
    const account &c = a;
    assert( c.balance() == 100 );

    bool caught = false; /* remember that we caught an exception */

    try { investment i( a, 200, 0 ); }
    catch ( const insufficient_funds & ) { caught = true; }

    assert( caught );

    {
        investment i( a, 50, 100 );
        i.next_year();
    }

    assert( c.balance() == 105 );

    {
        /* 0-interest investment does nothing */
        investment i( a, 105, 0 );
        i.next_year();
        i.next_year();
    }

    assert( c.balance() == 105 );

    {
        /* interest 100% doubles the investment every year */
        investment i( a, 100, 1000 );
        i.next_year();
        investment j = std::move( i );
        j.next_year();
        i = std::move( j );
    }

    assert( c.balance() == 405 );
    a.withdraw( 400 );
    assert( c.balance() == 5 );

    return 0;
}
