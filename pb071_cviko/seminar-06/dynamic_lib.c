//
// Created by Wermington on 15.2.16.
//

#include "dynamic_lib.h"

#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "assert.h"

#define UNUSED(a) ((void) (a))
#define NOT_IMPLEMENTED()                                      \
    do {                                                       \
        fprintf(stderr, "%s is not implemented!\n", __func__); \
        raise(SIGTERM);                                        \
    } while (0)

char *dyn_strcpy(const char *str)
{

    assert(str != NULL);
    size_t size = strlen(str) + 1;
    char* new = malloc(size * sizeof(*new));
    for(size_t i = 0; i<size; ++i)
    {
        new[i] = str[i];
    }
    return new;
}

char *dyn_strjoin(const char *pre, const char *post)
{
    assert(pre!=NULL);
    assert(post!=NULL);
    size_t len_1 = strlen(pre);
    size_t len_2 = strlen(post);
    char* res_str = malloc((len_1+len_2 +1)*sizeof(*res_str));
    for (size_t i = 0; i<(len_1+len_2+1); i++)
    {
        res_str[i] = (char) ((i<len_1) ? (pre[i]) : (post[i-len_1]));
    }
    return res_str;
}

char *read_line(void)
{
    int ch;
    size_t size = 1;
    char* res = malloc(size*sizeof(*res));

    while((ch = getchar()) != '\n')
    {
        if (realloc(res, size* sizeof(*res)) == NULL)
            return NULL;

        res[size-1] = (char) ch;
        ++size;
    }
    if (realloc(res, size*sizeof(*res)) == NULL)
        return NULL;
    res[size-1] = '\0';
    return res;
}

void **dyn_alloc2d(size_t rows, const size_t row_sizes[rows])
{
    //TODO
    UNUSED(rows);
    UNUSED(row_sizes);
    NOT_IMPLEMENTED();
    return NULL;
}

int dyn_free2d(void **memory, size_t rows)
{
    // TODO
    UNUSED(rows);
    UNUSED(memory);
    NOT_IMPLEMENTED();
    return 1;
}

/**
 * BONUSES
 */

unsigned **pascal_triangle(size_t depth)
{
    UNUSED(depth);
    NOT_IMPLEMENTED();
    return NULL;
}

char **string_split(const char *orig, const char *splitter, size_t *size)
{
    // TODO
    UNUSED(orig);
    UNUSED(splitter);
    UNUSED(size);
    NOT_IMPLEMENTED();
    return NULL;
}

char *string_replace_all(const char *original, const char *from, const char *to)
{
    // TODO
    UNUSED(original);
    UNUSED(from);
    UNUSED(to);
    NOT_IMPLEMENTED();
    return NULL;
}
