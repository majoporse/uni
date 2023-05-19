#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>

int print_file(const char *path) {

    int fd = open(path, O_RDONLY);
    if (fd == -1) {
        perror("lol");
        return 1;
    }

    char buffer[1024] = {'\0'};
    ssize_t size = 0;

    while ((size = read(fd, &buffer, 1024)) > 0) {
        write(1, buffer, 1024);
    }

    if (close(fd) != 0) {
        perror("lol");
        return 1;
    }

    return 0;
}


int print_stats(const char *path) {

    struct stat stats;
    stat(path, &stats);
    printf("Velikost souboru: %ld", stats.st_size);
    printf("Datum posledniho pristupu: %ld", stats.st_atim.tv_sec);
    printf("UID majitele: %u", stats.st_uid);
    printf("GID majitele: %u", stats.st_gid);
    return 0;
}


int main(int argc, char *argv[]) {

    if (argc != 2) {
        fprintf(stderr, "Invalid amount of arguments\n");
        return 1;
    }

    int (*fun)(const char *);

    if (strcmp(argv[1], "-s") == 0)
        fun = &print_stats;

    else if (strcmp(argv[1], "-f") == 0)
        fun = &print_file;

    else {
        fprintf(stderr, "si kokot\n");
        return 1;
    }

    for (int i = 1; i < argc; ++i) {
        fun(argv[i]);
    }

    return 0;
}
