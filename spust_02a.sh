#!/bin/bash

DIR701="/home/xhatalc/pv004lab/ukol_sae_f45e9"
RODIC_PID=$$
export RODIC_PID
bash $DIR701/vnoreny_02a.sh
source $DIR701/aktualni_02a.sh
exit 0