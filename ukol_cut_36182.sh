#!/bin/bash
cat /etc/passwd | cut -f1,3 -d:
if test $# -lt 1;then exit 1;fi
if cat /etc/passwd | cut -f3 -d: | grep ^$*$ >/dev/null;then exit 0;else exit 1;fi
