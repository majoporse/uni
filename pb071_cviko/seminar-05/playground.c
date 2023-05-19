#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "string_library.h"

void play_split()
{
    const char *original = "Ahoj svet 000 Query";
    char result[50][256];
    int size;
    char delim = ' ';

    string_split(original, result, &size, delim);
    printf("SPLIT: \nSize: %d\nParts: \n", size);
    for (int i = 0; i < size; i++) {
        printf("   %d. - %s\n", i + 1, result[i]);
    }
}

int main(void)
{
    string_count_substr("Ahoj", "A");

    return 0;
}
