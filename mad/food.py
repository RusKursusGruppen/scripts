#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: et ts=4 sw=4

from __future__ import with_statement
from glob import glob
import re
import codecs

class Food:
    re_pers = re.compile(r'^([0-9]+)')
    re_ingr = re.compile(r'^(?P<cat>\w+?);(?P<name>\w+?);(?P<amount>[0-9.]+?) (?P<unit>\w*)$', re.U | re.M)
    re_inst = re.compile(r'^([^:\n]+)(:.*)?$', re.U | re.M)
    categories = {
        "T": u"Tørvarer",
        "F": u"Frostvarer",
        "M": u"Mejeri",
        "D": u"Diverse"
    }

    def __init__(self):
        self.recipes = []

    def parse_ingredient(self, match):
        ingd = match.groupdict()
        ingd['amount'] = float(ingd['amount'])
        ingd['cat'] = self.categories.get(ingd['cat'], ingd['cat'])
        return ingd

    def load_dir(self, dir):
        for path in glob(dir + "/*"):
            title = pers = None
            ingredients  = None
            instructions = []
            with codecs.open(path, 'r', 'utf-8') as f:
                # first line is title
                title = f.readline().strip()
                # second is number of persons
                pers  = int(Food.re_pers.search(f.readline()).group(1))
                # read rest of file
                rest = ''
                read = f.read()
                while len(read) > 0:
                    rest += read
                    read = f.read()
                # next is ingredient list
                ingr = tuple(self.re_ingr.finditer(rest))
                ingredients = map(self.parse_ingredient, ingr)
                # then instructions
                instructions = Food.re_inst.findall(rest[ingr[-1].end():])
                print instructions
            self.recipes.append({'title':title, 'people':pers,
                                 'ingredients':ingredients, 'instructions':instructions})

    def get_recipes(self, num_people):
        ret = []
        for r in self.recipes:
            # scale amount in each recipe (lambda function returns x) - TODO: more readable?
            r['ingredients'] = map(lambda x: (x.update(amount=x['amount'] / r['people'] * num_people),x)[1],
                                   r['ingredients'])
            r['people'] = num_people
            ret.append(r)
        return ret

    def get_ingredients(self, num_people):
        ingredients = map(lambda r: r['ingredients'], self.get_recipes(num_people))
        all_as_list = reduce(lambda l,m: l+m, ingredients)
        summed = {}
        for i in all_as_list:
            # unpack
            cat, name, amount, unit = i['cat'], i['name'], i['amount'], i['unit']
            # initialize if needed
            summed[cat]       = summed.get(cat,{})
            summed[cat][name] = summed[cat].get(name, {})
            # update
            item = summed[cat][name]
            item['unit']   = unit
            item['amount'] = item.get('amount',0) + amount
        # return as list of categories
        return [ {'category':category,'items':items} for category,items in summed.items() ]
