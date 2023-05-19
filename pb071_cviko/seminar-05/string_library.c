#include "string_library.h"

#include <signal.h>
#include <stdio.h>

#define UNUSED(param) ((void)(param))
#define NOT_IMPLEMENTED()                                                   \
    do {                                                                    \
        fprintf(stderr, "Unimplemented function '%s' called.\n", __func__); \
        raise(SIGTERM);                                                     \
    } while (0)
#define ASSERT(expr)        \
    do {                    \
        if (!(expr)) {      \
            raise(SIGABRT); \
        }                   \
    } while (0)

size_t string_length(const char *str)
{
    ASSERT(str != NULL);
    size_t i = 0;
    while (str[i] != 0x0)
        ++i;
    return i;
}

char *string_copy(char *result, const char *original)
{
    if (!original)
        return NULL;
    int i = 0;
    while (original[i] != 0x0){
        result[i] = original[i];
        ++i;
    }
    return result;
}

size_t string_count_char(const char *string, char ch)
{
    ASSERT(string);
    int i = 0;
    size_t count = 0;
    while (string[i] != '\0')
        if (string[i++] == ch)
            ++count;
    return count;
}

size_t string_count_substr(const char *original, const char *substring)
{
    int i = 0;
    int j = 0;
    int count = 0;
    while(original[i] != '\0')
    {
        while (original[i] == substring[j] || substring[j] == '\0') {
            if (substring[j] == '\0') {
                ++count;
                break;
            }
            if (original[i] == '\0')
                return count;
            ++i;
            ++j;
        }
        j = 0;
        ++i;
    }

    return count;
}

size_t string_count_string_in_array(const char **array, const char *string)
{
    //TODO
    UNUSED(array);
    UNUSED(string);
    NOT_IMPLEMENTED();
    return 0;
}

void string_split(const char *original, char result[50][256], int *size, char delim)
{
    // TODO
    UNUSED(original);
    UNUSED(result);
    UNUSED(size);
    UNUSED(delim);
    NOT_IMPLEMENTED();
}
