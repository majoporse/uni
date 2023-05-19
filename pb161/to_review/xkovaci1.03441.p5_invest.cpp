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
    double curr_balance = 0;

    account() = default;
    account(double balance) : curr_balance{ balance }{}

    void withdraw( double w){
        if (w > curr_balance){
            throw insufficient_funds();
        }
        curr_balance -= w;
    }

    void deposit( double w){
        curr_balance += w;
    }

    double balance() const{
        return curr_balance;
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
    account& my_account;
    double current;
    int interest;

    investment( account& my_account, double investing, int new_interest) : my_account { my_account }, current { investing}, interest { new_interest } {
        my_account.withdraw(current);
    }

    investment& operator= (investment&& other) noexcept {
		my_account = other.my_account;
        interest = other.interest;
        current = other.current;
        other.current = 0;
        return *this;
    }

    investment ( investment&& other ): my_account { other.my_account } , current { other.current}, interest { other.interest } {
        other.current = 0;
    }

    void next_year(){
        current += (current / 1000 ) * interest;
    }

    ~investment(){
        my_account.deposit(current);
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
