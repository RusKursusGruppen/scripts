#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: et ts=4 sw=4

from glob import glob
import re
import codecs

class Food:
    def __init__(self):
        self.ingd_regex = re.compile(r"^(?P<cat>\w+?);(?P<name>\w+?);(?P<amount>[0-9.]+?) (?P<unit>\w*)$", re.U)
        self.categories = {
            "T": u"Tørvarer",
            "F": u"Frostvarer",
            "M": u"Mejeri",
            "D": u"Diverse"
        }
        self.recipes = []

    def parse_ingredient(self, line):
        ingd = self.ingd_regex.search(line).groupdict()
        ingd['amount'] = float(ingd['amount'])
        if (ingd['cat'] in self.categories.keys()):
            ingd['cat'] = self.categories[ingd['cat']]
        return ingd
    
    def load_dir(self, dir):
        pers_regex = re.compile(r"^([0-9]+)")
        
        for file in glob(dir + "/*"):
            parsed_ingredients = False
            lines_rest = []
            ingredients = []
            with codecs.open(file, 'r', 'utf-8') as f:
                i = 0
                for line in f:
                    line = line.strip()
                    if i == 0:
                        title = line
                    elif i == 1:
                        pers = int(pers_regex.search(line).group(1))
                    elif parsed_ingredients:
                        lines_rest.append(line)
                    else:
                        if (len(line) > 0):
                            ingredients.append(self.parse_ingredient(line))
                        else:
                            parsed_ingredients = True
                    i = i + 1
            self.recipes.append({'title':title, 'people':pers, 'ingredients':ingredients, 'text':"\n".join(lines_rest)})
    
    def get_recipes(self, num_people):
        ret = []
        for r in self.recipes:
            r['ingredients'] = map(lambda x: {'cat':x['cat'],'unit':x['unit'],'name':x['name'],'amount':x['amount'] / r['people'] * num_people}, r['ingredients'])
            r['people'] = num_people
            ret.append(r)
        return ret

    def get_ingredients(self, num_people):
        ret = {}
        for r in self.get_recipes(num_people):
            for i in r['ingredients']:
                if i['cat'] not in ret.keys():
                    ret[i['cat']] = {}
                if not i['name'] in ret[i['cat']].keys():
                    ret[i['cat']][i['name']] = {'amount':i['amount'], 'unit':i['unit']}
                else:
                    ret[i['cat']][i['name']]['amount'] += i['amount']
        return ret
