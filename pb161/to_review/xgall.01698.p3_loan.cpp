#include <cassert>
#include <utility>
#include <stdexcept>

/* V tomto příkladu se budeme zabývat (velmi zjednodušenými)
 * bankovními půjčkami. Navrhneme 2 třídy: ‹account›, která bude mít
 * obvyklé metody ‹deposit›, ‹withdraw›, ‹balance›, a které
 * konstruktoru lze předat počáteční zůstatek (v opačném případě
 * bude implicitně nula).
 *
 * Druhá třída bude ‹loan› – její konstruktor přijme «referenci» na
 * instanci třídy ‹account› a velikost půjčky (‹int›). Sestrojením
 * hodnoty typu ‹loan› se na přidružený účet připíše vypůjčená
 * částka. Třída ‹loan› nechť má metodu ‹repay›, která zařídí
 * (případně částečné – určeno volitelným parametrem typu ‹int›)
 * navrácení půjčky. Proběhne-li vše v pořádku, metoda vrátí ‹true›,
 * jinak ‹false›.
 *
 * Zůstatek účtu může být záporný, hodnota půjčky nikoliv. Půjčka
 * musí být vždy plně splacena (tzn. zabraňte situaci, kdy se
 * informace o dluhu „ztratí“ aniž by byl tento dluh splacen). */

class account {
    private:
    int _balance = 0;

    public:
    account() = default;
    account(int given) : _balance{given} {};

    int balance() const{
        return _balance;
    }

    void deposit(int given){
        _balance += given;
    }

    void withdraw(int requested) {
        _balance -= requested;
    }
};

class loan{
    account &borrower;
    int owed;
    

    public:

    loan(const loan&) = delete;
    loan& operator=(loan) = delete;
    loan& operator=(const loan&) = delete;
    loan( loan && ) = delete;
    loan &operator=( loan &&v ) = delete;
    
    loan(account &borrower, int principal) : borrower{borrower}, owed{principal}{
        borrower.deposit(principal);
    };

    ~loan(){
        borrower.withdraw(owed);
    }

    bool repay(){
        borrower.withdraw(owed);
        owed = 0;
        return true;
    }

    bool repay(int payment){
        if (payment > owed) return false;
        owed -= payment;
        borrower.withdraw(payment);
        return true;
    }


};

int main()
{
    account a;

    {
        loan l( a, 1000 );
        assert( a.balance() == 1000 );
        assert( l.repay( 100 ) );
        assert( a.balance() == 900 );
        a.deposit( 200 );
    }

    assert( a.balance() == 200 );

    {
        loan l( a, 500 );
        loan m( a, 100 );
        a.withdraw( 300 );
        assert( a.balance() == 500 );
        assert( m.repay( 50 ) );
        assert( !l.repay( 600 ) );
        assert( l.repay() );
        assert( l.repay() );
    }

    assert( a.balance() == -100 );
    return 0;
}
