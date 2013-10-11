'''
mtgojson.py
A module to parse files from MTG JSON and add them to a card database.
http://www.mtgjson.com
Author: John Cleaver
License: BSD 3-Clause
'''

import datetime
import json
from card_database import models


def parse_file(file_json):
    for set_json in file_json:
        _parse_set(set_json)


def _parse_set(set_json):
    for card in set_json['cards']:
        _parse_card(card)


def _parse_card(card_json):
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

    if 'types' in card_json:
        for card_type in card_json['types']:
            db_type = models.CardType.get_by(cardtype=card_type)
            if not db_type:
                db_type = models.CardTye(cardtype=card_type)
            db_card.card_types.append(db_type)

    if 'subtypes' in card_json:
        for card_subtype in card_json['subtypes']:
            db_subtype = models.SubType.get_by(subtype=card_subtype)
            if not db_subtype:
                db_subtype = models.SubType(subtype=card_subtype)
            db_card.subtypes.append(db_subtype) 

    if 'rarity' in card_json:
        db_rarity = models.Rarity.get_by(rarity=card_json['rarity'])
        if not db_rarity:
            db_rarity = models.Rarity.(rarity=card_json['rarity'],
                                       abbreviation=card_json['rarity'][0])
        db_card.rarity = db_rarity

    if 'printings' in card_json:
        for printing in card_json['printings']:
            db_expansion = models.Expansion.get_by(expansion=printing)
            if not db_expansion:
                db_expansion = models.Expansion(expansion=printing)
            db_card.expansions.append(db_expansion)

    if 'rulings' in card_json:
        for ruling in card_json['rulings']:
            models.Ruling(date=datetime.datetime.strptime(ruling['date'], "%Y-%m-%d").date(),
                          text=ruling['text']
                          card=db_card)


def determine_alt_side(name, names):
