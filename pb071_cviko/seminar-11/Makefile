CC=gcc
CFLAGS=-std=c99 -pedantic -Wall -Wextra -D_POSIX_C_SOURCE=200809L

TARGET=posix

all: $(TARGET)

$(TARGET): main.o
	$(CC) -o $@ $^
	
main.o: main.c
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -f $(TARGET) *.o

.PHONY: all clean
