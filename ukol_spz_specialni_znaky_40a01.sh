#!/bin/bash
rm -f /home/xhatalc/pv004lab/ukol_spz_specialni_znaky_40a01.txt /home/xhatalc/pv004lab/ukol_spz_specialni_znaky_40a01.data
if [ -f /home/xhatalc/pv004lab/ukol_spz_specialni_znaky_40a01.txt ]; then
	echo Nelze smazat soubor /home/xhatalc/pv004lab/ukol_spz_specialni_znaky_40a01.txt >&2
	exit 1
fi
echo Vepište libovolný neprázdný text a ukončete jej speciálním znakem EOF
cat - > /home/xhatalc/pv004lab/ukol_spz_specialni_znaky_40a01.txt
if [ ! -s /home/xhatalc/pv004lab/ukol_spz_specialni_znaky_40a01.txt ]; then
	rm -f /home/xhatalc/pv004lab/ukol_spz_specialni_znaky_40a01.txt
	echo Nebyl zapsán neprázdný text. Spusťte skript znovu. >&2
	exit 1
fi
rm -f /home/xhatalc/pv004lab/ukol_spz_specialni_znaky_40a01.txt
echo V pořádku.
echo
echo Následující výpis pozastavte speciálním znakem STOP na dobu delší než 2 sekundy.
echo Po uplynutí alespoň 2 sekund ve výpisu pokračujte speciálním znakem START.
PREDTIM=`date +%s`
CITAC=1
while true; do
        echo $CITAC
        sleep 0.5
        NYNI=`date +%s`
        if test $[$NYNI-$PREDTIM] -ge 2; then
                break;
        fi
        PREDTIM=$NYNI
        CITAC=$[$CITAC+1]
done
echo V pořádku.
echo
echo Nyní běžící skript násilně ukončete speciálním znakem INTR.
echo Učiňte tak nejpozději do 10 sekund.
trap '{
	echo 979ce7500c760f40a0120b8120d03e88 > /home/xhatalc/pv004lab/ukol_spz_specialni_znaky_40a01.data
	echo
	echo V pořádku.
	echo Nyní klikněte v ISu na Ověřit správnost vyřešení úkolu.
	exit 0
}' INT
sleep 10
echo Skript nebyl násilně ukončen. Chyba. Spusťte jej znovu.
rm -f /home/xhatalc/pv004lab/ukol_spz_specialni_znaky_40a01.data
exit 1
