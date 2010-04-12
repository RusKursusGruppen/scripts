#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: et ts=4 sw=4

from __future__ import with_statement
from food import Food
from lib import tempita
import getopt, sys, codecs, re

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
    res = "0x%x." % int(abs(f))
    if f < 0:
    	res = "-" + res
    x = abs(f) - int(abs(f))
    while x > 0:
        x *= 16
        res += "%x" % x
        x -= int(x)
    return res.rstrip('.')

def load_file(filename):
    return codecs.open(filename, "r", "utf-8").read()
def load_template(filename):
    return tempita.Template(load_file(filename))

def gen_recipes(food, out_dir, num_people):
    tpl_recipes = load_template("templates/recipes.tex")
    tpl_stub    = load_template("templates/recipe_stub.tex")
    recipes = food.get_recipes(num_people)
    for i,r in enumerate(recipes):
        with codecs.open("%s/%i.tex" % (out_dir, i), "w", "utf-8") as f:
            lines = []
            for ingr in r['ingredients']:
                lines.append(ur"%s & %s %s \\" % (ingr['name'], float2hex(ingr['amount']), ingr['unit']))
            rendered = tpl_stub.substitute(title=r['title'], num_persons=r['people'],
                                           text=r['text'], ingredients='\hline\n'.join(lines))
            f.write(rendered)
    with codecs.open("%s/recipes.tex" % out_dir, "w", "utf-8") as f:
        txt = tpl_recipes.substitute(includes='\n'.join(map(lambda x: r'\include{%s}' % unicode(x), xrange(len(recipes)))))
        f.write(txt)


def gen_shoppinglist(food, out_dir, num_people):
    tpl_list = load_template("templates/shoppinglist.tex")
    tpl_cat  = load_template("templates/shoppinglist_category.tex")
    ingredients = tuple(food.get_ingredients(num_people).iteritems())
    for i, (category, items) in enumerate(ingredients):
        with codecs.open("%s/%i.tex" % (out_dir, i), "w", "utf-8") as f:
            lines = []
            for name, info in items.iteritems():
                lines.append(ur"%s & %s %s \\" % (name, info['amount'], info['unit']))
            rendered = tpl_cat.substitute(name=category, items='\\hline\n'.join(lines))
            f.write(rendered)
    with codecs.open("%s/shoppinglist.tex" % out_dir, "w", "utf-8") as f:
        txt = tpl_list.substitute(includes='\n'.join(
            map(lambda x: r'\include{%s}' % unicode(x), range(len(ingredients)-1))))
        f.write(txt)


GENERATORS = {'recipes' : gen_recipes, 'shoppinglist': gen_shoppinglist}
def main(args):
    # parse options
    try:
        opts, args = getopt.getopt(args, "ho:i:t:n:", ["help"])
    except getopt.GetoptError, err:
        rtfm(str(err))
    # set options
    out_dir = in_dir = None
    listtype = None
    num_people = None
    for opt, arg in opts:
        if opt == '-o':   out_dir = arg
        elif opt == '-i': in_dir  = arg
        elif opt == '-n': num_people = int(arg)
        elif opt == '-t':
            if arg not in ('recipes', 'shoppinglist'):
                rtmf("invalid type: %s" % arg)
            listtype = arg
        elif opt in ('-h', '--help'):
            usage()
            sys.exit()
    # not correctly filled
    if None in (out_dir,in_dir,listtype,num_people):
        rtfm("missing required options")
    # generate list
    food = Food()
    food.load_dir(in_dir)
    GENERATORS[listtype](food, out_dir, num_people)

if __name__ == '__main__':
    main(sys.argv[1:])
