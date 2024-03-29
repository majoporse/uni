#!/bin/bash
echo Zadejte bezprostředně za sebou v tomto pořadí následující znaky:
echo mřížka, obrácené lomítko, vlnka, apostrof, uvozovky, stříška, obrácený apostrof, svislá čára, ampersand, dolar, lomítko
read -r ZNAKY
echo zsv 5514d $ZNAKY > /home/xhatalc/pv004lab/ukol_zsv_neobvykle_znaky_5514d.data
echo Nyní kliknutím v ISu požádejte o ověření splnění úkolu.
