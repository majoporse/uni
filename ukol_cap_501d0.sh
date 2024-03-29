#!/bin/bash


case $1 in
	-v|verze) echo "verze 4ed"
	exit 0
	;;
	-a|celkem) if [ $# -lt 2 ] || [ ! -e $2 ];then echo "300 hrmenych" >&2;exit 1;fi
	wc -l < $2;
	exit 0
	;;
	-s|vybrane) if [ $# -lt 3 ] ;then echo "300 hrmenych" >&2;exit 1;fi
	grep $3 $2|wc -l
	exit 0
	;;
	-r|nevybrane) if [ $# -lt 3 ]; then
		 echo "300hrmenych" >&2;exit 1;
		 fi;
	grep -v $3 $2 |wc -l
	exit 0
	;;
esac

echo "300 hrmenych" >&2
exit 1