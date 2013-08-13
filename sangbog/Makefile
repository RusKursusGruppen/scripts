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
# Graphics and other resource files used
RESDIR=./res
# The output directory for the finished results
OUTPUTDIR=./output

SONGSDIRTOKEN=$(SONGSDIR)up2date

# Ensure we have the necessary directories.
$(shell mkdir -p $(WORKDIR))
$(shell mkdir -p $(OUTPUTDIR))

# $(OUTPUTDIR)/nodebog.ps
all: $(OUTPUTDIR)/sangbog.ps $(OUTPUTDIR)/sangbogprint.pdf

clean:
	rm -f $(WORKDIR)/* $(OUTPUTDIR)/* $(SONGSDIR)/* $(SONGSDIRTOKEN)

$(SONGSDIRTOKEN): sangbog.chord
	# Split sangbog.chord into individual songs in src/
	$(BINDIR)/splitit.py ./sangbog.chord
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

$(WORKDIR)/titleidx.sxd: $(WORKDIR)/sangliste.tex
	$(BINDIR)/nicelatex.sh --output-directory=$(WORKDIR) $(WORKDIR)/sangbog.tex

$(WORKDIR)/index.tex: $(WORKDIR)/titleidx.sxd
	$(BINDIR)/genindex.py $(WORKDIR)/titleidx.sxd > $(WORKDIR)/titleidx.sbx

$(WORKDIR)/sangbog.tex: $(WORKDIR)/sangliste.tex
	cat $(TEXDIR)/header.tex > $(WORKDIR)/sangbog.tex
	cat $(TEXDIR)/forside.tex >> $(WORKDIR)/sangbog.tex
	cat $(WORKDIR)/sangliste.tex >> $(WORKDIR)/sangbog.tex
	cat $(TEXDIR)/bagside.tex >> $(WORKDIR)/sangbog.tex
	cat $(TEXDIR)/footer.tex >> $(WORKDIR)/sangbog.tex
	cp $(TEXDIR)/songs.sty $(WORKDIR)/songs.sty

$(WORKDIR)/sangbog.dvi: $(WORKDIR)/sangbog.tex $(WORKDIR)/index.tex
	cp $(RESDIR)/* $(WORKDIR)/
	$(BINDIR)/nicelatex.sh -output-directory=$(WORKDIR) $(WORKDIR)/sangbog.tex
	$(BINDIR)/nicelatex.sh -output-directory=$(WORKDIR) $(WORKDIR)/sangbog.tex
	$(BINDIR)/nicelatex.sh -output-directory=$(WORKDIR) $(WORKDIR)/sangbog.tex

$(WORKDIR)/tmp.ps: $(WORKDIR)/sangbog.dvi
	dvips -o $(WORKDIR)/tmp.ps $(WORKDIR)/sangbog.dvi -Ppdf

$(OUTPUTDIR)/sangbog.ps: $(WORKDIR)/tmp.ps
	cat $(WORKDIR)/tmp.ps | psresize -Pletter -PA4 | psbook | psnup -2 > $(OUTPUTDIR)/sangbog.ps

$(OUTPUTDIR)/sangbogprint.pdf: $(WORKDIR)/tmp.ps
	ps2pdf $(WORKDIR)/tmp.ps $(OUTPUTDIR)/sangbogprint.pdf

#$(WORKDIR)/autosangbog-latin1.chord: $(WORKDIR)/autosangbog.chord
#	iconv -f UTF-8 -t latin1 $(WORKDIR)/autosangbog.chord > $(WORKDIR)/autosangbog-latin1.chord

#$(OUTPUTDIR)/nodebog.ps: $(WORKDIR)/autosangbog-latin1.chord
#	chord/chord $(WORKDIR)/autosangbog-latin1.chord > $(OUTPUTDIR)/nodebog.ps
