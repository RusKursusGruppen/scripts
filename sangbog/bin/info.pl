#!/usr/bin/env perl

###############################################################################
# info.pl
# -------
#
# Dette lille script åbner og gennemlæser en single-song chord-fil og udskriver
# en enkelt linie til stdout med en beskrivelse af sangen i filen.
#
# Skrevet i forbindelse med en hel suite af små dumme scripts til brug for
# konstruktion af sangbog i rusturssammenhæng(TM).
#
# Slamkodet af: Uffe Friis Lichtenberg (uffefl@diku.dk)
#               DIKU, 2. juli 2000
###############################################################################

$filename = @ARGV;

@lines = <>;

$song = "";
$title = "";
$author = "";
foreach $line (@lines)
{
    if ($line =~ m/^\#kat:(.*)$/)
    {
	$kategori{$1} = 1;
    }
    if ($line =~ m/.*\{t:([^}]*)\}.*/)
    {
	$title = $1;
	$title =~ s/^\s*//;
	$title =~ s/\s*$//;
    }
    if ($line =~ m/.*\{st:Mel:\s*([^}]*)\}.*/)
    {
        $author = $1;
	$author =~ s/^\s*//;
	$author =~ s/\s*$//;
    }
    if ($line =~ m/.*\{\s*ns\s*\}.*/)
    {
       print "Error: {ns} found\n";
    }
    else
    {
        $song = $song . $line;
    }
}

if ($kategori{"umulig"} eq 1)
{
    print "X: ";
}
else
{
    print "A: ";
}

print "$title";
print " ($author)" if (!($author eq ""));
print " $ARGV\n";
