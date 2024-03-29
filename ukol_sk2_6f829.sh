#!/bin/bash

NAME=$1
CUR=0
shift

for SUBOR
do
	echo "-- $[ ++CUR ]. `basename ${SUBOR}` 3deea8c015ebd30470b7" >> $NAME;
	cat $SUBOR >> $NAME;
	
done