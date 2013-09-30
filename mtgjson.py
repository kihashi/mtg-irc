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


def determine_alt_side(name, names):