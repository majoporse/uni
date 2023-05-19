#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "readline.h"

#define UNUSED(VAR) \
    ((void) (VAR))

/**
 * Searches for \p search in each line of \p in and replaces it with
 * stars. The result is written into \p out.
 *
 * \param   search      string to censor
 * \param   in          input file
 * \param   out         output file
 * \return  0 on success, an arbitrary error code on failure
 */
int censor(const char *search, FILE *in, FILE *out)
{
    // TODO: implement the function

    // 1) use one loop to iterate over lines using ‹readline()›
    // 2) use another loop to search for all occurences of ‹search›
    //    using the ‹strstr()› function
    // 3) write the modified line to the ‹out› file

    char * line;
    char * pos;
    size_t len = strlen(search);
    while ((line = readline(in)) != NULL)
    {
        pos = line;
        while ((pos = strstr(pos, search)) != NULL)
        {
            memset(pos, '*', len);
        }
        fprintf(out, "%s", line);
        free(line);
    }
    return 1;
}

int main(int argc, char *argv[])
{
    if (argc != 4) {
        fprintf(stderr, "usage: %s STRING SOURCE DESTINATION\n", argv[0]);
        return EXIT_FAILURE;
    }

    FILE *file1 = fopen(argv[2], "r");
    FILE * file2 = fopen(argv[3], "w");
    censor(argv[1], file1, file2);

    // TODO: open input and output file

    // TODO: call ‹censor()›

    // TODO: close files

    return EXIT_SUCCESS;
}
