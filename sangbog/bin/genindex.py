#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import codecs
import locale
locale.setlocale(locale.LC_ALL, "")

filename = sys.argv[1]

f = codecs.open(filename, 'r', 'utf-8')
f.readline() # første linie er junk

song_array = []

while True:
  line1 = f.readline().strip() # sang titel
  line2 = f.readline().strip() # sang nummer
  line3 = f.readline().strip() # sang hyperlink

  if not line1:
    break

  # songs.sty generere nogle underlige æøå'er
  line1 = line1.replace("\IeC {\o }", u'ø').replace("\IeC {\O }", u'Ø').replace("\IeC {\\ae }", u'æ').replace("\IeC {\\r a}", u'å').replace("\IeC {\\'e}", u'é')

  # lille hax for at få \TeX til at virke
  line1 = line1.replace("T\kern -.1667em\lower .5ex\hbox {E}\kern -.125emX\spacefactor \@m ", "\TeX")

  index = line1[0]

  # Vi har mærkelige sangnavne
  if index == "(":
    index = line1[1]
  elif re.search(r'^\{\\TeX\}', line1):
    index = "T"
  elif re.search(r'\$\\lambda', line1):
    index = "L"

  index = index.capitalize()

  song_array.append((index, line1, "\\idxentry{" + line1 + "}{\\hyperlink{" + line3 + "}{" + line2 + "}}"))

f.close()

# Dette er hvad der sker, når man smider unicode med ind
def cmpStr(x, y):
  if locale.strcoll(x[0], y[0]) == 0:
    a = x[1]
    b = y[1]
    # Python tror at alfabetet hedder åæø og ikke æøå
    a = a.replace('æ', 'zae').replace('ø', 'zoe').replace('å', 'zzaa').replace('-', '')
    b = b.replace('æ', 'zae').replace('ø', 'zoe').replace('å', 'zzaa').replace('-', '')

    if a[0] == "(":
      a = a[1:]

    if b[0] == "(":
      b = b[1:]

    return locale.strcoll(a, b)
  else:
    return locale.strcoll(x[0], y[0])

song_array.sort(lambda x, y: cmpStr(x, y), key=lambda s: (s[0], s[1].encode('utf-8').lower()))
alpha = ""
first = True

for pair in song_array:
  if alpha != pair[0]:
    alpha = pair[0]
    if not first:
        print ("\\end{idxblock}").encode('utf-8')
    print ("\\begin{idxblock}{" + alpha + "}").encode('utf-8')
    first = False

  print pair[2].encode('utf-8')
print ("\\end{idxblock}").encode('utf-8')
