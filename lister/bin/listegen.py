#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Gloværdig generisk listegenerator til RKG!
#
# Hacket sammen af Troels Henriksen <athas@sigkill.dk> den 11. april
# 2010.

import sys, os, re

sys.path += [sys.path[0] + '/..']
from lib import tempita


if len(sys.argv) != 5:
    print "Requires exactly four parameters: paper size, column description file, russes file and supervisors file"
    exit(os.EX_USAGE)

papersize, desc_file, rus_file, sup_file = sys.argv[1:]

widths = []
headers = []

for line in open(desc_file, 'r'):
    match = re.match("^([^ ]*) (.*)$", line)
    widths.append(match.group(1))
    headers.append(match.group(2))

prep = lambda names: ' '.join(name.capitalize() for name in names.split())
read = lambda path: sorted(map(prep, open(path)))
russes = read(rus_file)
supers = read(sup_file)
empties = '& '*(len(headers)-1)
title = os.path.basename(desc_file).rsplit('.',1)[0]

templ = file('templates/list.tex').read()
print tempita.sub(templ, papersize=papersize, widths=widths,
                  headers=headers, russes=russes, supers=supers,
                  title=title,empties=empties)

