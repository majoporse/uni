#include <cassert>

/* Vypočtěte faktoriál zadaného nezáporného čísla. */

int factorial( int n )
{
	if ( n == 0)
	{
		return 1;
	}
	return n * factorial(n-1);
}

int main()
{
    assert( factorial( 0 ) == 1 );
    assert( factorial( 3 ) == 6 );
    assert( factorial( 4 ) == 24 );

    return 0;
}
