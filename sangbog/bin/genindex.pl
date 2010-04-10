#!/usr/local/bin/perl

$filename = @ARGV;

@lines = <>;

#print "{t:Index}\n";
#print "{col:2}\n";

print "\n\\begin{center}\n\\section*{Index}\n\\end{center}\n";
print "\\begin{multicols}{2}\n\\noindent\n";

foreach $line (@lines)
{
    chomp $line;
    if ($line =~ m/\\[s]ection\*\{([^}]+)\}/)
    {
	print $1;
	print "\\\\\n";
    }
}

print "\\end{multicols}\n \n";
