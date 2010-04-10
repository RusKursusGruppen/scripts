#!/usr/bin/python
import csv
import os
import sys

# Takes a filename of a .csv file and returns a list of lists.
def create_list(filename):
    reader = csv.reader(open(filename))

    thelist = []
    for row in reader:
        thelist.append(row)

    return thelist

# Returns a string representing a LaTeX table.
def create_table(list):
    return " \\\\ \n".join(map(" & ".join, list)) + " \\\\ \n"

def stregliste(names, header):
    postfix = " " + " ".join(map(lambda a: "&", header)) + " \\\\ \n"
    name_table = "".join(map(lambda str: str + postfix, names))
    beer_table = " & " + " & ".join(header) + " \\\\ \n"
    return beer_table + "\hline \n" + name_table


latex = """\\documentclass{{article}}
\\usepackage[table]{{xcolor}}
\\usepackage{{tabularx}}
\\usepackage{{rotating}}

\\topmargin -1.4in
\\oddsidemargin -0.9in
\\textwidth 6.9in
\\footskip 0.1in
\\textheight = 64\\baselineskip
\\advance\\textheight by \\topskip

\\begin{{document}}

\\pagestyle{{empty}}

\\rowcolors{{1}}{{white}}{{lightgray}}

\\begin{{sidewaystable}}
\\begin{{tabularx}}{{\\textwidth}}{{| l | X | X | X |}}

{table}

\\end{{tabularx}}
\\end{{sidewaystable}}
\\end{{document}}"""

def make_tex(names, header, out_file="out.tex"):
    name_list = map(lambda ls: ls[0], create_list(names))
    header_list = map(lambda ls: ls[0], create_list(header))
    sorted_name_list =  sorted(name_list)

    out = open(out_file, "w")
    out.writelines(latex.format(table = stregliste(sorted_name_list, header_list)))
    print("pdflatex " + out_file)
    os.system("pdflatex " + out_file)

make_tex(sys.argv[1], sys.argv[2])
