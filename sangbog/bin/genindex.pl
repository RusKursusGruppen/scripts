#!/usr/bin/env perl

$filename = @ARGV;

@lines = <>;

#print "{t:Index}\n";
#print "{col:2}\n";

print "\n\\begin{center}\n\\section*{Index}\n\\end{center}\n";
print "\\begin{multicols}{2}\n\\noindent\n";

my $i = 0;
foreach $line (@lines)
{
    chomp $line;
    if ($line =~ m/\\beginsong{([^}]+)\}.*?/)
    {
	print $i . ". " . $1;
	$i += 1;
	print "\\\\\n";
    }
}

print "\\end{multicols}\n \n";
print "\\newpage";
