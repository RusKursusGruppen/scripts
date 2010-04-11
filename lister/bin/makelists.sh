#!/bin/sh

# Fail on error
set -e

BINDIR=bin
WORKDIR=work
OUTPUTDIR=output
COLUMNDIR=lister
RUSFILE=russer
LIBDIR=lib

mkdir -p $WORKDIR
mkdir -p $OUTPUTDIR

TABLEDATA=$(ls $COLUMNDIR/*.a3 $COLUMNDIR/*.a4)
#TABLETEX=$(echo $TABLEDATA | sed 's/ /.tex /g' | sed s/$COLUMNDIR/$WORKDIR/g)
#TABLERESULTS=$(echo $TABLEDATA | sed 's/ /.pdf /g' | sed s/$COLUMNDIR/$OUTPUTDIR/g)

cp $LIBDIR/a3.sty $WORKDIR/

for file in $TABLEDATA; do
    OUTPUTFILE=$(echo $file | sed 's/a[34]/tex/g' | sed s/$COLUMNDIR/$WORKDIR/)
    if [ $(echo $file | grep a3) ]
    then
        $BINDIR/listegen.py a3 "$file" "$RUSFILE" > $OUTPUTFILE
    else
        $BINDIR/listegen.py a4 "$file" "$RUSFILE" > $OUTPUTFILE
    fi
    pdflatex -output-directory=$WORKDIR $OUTPUTFILE
    PDFFILE=$(echo $OUTPUTFILE | sed 's/tex/pdf/')
    cp $PDFFILE $OUTPUTDIR/
done
