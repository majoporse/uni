#!/bin/bash

FILE=/home/xhatalc/pv004lab/ukol_geo_4aaaa.data

if test $# -eq 0; then echo debyl >&2;exit 1; fi

while getopts 'hdva:o:' MENO; do
	case "$MENO" in
		h)    echo Napoveda >&2;;
		a)    echo $OPTARG >> $FILE;;
		d)    if ! test -f $FILE; then exit 0; fi; rm $FILE;;
		o)    echo $OPTARG > $FILE;;
		v)    if ! test -f $FILE; then exit 0; fi; cat $FILE;;
		?)    echo "Byla zadána chybná volba" >&2; exit 1 ;;
	esac
done
