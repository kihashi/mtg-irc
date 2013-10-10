'''
mtgojson.py
A module to parse files from MTG JSON and add them to a card database.
http://www.mtgjson.com
Author: John Cleaver
License: BSD 3-Clause
'''

import json
from card_database import models


def parse_file(file):


def load_card(card_json):
    db_card = models.MagicCard()

    db_card.layout = card_json['layout']
    db_card.name = card_json['name']
    db_card.converted_mana_cost = card_json['cmc']

    if 'manaCost' in card_json:
        db_card.mana_cost = card_json['manaCost']

    if 'text' in card_json:
        db_card.rules_text = card_json['text']

    if 'power' in card_json:
        db_card.power = card_json['power']

    if 'toughness' in card_json:
        db_card.toughness = card_json['toughness']

    if 'loyalty' in card_json:
        db_card.loyalty = card_json['loyalty']

    if 'colors' in card_json:
        for card_color in card_json['colors']:
            db_color = models.Color.get_by(color=card_color)
            if not db_color:
                db_color = models.Color(color=card_color)
            db_card.colors.append(db_color)

    if 'supertypes' in card_json:
        for card_supertype in card_json['supertypes']:
            db_supertype = models.SuperType.get_by(supertype=card_supertype)
            if not db_supertype:
                db_supertype = models.SuperType(supertype=card_supertype)
            db_card.supertype.append(db_supertype)


def determine_alt_side(name, names):
