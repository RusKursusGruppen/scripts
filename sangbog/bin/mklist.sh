#!/bin/sh

###############################################################################
# mklist.sh
# ---------
#
# Dette lille script gennemsøger en masse enkelte single-song chord-filer i
# underkataloget src/ og laver en simpel "playlist" ved at kalde ./info.pl på
# hver af dem.
#
# Skrevet i forbindelse med en hel suite af små dumme scripts til brug for
# konstruktion af sangbog i rusturssammenhæng(TM).
#
###############################################################################

for file in src/*; do
	bin/info.pl "$file"
done
