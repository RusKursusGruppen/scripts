#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import codecs
import locale
locale.setlocale(locale.LC_ALL, "")

filename = sys.argv[1]

f = codecs.open(filename, 'r', 'utf-8')
i = 0

index = []

for line in f:
  obj = re.search(r'beginsong\{([^\}]+)\}.*?', line)

  if obj:
    s = obj.group(1)
    ss = s[0]
    
    # Vi har mærkelige sangnavne:
    if ss == "(":
      ss = s[1]

    elif re.search(r'\$\\lambda', s):
      ss = "L"
  
    ss = ss.capitalize()
    
    index.append((ss, s, "\\idxentry{" + s + "}{\\hyperlink{song1-" + str(i) + ".1}{" + str(i) + "}}"))
    i += 1
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

index.sort(lambda x, y: cmpStr(x, y), key=lambda s: (s[0], s[1].encode('utf-8').lower()))
alpha = ""
first = True

for pair in index:
  if alpha != pair[0]:
    alpha = pair[0]
    if not first:
        print ("\\end{idxblock}").encode('utf-8')
    print ("\\begin{idxblock}{" + alpha + "}").encode('utf-8')
    first = False

  print pair[2].encode('utf-8')
print ("\\end{idxblock}").encode('utf-8')