'''
init_db.py
A module to set up sets, colors, rarities, and other objects in the database.
Author: John Cleaver <cleaver.john.k@gmail.com>
License: BSD 3-Clause
'''

import models
from expansion import *


def create_colors():
    for c in [(u"White", u"W"),
              (u"Blue", u"U"),
              (u"Black", u"B"),
              (u"Red", u"R"),
              (u"Green", u"G")]:
        models.Color(color=c[0], abbreviation=c[1])


def create_rarities():
    for r in [(u"Common", u"C"),
              (u"Uncommon", u"U"),
              (u"Rare", u"R"),
              (u"Mythic Rare", u"M"),
              (u"Time Spiral: Special")]:
        models.Rarity(rarity=r[0], abbreviation=r[1])


def create_expansions():
    for e, a in sets.iteritems():
        models.Expansion(expansion=e, abbreviation=a)


def create_layouts():
    for l in [(u"normal", u"nml"),
              (u"split", u"spl"),
              (u"flip", u"flp"),
              (u"double-faced", u"dbl"),
              (u"token", u"tkn")]:
        models.Layout(layout=l[0], abbreviation=l[1])


def main():
    models.setup()
    create_colors()
    create_rarities()
    create_expansions()
    create_layouts()
    models.close()

if __name__ == '__main__':
    main()
