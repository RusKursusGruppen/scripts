#!/bin/sh

latex -halt-on-error -file-line-error $@ | egrep '^.*:[0-9]+:' || exit 0
