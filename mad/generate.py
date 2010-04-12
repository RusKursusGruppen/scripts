#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: et ts=4 sw=4

from __future__ import with_statement
from food import Food
import getopt
import sys
import codecs
import re

def usage():
    print """Usage:
{0} -h
{0} -o output_dir -i input_dir -t type -n num_people

Valid types:
  recipes
  shoppinglist""".format(sys.argv[0])

def rtfm(msg):
    print msg
    usage()
    sys.exit(2)

def float2hex(f):
    res = "0x%x." % abs(f)
    if f < 0:
    	res = "-" + res
    x = abs(f) - int(abs(f))
    while x > 0:
        x *= 16
        res += "%x" % x
        x -= int(x)
    return res.rstrip('.')

def load_file(filename):
    with codecs.open(filename, "r", "utf-8") as f:
        return f.read()

def gen_recipes(food, out_dir, num_people):
    tpl_recipes = load_file("tpl/recipes.tex")
    tpl_stub    = load_file("tpl/recipe_stub.tex")
    re_title = re.compile("##TITLE##", re.U | re.I)
    re_pers  = re.compile("##PERS##", re.U | re.I)
    re_text  = re.compile("##TEXT##", re.U | re.I)
    re_ingr  = re.compile("##INGREDIENTS##", re.U | re.I)
    i = 0
    for r in food.get_recipes(num_people):
        with codecs.open("%s/%i.tex" % (out_dir, i), "w", "utf-8") as f:
            txt = re_title.sub(r['title'], tpl_stub)
            txt = re_pers.sub(unicode(hex(r['people'])), txt)
            # <hack>
            if (re.match(r'^\\', r['text'])):
                r['text'] = "\\" + r['text']
            # </hack>
            txt = re_text.sub(r['text'], txt)
            lines = []
            for ingr in r['ingredients']:
                lines.append(ur"%s & %s %s \\\\" % (ingr['name'], float2hex(ingr['amount']), ingr['unit']))
            txt = re_ingr.sub("\\hline\n".join(lines), txt)
            f.write(txt)
            i = i + 1
    with codecs.open("%s/recipes.tex" % out_dir, "w", "utf-8") as f:
        txt = re.sub(r"##INCLUDES##", "\n".join(map(lambda x: "\\include{" + unicode(x) + "}", range(i))), tpl_recipes)
        f.write(txt)


def gen_shoppinglist(food, out_dir, num_people):
    tpl_list = load_file("tpl/shoppinglist.tex")
    tpl_cat  = load_file("tpl/shoppinglist_category.tex")
    re_name = re.compile("##NAME##", re.U | re.I)
    re_items = re.compile("##ITEMS##", re.U | re.I)
    i = 0
    for category, items in food.get_ingredients(num_people).iteritems():
        with codecs.open("%s/%i.tex" % (out_dir, i), "w", "utf-8") as f:
            lines = []
            for name, info in items.iteritems():
                lines.append(ur"%s & %s %s \\\\" % (name, float2hex(info['amount']), info['unit']))
            txt = re_items.sub("\\hline\n".join(lines), tpl_cat)
            txt = re_name.sub(category, txt)
            f.write(txt)
        i = i + 1
    with codecs.open("%s/shoppinglist.tex" % out_dir, "w", "utf-8") as f:
        txt = re.sub(r"##INCLUDES##", "\n".join(map(lambda x: "\\include{" + unicode(x) + "}", range(i - 1))), tpl_list)
        f.write(txt)


def main(args):
    try:
        opts, args = getopt.getopt(args, "ho:i:t:n:", ["help"])
    except getopt.GetoptError, err:
        rtfm(str(err))
    out_dir = None
    in_dir = None
    type = None
    num_people = None
    for opt, arg in opts:
        if opt == '-o':   out_dir = arg
        elif opt == '-i': in_dir  = arg
        elif opt == '-n': num_people = int(arg)
        elif opt == '-t':
            if arg not in ('recipes', 'shoppinglist'):
                rtmf("invalid type: %s" % arg)
            type = arg
        elif opt in ('-h', '--help'):
            usage()
            sys.exit()
    if out_dir == None or in_dir == None or type == None or num_people == None:
        rtfm("missing required options")
    food = Food()
    food.load_dir(in_dir)
    if type == 'recipes':
        gen_recipes(food, out_dir, num_people)
    elif type == 'shoppinglist':
        gen_shoppinglist(food, out_dir, num_people)

if __name__ == '__main__':
    main(sys.argv[1:])
