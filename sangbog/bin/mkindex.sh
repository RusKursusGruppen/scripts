#/usr/local/bin/tcsh
echo \{t:Index\}
echo \{col:2\}
grep ^\{t: | perl -pi -e 's/^\{t:[0-9]+\. (.*)\}/$1/' | nl -w3 -v0 '-s. '
echo \{ns\}
echo \{t:Appendix\}
echo \{st:De umulige sange\}
