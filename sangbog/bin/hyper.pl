#!/usr/bin/env perl

###############################################################################
# hyper.pl
# --------
#
# Dette (desværre ikke specielt lille) script løber, givet på stdin en
# "playlist" i ./info.pl format, en masse sange igennem, finder ud af hvilke
# kategorier de definerer, opretter hyperlinks imellem sangene og udskriver en
# samlet multi-song chord-fil til stdout, der indeholder disse links som
# {c:Kommentarer}.
#
# Skrevet i forbindelse med en hel suite af små dumme scripts til brug for
# konstruktion af sangbog i rusturssammenhæng(TM).
#
# Slamkodet af: Uffe Friis Lichtenberg (uffefl@diku.dk)
#               DIKU, 2. juli 2000
###############################################################################

srand 42;

@songs = <>;

# Registrer alle kategorier (så kat:* virker)
foreach $song (@songs)
{
    chomp $song;
    $song =~ m/^.* ([^ ]+)$/ || die "Error in input (line ".($n+1).")";
    $file = $1;
    open(FIL,"<$file");
    foreach $line (<FIL>)
    {
	chomp $line;
	if ($line =~ m/^\#kat:([abcdefghijklmnopqrstuvwxyzæøå].*)$/)
	{
	    $kategorier{$1} = "A";
	}
    }
    close(FIL);
}

# Find og registrer de enkelte sanges kategorier
$n = 0;
foreach $song (@songs)
{
    chomp $song;
    $song =~ m/^.* ([^ ]+)$/ || die "Error in input (line ".($n+1).")";
    $file = $1;
    open(FIL,"<$file");
    foreach $line (<FIL>)
    {
	chomp $line;
	if ($line =~ m/^\#kat:(.*)$/)
	{
	    if ($1 eq "*")
	    {
		while (($kat,$what) = each %kategorier)
		{
		    $kategori{$kat} .= "$n ";
		}
	    }
	    else
	    {
		$kategori{$1} .= "$n ";
	    }
	}
    }
    close(FIL);
    $n++;
}

# Bland ruten godt og grundigt
while (($kat,$what) = each %kategori)
{
    $whatever = "";
    @what = split(" ",$what);
    $num = @what;
    while ($num)
    {
	$n = int(rand $num);
	$whatever .= "@what[$n] ";
	@what[$n] = @what[$num-1];
	$num--;
    }
    $kategori{$kat} = $whatever;
}

# Sørg for at ruten starter forfra
while (($kat,$what) = each %kategori)
{
    $what =~ s/^([^ ]+)(.*)$/ $1$2$1/;
    $kategori{$kat} = $what;
}

# Udskriv ruterne
$n = 0;
foreach $song (@songs)
{
    chomp $song;
    $song =~ m/^.* ([^ ]+)$/ || die "Error in input (line ".($n+1).")";
    $file = $1;
    $title = "";
    $author = "";
    $song = "";
    $klump = "";
    open(FIL,"<$file");
    foreach $line (<FIL>)
    {
	chomp $line;
	if ($line =~ s/(.*)\{t:([^}]*)\}(.*)/\1\{t:$n. \2\}\3/)
        {
	    $title = $2;
	    $title =~ s/^\s*//;
	    $title =~ s/\s*$//;
	}
        if ($line =~ m/.*\{st:Mel:\s*([^}]*)\}.*/)
        {
	    $author = $1;
	    $author =~ s/^\s*//;
	    $author =~ s/\s*$//;
	}
	if ($line =~ m/^\#kat:(.*)$/)
        {
	    $akt = $1;
	    if ($1 eq "*")
	    {
		while (($kat,$what) = each %kategorier)
		{
		    $what = $kategori{$kat};
		    $what =~ s/.*? $n ([^ ]+).*/\1/;
		   # $what++;
		    $klump .= "{c:En $kat-sang? Gå til $what}\n";
		}
	    }
	    else
	    {
		$what = $kategori{$akt};
		$what =~ s/.*? $n ([^ ]+).*/\1/;
		#$what++;
		$klump .= "{c:Endnu en $akt-sang? Gå til $what}\n";
	    }
	}
        else
        {
	    $song .= "$line\n";
	}
    }
    close(FIL);
    print $song . "\n" . $klump. "{ns}\n";
    $n++;
}
