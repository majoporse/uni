#!/bin/bash

factorial(){
    echo "define f (x){ if (x <= 1) return (1); return (f(x-1) * x); }; f($1)" | bc -l
}

if test $# -lt 1 || ! test $1 -eq $1 > /dev/null 2>&1 || test $1 -lt 0 || test $1 -gt 20; then 
exit 1; fi


factorial $1

# autor edb76
