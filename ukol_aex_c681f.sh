#!/bin/bash

RES=0
CUR=0

for NUM
do
	RES=$[ RES + (NUM *++CUR) ]
done

echo "30b90 $RES"
