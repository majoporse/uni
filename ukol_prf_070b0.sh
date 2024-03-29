#!/bin/bash

if test $# -lt 1;then TMP=`grep '' /etc/passwd`;else TMP=`grep -e $1 /etc/passwd`;fi

while read LINE;
do
FIRST=$(echo $LINE | cut -f1 -d':')
SEC=$(echo $LINE | cut -f3 -d':')
THIRD=$(echo $LINE | cut -f4 -d:)
printf '%+16s | %-5s | %s\n' $FIRST $SEC $THIRD
done <<<"$TMP"
