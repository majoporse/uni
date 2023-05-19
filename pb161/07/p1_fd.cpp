#include <memory>
#include <fcntl.h>
#include <unistd.h>
#include <system_error>
#include <cassert>
#include <vector>

/* Dle normy POSIX, otevřením souboru nebo podobného zdroje získáme
 * tzv. «popisovač otevřeného souboru» (angl. file descriptor), malé
 * celé číslo, které pak lze dále předávat systémovým voláním (např.
 * ‹read› nebo ‹write›). Není-li již zdroj potřebný, popisovač je
 * nutné uvolnit systémovým voláním ‹close› (a to právě jednou – je
 * důležité, aby stejný popisovač nebyl uvolněn dvakrát).
 *
 * Naprogramujte typ ‹fd›, který bude popisovač souboru uchovávat, a
 * zároveň zabezpečí, že ho není lze omylem ztratit (aniž bychom ho
 * uvolnili) ani omylem uvolnit vícenásobně.
 *
 * Hodnoty typu ‹fd› nechť je možné přesouvat (a přiřazovat
 * přesunutím), a vytvářet dvěma způsoby:
 *
 *  1. funkcí ‹fd_open( path, flags )›, která vnitřně použije
 *     systémové volání ‹open› a výsledný popisovač vrátí jako hodnotu
 *     typu ‹fd›,
 *  2. funkcí ‹fd_dup( raw_fd )›, která přijme číselný (syrový,
 *     nechráněný) popisovač a systémovým voláním ‹dup› vytvoří jeho
 *     «chráněnou» kopii typu ‹fd›.
 *
 * Parametr ‹path› je typu ‹const char *› a stačí jej přeposlat
 * systémovému volání tak, jak ho obdržíte – není potřeba jej
 * jakkoliv kontrolovat nebo interpretovat. Více informací
 * o voláních ‹open› a ‹dup› získáte příkazy ‹man 2 open› a ‹man 2
 * dup› na stroji ‹aisa›.
 *
 * Typ ‹fd› nechť má dále metody ‹read› a ‹write›, které vrátí resp.
 * přijmou, vektor bajtů (jako hodnot typu ‹char›). Počet bajtů,
 * které je potřeba načíst, dostane metoda ‹write› jako parametr.
 *
 * Více informací o potřebných funkcích získáte opět příkazy ‹man 2
 * read› and ‹man 2 write›.
 *
 * Selže-li některé ze systémových volání ‹open›, ‹read› nebo
 * ‹write›, ukončete dotčenou funkci výjimkou ‹std::system_error›.
 * Pokus o čtení nebo zápis s použitím neplatného popisovače
 * (implicitně sestrojeného, vykradeného, nebo již uzavřeného) nechť
 * skončí výjimkou ‹std::invalid_argument›. */

struct handle{
    int file;
    handle(const char *name, int flags): file{::open(name, flags)}{}
    handle(int i): file{::dup(i)}{}
    handle(const handle &other) = default;
    ~handle(){::close(file);}
};

struct fd{

    std::shared_ptr<handle> opened;

    fd (fd &&other) {opened = other.opened; other.opened = nullptr;}

    fd (const fd &other) {opened = other.opened;}

    fd() = default;

    fd(int i) : opened{std::make_shared<handle>(i)}{};

    fd(const char *path, int flags) : opened{std::make_shared<handle>(path, flags)}{}

    fd &operator=(const fd &other) = default;

    std::vector< char > read(int ammount){
        if (!opened) throw std::invalid_argument("kokotina");
        std::vector< char > res(ammount, 0);
        int red;
        if((red = ::read(opened->file, &res[0], ammount)) == -1)
            throw std::system_error();
        res.resize(red);
        return res;
    }

    void write(std::vector<char> text){
        int ammount = text.size();
        ::write(opened->file, &text[0], ammount);
    }

    void close(){
        opened.reset();
        opened = nullptr;
    }

};

fd fd_open(const char *path, int flags ){
    return {path, flags};
}

fd fd_dup(int raw_fd ){
    return {raw_fd};
}

int main()
{
    using bytes = std::vector< char >;

    int fd_0 = ::open( "/dev/null", O_WRONLY );
    assert( fd_0 >= 0 );
    ::close( fd_0 );

    fd null = fd_open( "/dev/null", O_WRONLY );
    fd zero = fd_open( "/dev/zero", O_RDONLY );
    fd rand = fd_open( "/dev/urandom", O_RDONLY );
    fd std_in = fd_dup( 0 );

    int caught = 0;

    try { null.read( 10 ); }
    catch ( const std::system_error & ) { ++ caught; }
    assert( caught == 1 );

    assert(( zero.read( 5 ) == bytes{ 0, 0, 0, 0, 0 } ));
    assert(( rand.read( 5 ) != bytes{ 0, 0, 0, 0, 0 } ));

    null = fd_open( "/dev/null", O_RDWR );
    assert( null.read( 5 ).empty() );

    {
        null.write( { 'n', 'o', 'p', 'e' } );
        zero.close();
        fd x = std::move( null );

        try { zero.read( 10 ); }
        catch ( const std::invalid_argument & ) { ++ caught; }
        assert( caught == 2 );

        try { null.read( 10 ); }
        catch ( const std::invalid_argument & ) { ++ caught; }
        assert( caught == 3 );
    }

    {
        fd n2;
        {
            fd n1 = fd_open( "/dev/null", O_WRONLY );
            n1.close();
            n2 = fd_open( "/dev/null", O_WRONLY );
        }

        n2.write( { 'f', 'o', 'o' }  );
    }

    {
        ::close( ::open( "g1_fd.out", O_CREAT, 0666 ) );
        fd file_out = fd_open( "g1_fd.out", O_WRONLY );
        file_out.write( { 'E', 'H', 'L', 'O', '\n' } );
        fd file_in = fd_open( "g1_fd.out", O_RDONLY );
        ::unlink( "g1_fd.out" );
        assert(( file_in.read( 3 ) == bytes{ 'E', 'H', 'L' } ));
    }

    assert( ::open( "/dev/null", O_WRONLY ) == fd_0 );

    return 0;
}
