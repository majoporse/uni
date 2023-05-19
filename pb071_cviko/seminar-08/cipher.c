#include <assert.h>
#include <stdlib.h>
#include <stdio.h>

// Do *NOT* use ‹readline()› in this exercise! It will not work as you expect.
// #include "readline.h"

#define BLOCK_SIZE 512
#define UNUSED(VAR) \
    ((void) (VAR))

/**
 * Reads 512 binary bytes from \p key and uses it as key to "encrypt"
 * each block of 512 from \p in. Resulting blocks are written to \p out.
 *
 * @param   key         the file to read key from
 * @param   in          input file
 * @param   out         output file
 * @return  0 on success, an arbitrary error code on failure
 */
int xorcrypt(FILE *key, FILE *in, FILE *out)
{
    // TODO: implement the function
    // 1) read the key to a 512 byte long buffer using ‹fread()›
    // 2) read 512 byte blocks from ‹in› file
    // 3) for each such block use the xor operator ‹^› (caret) to encrypt
    //    each byte of the block with the respective byte in the ‹key› block
    // 4) write the modified block to the ‹out› file
    //
    // Note that the last block may be smaller than 512 bytes.
    // You sould take this into account when implementing this function.
    unsigned long bytes_read = 0;
    char key_array[BLOCK_SIZE];
    char buffer[BLOCK_SIZE];

    if (fread(key_array, 1, BLOCK_SIZE, key) != BLOCK_SIZE)
        return EXIT_FAILURE;

    while((bytes_read = fread(buffer, 1, BLOCK_SIZE,in)) > 0)
    {
        for (unsigned i = 0; i < bytes_read; i++) {
            buffer[i] ^= key_array[i];
        }
        fwrite(buffer,1, bytes_read, out);
        fflush(out);
    }

    return EXIT_SUCCESS;
}

int main(int argc, char *argv[])
{
    if (argc != 4) {
        fprintf(stderr, "usage: %s KEY INPUT OUTPUT\n", argv[0]);
        return EXIT_FAILURE;
    }
    FILE *file_input = fopen(argv[2], "rb");
    FILE *file_output = fopen(argv[3], "wb");
    FILE *key_file = fopen(argv[1], "rb");

    if (file_input == NULL || file_output == NULL || key_file == NULL){
        return EXIT_FAILURE;
    }
    int result = xorcrypt(key_file, file_input,file_input);

    fclose(key_file);
    fclose(file_input);
    fclose(file_output);

    // TODO: open files

    // TODO: call ‹xorcrypt()›

    // TODO: close files

    return result;
}
