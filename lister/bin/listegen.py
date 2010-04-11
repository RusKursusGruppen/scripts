#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Gloværdig generisk listegenerator til RKG!
#
# Hacket sammen af Troels Henriksen <athas@sigkill.dk> den 11. april
# 2010.

from __future__ import with_statement
import sys, os, re

if len(sys.argv) != 4:
    print "Requires exactly three parameters: paper size, column description file, and first column data"
    exit(os.EX_USAGE)

paper_size, desc_file, data_file = sys.argv[1:]

widths = []
headers = []

for line in open(desc_file, 'r'):
    match = re.match("^([^ ]*) (.*)$", line)
    widths.append("p{%s}" % match.group(1))
    headers.append(r"\vspace{0.2cm}" + match.group(2))

russes = []

for line in open(data_file):
    empties = "\\\\\\hline"
    for i in range(1,len(headers)):
        empties = "&" + empties
    russes.append(line + "\\vspace{0.2cm}" + empties)

russes.sort()

meat = r"""\begin{center}
\begin{longtable}{%(widths)s}\hline
%(headers)s\endhead
\hline
%(russes)s
\end{longtable}
\end{center}""" % {'papersize' : paper_size,
                   'widths': "|%s|" % ("|".join(widths)),
                   'headers': " & ".join(headers),
                   'russes': "\n".join(russes) }

title = os.path.basename(desc_file).rsplit('.',1)[0]
meat = (r'\begin{center}\textsc{%s}\end{center}' % title) + meat
if paper_size == "a3":
    meat = "\\begin{landscape}\n%s\\end{landscape}\n" % meat

print r"""\documentclass[11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{%(papersize)s,lscape}
\usepackage[danish]{babel}
\usepackage[T1]{fontenc}
\usepackage{longtable}
\usepackage[top=1cm, bottom=1cm, left=1cm, right=1cm]{geometry}
\pagestyle{empty}
\begin{document}
%(meat)s
\end{document}
""" % { 'papersize': paper_size, 'meat': meat }
