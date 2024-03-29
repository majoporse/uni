#!/bin/bash

if echo $* | fgrep '|' >/dev/null; then echo lol >&2; exit 1; fi
