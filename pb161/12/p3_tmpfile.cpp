#include <fstream>  /* fstream */
#include <cstdio>   /* remove */
#include <unistd.h> /* access */
#include <cassert>

/* We will implement a simple wrapper around ‹std::fstream› that
 * will act as a temporary file. When the object is destroyed, use
 * ‹std::remove› to unlink the file. Make sure the stream is closed
 * before you unlink the file. */

/* The ‹tmp_file› class should have the following interface:
 *
 *  • a constructor which takes the name of the file
 *  • method ‹write› which takes a string and replaces the content
 *    of the file with that string; this method should flush the
 *    data to the operating system (e.g. by closing the stream)
 *  • method ‹read› which returns the current content of the file
 *  • method ‹stream› which returns a reference to an instance of
 *    ‹std::fstream› (i.e. suitable for both reading and writing)
 *
 * Calling both ‹stream› and ‹write› on the same object is undefined
 * behaviour. The ‹read› method should return all data sent to the
 * file, including data written to ‹stream()› that was not yet
 * flushed by the user. */

class tmp_file{
    std::string name;
    std::fstream _stream;
public:
    tmp_file( const std::string& name ): name{name}{
                _stream = std::fstream( name, std::ios::binary | std::ios::out | std::ios::in | std::ios::trunc);
                
            }

    void write( const std::string& data) {
        _stream << data.data();
        _stream.seekg(0);
    }

    std::string read()     { 
        _stream.seekg(0); 
        std::string s; 
        std::getline( _stream, s, '\0' );
        return s;
    }
    std::fstream& stream() { return _stream;}

    ~tmp_file(){
        _stream.close();
        std::remove( name.data() );
    }
};

int main()
{
auto fs = std::fstream( "t.tmp", std::ios::out);
fs << "hello world\n";
fs.seekg(0); // move the file pointer to the beginning of the file
std::string content;
std::getline( fs, content, '\0' );




    auto check_content = []( auto data )
    {
        std::ifstream ifs( "tmpfile.tmp" );
        std::string content;
        std::getline( ifs, content, '\0' );
        assert( content == data );
    };

    /* We use the POSIX function ‹access› to check file existence.
     * This is not part of the C++ standard and will only work on
     * UNIX-like systems. */

    std::remove( "tmpfile.tmp" );

    {
        assert( ::access( "tmpfile.tmp", F_OK ) );
        tmp_file t( "tmpfile.tmp" );
        assert( ::access( "tmpfile.tmp", F_OK ) == 0 );

        t.write( "hello world\n" );
        check_content( "hello world\n" );
        assert( t.read() == "hello world\n" );
    }

    assert( ::access( "tmpfile.tmp", F_OK ) );

    {
        tmp_file t( "tmpfile.tmp" );
        t.stream() << "bye world" << std::endl;
        check_content( "bye world\n" );
        t.stream() << "... bye";

        assert( t.read() == "bye world\n... bye" );
    }

    assert( ::access( "tmpfile.tmp", F_OK ) );

    return 0;
}
