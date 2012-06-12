#!/usr/bin/env python
# coding: utf-8

''' Oprindelig beskrivelse af dette script (fra perl-versionen) '''
###############################################################################
# Dette lille script splitter en multi-song chord-fil op i mange sm<E5> chord-filer
# i et underkatalog der hedder src/. S<F8>rg for at kataloget eksisterer og er tomt
# f<F8>r du kalder dette script.
#
# Hvis der er eksotiske tegn blandt titler og/eller melodi angivelser i
# chord-sangene, s<E5> kan det kr<E6>ve lidt tilretning af sidste searchreplace linie
# hvor $filename konstrueres.
#
# Skrevet i forbindelse med en hel suite af sm<E5> dumme scripts til brug for
# konstruktion af sangbog i rusturssammenh<E6>ng(TM).
#
# Slamkodet af: Uffe Friis Lichtenberg (uffefl@diku.dk)
#               DIKU, 2. juli 2000
###############################################################################

from __future__ import with_statement
import sys, re, string

# where to output files
OUTDIR = 'src'

# precompiled regular expressions
RE_newsong = re.compile(r'\{\s*ns\s*\}')
RE_title   = re.compile(r'\{t:([^}]*)\}') # TODO: title can be empty?
RE_melody  = re.compile(r'\{st:(Mel:)?\s*([^}]+)\}') # TODO: ignore case?

# characters to use in file names
SAFE_CHARS = set(string.letters+string.digits+'_')

## before sanitizing file names (and stripping characters)
## perform following convertions
CONVERTIONS = ( ('æ', 'zae'), ('ø', 'zoe'), ('å', 'zzaa') )

def split_songs(data):
    ''' divide string into seperate songs '''
    return RE_newsong.split(data)

def get_info(song_data):
    ''' extract title and melody from song '''
    print song_data
    title = RE_title.search(song_data).group(1)
    match = RE_melody.search(song_data)
    melody = match and match.group(2) or ''
    return (title, melody)

def sanitize_filename(filename):
    ''' make a ascii-only readable filename '''
    filename = filename.lower()
    filename = reduce(lambda s,(fr,to): s.replace(fr,to), CONVERTIONS, filename)
    filename = re.sub(r'\s+', '_', filename)
    filename = ''.join(c for c in filename if c in SAFE_CHARS)
    return filename

def write_files(songs, infos, outdir):
    ''' write files in outdir - one for each song '''
    for (title, melody), data in zip(infos, songs):
        filename = sanitize_filename(
            title + (melody and ' - %s' % melody or ''))
        with open('%s/%s.chord' % (outdir, filename), 'w') as fd:
            fd.write(data.strip())

if __name__ == '__main__':
    data  = open(sys.argv[1]).read()
    songs = filter(lambda x: len(x.strip())>0, split_songs(data))
    infos = map(get_info, songs)
    write_files(songs, infos, OUTDIR)
