# if you are compiling under DOS, you may have to replace all the ".o" extension
# by ".obj"

# Paper size is now a runtime option !!!

# If your system does not have a getopt fonction, uncomment the next line
#GETOPT = getopt.o

# Use a ansi compiler
CC = cc 
CFLAGS = -g

# where to put the resulting program
BINDIR = /home/embla8/krogh/bin/hp9000s300

# where to put the man page
MANDIR = home/embla8/krogh/chords
MANEXT = l

# You should not have to change anything below this line

# name of the program
PROGRAMS = chord  a2crd

INCL = chord.h getopt.h patchlevel.h
SRC = common.c xpose.c iso.c chord.c grid.c getopt.c toc.c chord.man Makefile a2crd.c
OBJ = common.o xpose.o iso.o chord.o grid.o toc.o  ${GETOPT}
SONGS = songs/space-oddity songs/heaven songs/everybody-hurts
DOCS = README guide.ps license.txt a2crd.man a2crd.txt
RELNAME = chord362

all: $(PROGRAMS)

chord : $(OBJ) Makefile
	$(CC) $(CFLAGS) -o $@ $(OBJ)

a2crd: a2crd.o Makefile
	$(CC) $(CFLAGS) -o $@ a2crd.o common.o
	
chord.o    : chord.h
common.o   : chord.h
grid.o     : chord.h
xpose.o	   : chord.h
getopt.o   : getopt.h
toc.o	   : chord.h

install : all
	cp $(PROGRAMS) $(BINDIR)
	rm -f $(MANDIR)/cat$(MANEXT)/chord.$(MANEXT)
	cp chord.man $(MANDIR)/man$(MANEXT)/chord.$(MANEXT)
	chmod 666 $(MANDIR)/man$(MANEXT)/chord.$(MANEXT)
	cp a2crd.man $(MANDIR)/man$(MANEXT)/a2crd.$(MANEXT)
	chmod 666 $(MANDIR)/man$(MANEXT)/a2crd.$(MANEXT)
	
shar : $(SRC)
	rm -f $(RELNAME).part*
	shar -F -L 60 -o $(RELNAME).part $(SRC) $(INCL) $(SONGS) $(DOCS)

tar : $(SRC)
	tar cvf $(RELNAME).tar $(SRC) $(INCL) $(SONGS) $(DOCS)
	rm -f $(RELNAME).tar.Z
	compress -v $(RELNAME).tar

lint : $(SRC)
	lint $(SRC)

clean:
	rm -f core *.o chord 

floppy:
	cp $(SRC) $(DOCS) /floppy/floppy0
	rm /floppy/floppy0/Makefile
	eject floppy
