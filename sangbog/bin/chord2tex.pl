#!/usr/bin/env perl

use strict;
use warnings;

my $infile = $ARGV[0];

my $ignoreblank = 1;
my $lastlinespace = 1;
my $numsection = 0;

open( my $in, $infile ) or die "Couldn't read $infile: $!";

my $inChorus = 0;
my $inVerse = 0;

sub doit ($) {
  my $line = shift(@_);

  # fjern noder
  $line =~ s/\[([^\]]*)\]//g;

  if ($line =~ m/^#.*$/) {
    # fjern chord-kommentarer og #kat
  } elsif ($line =~ m/^\{ns\}/) {
    if ($inChorus) {
      print "\\endchorus\n";
      $inChorus = 0;
    }

    if ($inVerse) {
      print "\\endverse\n";
      $inVerse = 0;
    }

    print "\\endsong\n";
    $ignoreblank = 1;
  } elsif ($line =~ m/^\{col([^}]*)\}/) {
    # {col*
  } elsif ($line =~ m/^\{define([^}]*)\}/) {
    # {define
  } elsif ($line =~ m/^\{c:([^}]*)\}/) {
    # {c:

    print "\\noindent\\textbf\{$1\} \\\\ \n";
    $ignoreblank = 1;
  } elsif ($line =~ m/^\{soc\}/) {
    # {soc}

    if ($inVerse) {
      print "\\endverse\n";
      $inVerse = 0;
    }

    print "\\beginchorus \n";
    $inChorus = 1;
    $ignoreblank = 1;
  } elsif ($line =~ m/^\{eoc\}/) {
    # {eoc
    print "\\endchorus \n";
    $inChorus = 0;
  } elsif ($line =~ m/^\{sot\}/) {
    # {sot}
    $ignoreblank = 1;
  } elsif ($line =~ m/^\{eot\}/) {
    # {eot}
    $ignoreblank = 1;
  } elsif ($line =~ m/^\\\\/) {
    print "\\vspace*\{2mm\}\n";
  } elsif ($line =~ m/^\{t:(.*?)\}$/) {
    # {t:
    print STDERR "++$line\n";

    my $str;
    $str = "\\beginsong\{$1\}[";

    my $i;

    while($i = <$in>) {
      # {st:
      if ($i =~ m/^\{st:([^}]*)\}/) {
        next;
      } elsif($i =~ m/^\{[mM]el:([^}]*)\}/) {
        $str = $str . "sr=\{\\footnotesize Mel: $1\}, \n";
      } elsif ($i =~ m/^{[bB]y:(.*?)\}$/) {
        $str = $str . "by=\{\\footnotesize $1\}, \n"
      } elsif ($i =~ m/^{[iI]title:(.*?)\}$/) {
        $str = $str . "ititle=\{$1\}, \n"
      } else {
        last;
      }
    }

    $str = $str . "cr=\{\}] \n";
    $str =~ s/\&/\\\&/gs;
    print $str;

    $ignoreblank = 1;

    doit($i) if($i);

  } elsif ($line =~ m/^\s*$/i) {
    # blank linie, hvis efter \section, gÃ¸r intet
    if ($ignoreblank == 0 && $lastlinespace == 0) {
      $line = "\n";
      $lastlinespace = 1;
    } else {
      $line = "";
    }

    if ($inVerse) {
      print "\\endverse\n\n";
      $inVerse = 0;
    }

    if ($line !~ m/^[\s\n]*$/i) {
      print $line;
    }
  } else {
    if ($inVerse == 0 && $inChorus != 1) {
      print "\\beginverse\n";
      $inVerse = 1;
    }

    $ignoreblank = 0;
    $lastlinespace = 0;

    chomp $line;

    # tilføk \\\\ efter linjen
    $line =~ s/^(.*)$/$1 \n/gs;

    # escape "&"
    $line =~ s/\&/\\\&/gs;

    if ($line !~ m/^[\s\n]*$/i) {
      print $line;
    }
  }
}

print "\\begin\{songs\}\{titleidx\}\n";
print "\\setcounter\{songnum\}\{0\}\n";

while ( <$in> ) {
  doit $_;
}

close $in;
