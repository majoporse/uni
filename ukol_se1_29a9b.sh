#!/bin/bash
who|sed -e 's/^\([^ ]*\).*(\([^)]*\))/Úkol 29a9b: Uživatel \1 z adresy \2/' -e 's/^\([^ ]*\).*(\([^)]*\))/Úkol 29a9b: Uživatel \1/'|sort|uniq
