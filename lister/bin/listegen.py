#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Gloværdig generisk listegenerator til RKG!
#
# Hacket sammen af Troels Henriksen <athas@sigkill.dk> den 11. april
# 2010.

import sys, os, re

sys.path += [sys.path[0] + '/..']
from lib import tempita


if len(sys.argv) != 4:
    print "Requires exactly three parameters: paper size, column description file, and first column data"
    exit(os.EX_USAGE)

papersize, desc_file, data_file = sys.argv[1:]

widths = []
headers = []

for line in open(desc_file, 'r'):
    match = re.match("^([^ ]*) (.*)$", line)
    widths.append(match.group(1))
    headers.append(match.group(2))

cap = lambda names: ' '.join(name.capitalize() for name in names.split())
russes = sorted(map(cap, open(data_file)))
empties = '& '*(len(headers)-1)
title = os.path.basename(desc_file).rsplit('.',1)[0]

templ = file('templates/list.tex').read()
print tempita.sub(templ, papersize=papersize, widths=widths,
                  headers=headers, russes=russes, title=title,
                  empties=empties)

