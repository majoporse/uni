#!/bin/bash

# Skript automaticky vytvořil IS MU během ověřování nastavení prostředí pro spouštění skriptů.
# Skript lze po ověření funkce libovolně mazat.

echo Skript $0 bezi.
if [ $# -gt 0 ]; then
	echo -n "Parametry: "
	for I in {1..20}; do
		eval echo -n $I=\${$I}
		[ $I -eq $# ] && break
		echo -n ", " 
	done
	echo
fi
echo
PREFIX=~/pv004lab/ukol_skr_c7112
mkdir ${PREFIX}_dir
if [ ! -d ${PREFIX}_dir ]; then
	echo "CHYBA: Nevytvořil se podadresář ${PREFIX}_dir"
	exit 1
fi
rmdir ${PREFIX}_dir
if [ -d ${PREFIX}_dir ]; then
	echo "CHYBA: Nesmazal se podadresář ${PREFIX}_dir"
	exit 1
fi
touch ${PREFIX}_file
if [ ! -f ${PREFIX}_file ]; then
	echo "CHYBA: Nevytvořil se soubor ${PREFIX}_file"
	exit 1
fi
rm ${PREFIX}_file
if [ -f ${PREFIX}_file ]; then
	echo "CHYBA: Nesmazal se soubor ${PREFIX}_file"
	exit 1
fi
echo ok
exit
