#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# sortsongs.py
# --------
#
# Dette script tager pÃ¥ stdin en "playlist" i ./info.pl format, og
# udspyr pÃ¥ stdout en sorteret rÃ¦kkefÃ¸lge der overholder (hardcodede)
# krav til nummering.
#
# Skrevet i forbindelse med en hel suite af smÃ¥ dumme scripts til brug for
# konstruktion af sangbog i rusturssammenhÃ¦ng(TM).
#
# Slamkodet af: Troels Henriksen (athas@sigkill.dk)
#               DIKU, 10. april 2000
#  (Som virkelig ikke kan Python)
###############################################################################

import sys
import re

songs = []
endlist = []

# IndlÃ¦s alle sange og put dem i songs-listen, lav samtidigt en tom
# plads i vores endelige liste.
for line in sys.stdin:
    match = re.match("^(.): (.*) ([^ \n]+)$", line)
    songs.append(match.groups())
    endlist.append(None)

# GÃ¥ nu sangene igennem og sÃ¦t de specielle tilfÃ¦lde pÃ¥ deres rette
# plads...

for song in songs:
    if (song[1] == "I Morgen Er Verden Vor (Tomorrow belongs to me - Cabaret)"):
        endlist[42] = song
        songs.remove(song)
    elif (song[1] == "DAT62(1/2)80 Slagsang (Fy Fy Skamme Skamme - McEwan og Ingerslev)"):
        endlist[43] = song
        songs.remove(song)

songs.sort()
songs.reverse()

for i in range(0, len(endlist)):
    if not endlist[i]:
        endlist[i] = songs.pop()

for song in endlist:
    print song[0] + ": " + song[1] + " " + song[2]
