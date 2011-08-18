#!/usr/bin/env perl

use strict;
use warnings;

my $infile = $ARGV[0];

open( my $in, $infile ) or die "Couldn't read $infile: $!";

my $line;
while($line = <$in>) {
    $line =~ s/æ\s+/\\ae\\ /gs;
    $line =~ s/Æ\s+/\\AE\\ /gs;
    $line =~ s/ø\s+/\\o\\ /gs;
    $line =~ s/Ø\s+/\\O\\ /gs;
    $line =~ s/å\s+/\\aa\\ /gs;
    $line =~ s/Å\s+/\\AA\\ /gs;
    $line =~ s/é\s+/\\'\{e\}\\ /gs;

    $line =~ s/æ/\\ae /gs;
    $line =~ s/Æ/\\AE /gs;
    $line =~ s/ø/\\o /gs;
    $line =~ s/Ø/\\O /gs;
    $line =~ s/å/\\aa /gs;
    $line =~ s/Å/\\AA /gs;

    $line =~ s/é/\\'\{e\}/gs;
    $line =~ s/ä/\\"\{a\}/gs;
    $line =~ s/ö/\\"\{o\}/gs;
        
    print $line;
}