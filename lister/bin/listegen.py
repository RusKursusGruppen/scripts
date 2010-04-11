#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Gloværdig generisk listegenerator til RKG!
#
# Hacket sammen af Troels Henriksen <athas@sigkill.dk> den 11. april
# 2010.

from __future__ import with_statement

import sys
import os
import re

if len(sys.argv) != 4:
    print "Requires exactly three parameters: paper size, column description file, and first column data"
    exit(os.EX_USAGE)

widths = []
headers = []

with open(sys.argv[2], 'r') as f:
    for line in f:
        match = re.match("^([^ ]*) (.*)$", line)
        widths.append("p{" + match.group(1) + "}")
        headers.append("\\vspace{0.2cm}" + match.group(2))

russes = []

with open(sys.argv[3], 'r') as f:
    for line in f:
        empties = "\\\\\\hline"
        for i in range(1,len(headers)):
            empties = "&" + empties
        russes.append(line + "\\vspace{0.2cm}" + empties)

print """\\documentclass[11pt]{article}
\\usepackage[utf8]{inputenc}
\\usepackage{%(papersize)s,lscape}
\\usepackage[danish]{babel}
\\usepackage[T1]{fontenc}
\\usepackage{longtable}
\\usepackage[top=1cm, bottom=1cm, left=1cm, right=1cm]{geometry}
\\pagestyle{empty}
\\begin{document}
\\begin{landscape}
\\begin{center}
\\begin{longtable}{%(widths)s}\\hline
%(headers)s\\endhead
\\hline
%(russes)s
\\end{longtable}
\\end{center}
\\end{landscape}
\\end{document}
""" % {'papersize' : sys.argv[1],
       'widths': "|" + "|".join(widths) + "|",
       'headers': " & ".join(headers),
       'russes': "\n".join(russes) }
