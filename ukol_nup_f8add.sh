#!/bin/bash

if [ ! $# -eq 2 ];then echo 00990 >&2;exit 1; fi

if ! [ $2 -eq $2 ] 2>/dev/null;then exit 1;fi

if [ ! -e $1 ]; then exit 1;fi

SIZE=$(stat -c %s $1)

if [ $SIZE -ge $2 ]; then echo $SIZE; else echo 0; fi

exit 0
