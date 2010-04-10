#!/usr/local/bin/perl

use strict;
use warnings;

my $infile = $ARGV[0];

my $ignoreblank = 1;
my $lastlinespace = 1;
my $numsection = 0;

open( my $in, $infile )   or die "Couldn't read $infile: $!";

sub doit ($)
{
    my $line = shift(@_);
    # fjern noder
    $line =~ s/\[([^\]]*)\]//g;

    if ($line =~ m/^#.*$/) {
	# fjern chord-kommentarer og #kat
    } elsif ($line =~ m/^\{ns\}/){ # {ns}
	print "\\end\{multicols\}\n";
	print "\\vspace\{0.5cm\}\n";
	$ignoreblank = 1;
    } elsif ($line =~ m/^\{col([^}]*)\}/) { # {col*
    } elsif ($line =~ m/^\{define([^}]*)\}/) { # {define
    } elsif ($line =~ m/^\{c:([^}]*)\}/) { # {c:
        print "\\textbf\{$1\} \\\\ \n";
	$ignoreblank = 1;
    } elsif ($line =~ m/^\{soc\}/) { # {soc}
        print "\{\\it\n";
	$ignoreblank = 1;
    } elsif ($line =~ m/^\{eoc\}/) { # {eoc
        print "\}\n";
    } elsif ($line =~ m/^\{sot\}/) { # {sot}
        print "\\begin\{comment\}\n";
	$ignoreblank = 1;
    } elsif ($line =~ m/^\{eot\}/) { # {eot}
        print "\\end\{comment\}\n";
	$ignoreblank = 1;
    } elsif ($line =~ m/^\{t:([^}]*)\}/) { # {t:
	print "\\begin{center}\n";
        print "\\section\*\{$1\} \n";
	print STDERR "++$line\n";
	my $i;
	while($i = <$in>) { # {st:
	    last unless ($i =~ m/^\{st:([^}]*)\}/);
	    print "\\textbf\{$1\} \\\\ \n";
	}
	print "\\end{center}\n";
	print "\\begin\{multicols\}\{2\}\n";
	print "\\noindent\n";	
	$ignoreblank = 1;
	doit($i) if($i);
    } elsif ($line =~ m/^\s*$/i)
    {
	# blank linie, hvis efter \section, gør intet
	if ($ignoreblank == 0 && $lastlinespace == 0) 
	{
	    $line = "\\\\\n";
	    $lastlinespace = 1;
	} else {
	    $line = "";
	}
	if ($line !~ m/^[\s\n]*$/i)
	{
	    print $line;
	}
    } else {
	$ignoreblank = 0;
	$lastlinespace = 0;

	chomp $line;

	# tilføj \\\\ efter linjen
	$line =~ s/^(.*)$/$1 \\\\ \n/gs;

	# escape "&"
	$line =~ s/\&/\\\&/gs;

	# escape "'"
	#$line =~ s/'/\\'/gs;
	if ($line !~ m/^[\s\n]*$/i)
	{
	    print $line;
	}
    }
}

while ( <$in> ) {
    doit $_;
}
close $in;
