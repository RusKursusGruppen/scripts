#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: et ts=4 sw=4

from __future__ import with_statement
from food import Food
from lib.tempita import Template
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

def open_file(filename, mode='r'):
    return codecs.open(filename, mode, 'utf-8')
def load_file(filename):
    return open_file(filename).read()
def load_template(filename):
    return Template(load_file(filename))


def build_generator(tpl_single_path, tpl_list_path):
    tpl_single = load_template(tpl_single_path)
    tpl_list   = load_template(tpl_list_path)
    def generator(out_dir, list):
        for i,items in enumerate(list):
            print items
            with open_file('%s/%i.tex' % (out_dir, i), mode='w') as f:
                f.write(tpl_single.substitute(**items))
        with open_file('%s/list.tex' % (out_dir), mode='w') as f:
            print "LENGTH", len(list)
            f.write(tpl_list.substitute(count=len(list)))
    return generator

def gen_recipes(food, out_dir, num_people):
    gen = build_generator('templates/recipe_stub.tex', 'templates/recipes.tex')
    recipes = food.get_recipes(num_people)
    gen(out_dir, recipes)

def gen_shoppinglist(food, out_dir, num_people):
    gen = build_generator('templates/shoppinglist_category.tex', 'templates/shoppinglist.tex')
    ingredients = food.get_ingredients(num_people)
    gen(out_dir, ingredients)


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
