#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: et ts=4 sw=4

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
    a, b = str(f).split('.')
    return (hex(int(a)) + "." + hex(int(b)).lstrip("0x")).rstrip('.')

def load_file(filename):
    with codecs.open(filename, "r", "utf-8") as f:
        return "".join(f.readlines())

def gen_recipes(food, out_dir, num_people):
    tpl_recipes = load_file("tpl/recipes.tex")
    tpl_stub    = load_file("tpl/recipe_stub.tex")
    re_title = re.compile("##TITLE##", re.U | re.I)
    re_pers  = re.compile("##PERS##", re.U | re.I)
    re_text  = re.compile("##TEXT##", re.U | re.I)
    re_ingr  = re.compile("##INGREDIENTS##", re.U | re.I)
    i = 0
    includes = []
    for r in food.get_recipes(num_people):
        with codecs.open("{0}/{1}.tex".format(out_dir, i), "w", "utf-8") as f:
            str = re_title.sub(r['title'], tpl_stub)
            str = re_pers.sub(unicode(hex(r['people'])), str)
            # <hack>
            if (re.match(r'^\\', r['text'])):
                r['text'] = "\\" + r['text']
            # </hack>
            str = re_text.sub(r['text'], str)
            lines = []
            for ingr in r['ingredients']:
                lines.append(ur"{0} & {1} {2} \\\\".format(ingr['name'], float2hex(ingr['amount']), ingr['unit']))
            str = re_ingr.sub("\\hline\n".join(lines), str)
            f.write(str)
            includes.append("{0}".format(i))
            i = i + 1
    with codecs.open("{0}/recipes.tex".format(out_dir), "w", "utf-8") as f:
        str = re.sub(r"##INCLUDES##", "\n".join(map(lambda x: "\\include{" + x + "}", includes)), tpl_recipes)
        f.write(str)


def gen_shoppinglist(food, out_dir, num_people):
    tpl_list = load_file("tpl/shoppinglist.tex")
    tpl_cat  = load_file("tpl/shoppinglist_category.tex")
    re_name = re.compile("##NAME##", re.U | re.I)
    re_items = re.compile("##ITEMS##", re.U | re.I)
    i = 0
    includes = []
    for category, items in food.get_ingredients(num_people).iteritems():
        with codecs.open("{0}/{1}.tex".format(out_dir, i), "w", "utf-8") as f:
            lines = []
            for name, info in items.iteritems():
                lines.append(ur"{0} & {1} {2} \\\\".format(name, float2hex(info['amount']), info['unit']))
            str = re_items.sub("\\hline\n".join(lines), tpl_cat)
            str = re_name.sub(category, str)
            f.write(str)
            includes.append("{0}".format(i))
        i = i + 1
    with codecs.open("{0}/shoppinglist.tex".format(out_dir), "w", "utf-8") as f:
        str = re.sub(r"##INCLUDES##", "\n".join(map(lambda x: "\\include{" + x + "}", includes)), tpl_list)
        f.write(str)


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
        if opt == '-o':
            out_dir = arg
        elif opt == '-i':
            in_dir = arg
        elif opt == '-n':
            num_people = int(arg)
        elif opt == '-t':
            if arg in ('recipes', 'shoppinglist'):
                type = arg
            else:
                rtmf("invalid type: {0}".format(arg))
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
