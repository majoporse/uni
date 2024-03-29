#!/bin/bash

for MENO
do
	if echo $MENO | grep .c81 > /dev/null; 
	then mv $MENO ${MENO//.c81/.656};
	else mv $MENO ${MENO}.656;
	fi
done
