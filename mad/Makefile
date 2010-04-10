OUTDIR=out
INDIR=opskrifter
NUMPEOPLE=42

all: clean recipes shoppinglist

recipes:
	mkdir -p ${OUTDIR}/recipes
	./generate.py -i ${INDIR} -o ${OUTDIR}/recipes -t recipes -n ${NUMPEOPLE}
	(cd ${OUTDIR}/recipes; pdflatex recipes.tex && pdflatex recipes.tex && pdflatex recipes.tex)

shoppinglist:
	mkdir -p ${OUTDIR}/shoppinglist
	./generate.py -i ${INDIR} -o ${OUTDIR}/shoppinglist -t shoppinglist -n ${NUMPEOPLE}
	(cd ${OUTDIR}/shoppinglist; pdflatex shoppinglist.tex && pdflatex shoppinglist.tex && pdflatex shoppinglist.tex)

clean:
	find ${OUTDIR} -type f -exec rm -f {} \;
