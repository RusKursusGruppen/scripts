OUTDIR=out
INDIR=opskrifter
NUMPEOPLE=42

all: clean recipes shoppinglist

recipes:
	mkdir -p ${OUTDIR}/recipes
	./generate.py -i ${INDIR} -o ${OUTDIR}/recipes -t recipes -n ${NUMPEOPLE}
	(cd ${OUTDIR}/recipes; pdflatex list.tex && pdflatex list.tex && pdflatex list.tex && mv list.pdf recipelist.pdf)

shoppinglist:
	mkdir -p ${OUTDIR}/shoppinglist
	./generate.py -i ${INDIR} -o ${OUTDIR}/shoppinglist -t shoppinglist -n ${NUMPEOPLE}
	(cd ${OUTDIR}/shoppinglist; pdflatex list.tex && pdflatex list.tex && pdflatex list.tex && mv list.pdf shoppinglist.pdf)

clean:
	find ${OUTDIR} -type f -exec rm -f {} \;
