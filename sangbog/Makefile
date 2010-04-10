# The directory in which we put temporary files, nothing permanent
# should be stored here.
WORKDIR=./work
# Where we store songs after splitting (note that some scripts
# hardcode this directory)
SONGSDIR=./src
# Ancillary scripts and programs
BINDIR=./bin
# TeX bits and pieces that are used as the scaffold for the book.
TEXDIR=./tex
# The output directory for the finished results
OUTPUTDIR=./output

SONGSDIRTOKEN=$(SONGSDIR)up2date

# Ensure we have the necessary directories.
$(shell mkdir -p $(WORKDIR))
$(shell mkdir -p $(OUTPUTDIR))

all: $(OUTPUTDIR)/sangbog.ps $(OUTPUTDIR)/sangbogprint.pdf $(OUTPUTDIR)/nodebog.ps

clean:
	rm -f $(WORKDIR)/* $(OUTPUTDIR)/* $(SONGSDIR)/* $(SONGSDIRTOKEN)

$(SONGSDIRTOKEN): sangbog.chord
	# Split sangbog.chord into individual songs in src/
	$(BINDIR)/splitit.pl ./sangbog.chord
	touch $(SONGSDIRTOKEN)

$(WORKDIR)/list.txt: $(SONGSDIRTOKEN)
	# Create a list of the songs in the order in which they will
	# appear in the book.
	$(BINDIR)/mklist.sh | $(BINDIR)/sortsongs.py > $(WORKDIR)/list.txt

$(WORKDIR)/autosangbog.chord: $(WORKDIR)/list.txt
	# Create hyperlinks between the listed songs as defined by
	# their category, creating a new complete file of songs in
	# their proper order and with cross-references in
	# autosangbog.chord.
	$(BINDIR)/hyper.pl $(WORKDIR)/list.txt > $(WORKDIR)/autosangbog.chord

$(WORKDIR)/sangliste.tex: $(WORKDIR)/autosangbog.chord
	# Convert the generated song file to TeX format.
	$(BINDIR)/chord2tex.pl $(WORKDIR)/autosangbog.chord > $(WORKDIR)/sangliste.tex

$(WORKDIR)/index.tex: $(WORKDIR)/sangliste.tex
	$(BINDIR)/genindex.pl $(WORKDIR)/sangliste.tex > $(WORKDIR)/index.tex

$(WORKDIR)/sangbog.tex: $(WORKDIR)/index.tex $(WORKDIR)/sangliste.tex
	cat $(TEXDIR)/header.tex > $(WORKDIR)/sangbog.tex
	cat $(TEXDIR)/forside.tex >> $(WORKDIR)/sangbog.tex
	cat $(WORKDIR)/index.tex >> $(WORKDIR)/sangbog.tex
	cat $(WORKDIR)/sangliste.tex >> $(WORKDIR)/sangbog.tex
	cat $(TEXDIR)/bagside.tex >> $(WORKDIR)/sangbog.tex
	cat $(TEXDIR)/footer.tex >> $(WORKDIR)/sangbog.tex

$(WORKDIR)/sangbog.dvi: $(WORKDIR)/sangbog.tex
	$(BINDIR)/nicelatex.sh -output-directory=$(WORKDIR) $(WORKDIR)/sangbog.tex
	$(BINDIR)/nicelatex.sh -output-directory=$(WORKDIR) $(WORKDIR)/sangbog.tex
	$(BINDIR)/nicelatex.sh -output-directory=$(WORKDIR) $(WORKDIR)/sangbog.tex

$(WORKDIR)/tmp.ps: $(WORKDIR)/sangbog.dvi
	dvips -o $(WORKDIR)/tmp.ps $(WORKDIR)/sangbog.dvi

$(OUTPUTDIR)/sangbog.ps: $(WORKDIR)/tmp.ps
	cat $(WORKDIR)/tmp.ps | psresize -Pletter -PA4 | psbook | psnup -2 > $(OUTPUTDIR)/sangbog.ps

$(OUTPUTDIR)/sangbogprint.pdf: $(WORKDIR)/tmp.ps
	ps2pdf $(WORKDIR)/tmp.ps
	mv $(WORKDIR)/tmp.pdf $(OUTPUTDIR)/sangbogprint.pdf

$(OUTPUTDIR)/nodebog.ps: sangbog.chord
	chord/chord sangbog.chord > $(OUTPUTDIR)/nodebog.ps
