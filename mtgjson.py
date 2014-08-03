'''
mtgojson.py
A module to parse files from MTG JSON and add them to a card database.
http://www.mtgjson.com
Author: John Cleaver
License: BSD 3-Clause
'''

import datetime
import json
import sys
import argparse
import card_database.models as models
from unidecode import *
import card as card_funcs


def parse_mtgojson(file_location, argv):
    with open(file_location, 'r') as json_file:
        file_json = json.loads(json_file.read())
    models.setup()
    if argv.set:
        _parse_set(file_json)
    else:
        _parse_file(file_json)
    models.close()


def _parse_file(file_json):
    for set_json in file_json:
        _parse_set(file_json[set_json])


def _parse_set(set_json):
    if "name" in set_json:
        db_expansion = models.Expansion.get_by(name=set_json['name'])
        if not db_expansion:
            db_expansion = models.Expansion(name=set_json['name'],
                                            abbreviation=set_json['code'])
            if 'oldCode' in set_json:
                db_expansion.old_code = set_json['oldCode']

            if 'gathererCode' in set_json:
                db_expansion.gatherer_code = set_json['gathererCode']

    for card in set_json['cards']:
        _parse_card(card, db_expansion)


def _parse_card(card_json, expansion):
    try:
        db_card = card_funcs.find_card_by_name(card_json['name'])
    except card_funcs.CardNotFoundError:
        db_card = models.MagicCard()

        db_card.name = card_json['name']
        #FIXME: This line breaks everything.
        db_card.search_name = unidecode(card_json['name'].lower().replace("'", "").replace(",", ""))

        if 'cmc' in card_json:
            db_card.converted_mana_cost = card_json['cmc']

        if 'manaCost' in card_json:
            db_card.mana_cost = card_json['manaCost']

        if 'text' in card_json:
            db_card.rules_text = card_json['text'].replace("\n", " ")

        if 'power' in card_json:
            db_card.power = card_json['power']

        if 'toughness' in card_json:
            db_card.toughness = card_json['toughness']

        if 'loyalty' in card_json:
            db_card.loyalty = card_json['loyalty']

        if 'layout' in card_json:
            db_layout = models.Layout.get_by(layout=card_json['layout'])
            if not db_layout:
                db_layout = models.Layout(layout=card_json['layout'])
            db_card.layout = db_layout

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
                db_card.supertypes.append(db_supertype)

        if 'types' in card_json:
            for card_type in card_json['types']:
                db_type = models.CardType.get_by(magictype=card_type)
                if not db_type:
                    db_type = models.CardType(magictype=card_type)
                db_card.card_types.append(db_type)

        if 'subtypes' in card_json:
            for card_subtype in card_json['subtypes']:
                db_subtype = models.SubType.get_by(subtype=card_subtype)
                if not db_subtype:
                    db_subtype = models.SubType(subtype=card_subtype)
                db_card.subtypes.append(db_subtype)

        if 'rulings' in card_json:
            for card_ruling in card_json['rulings']:
                models.Ruling(date=datetime.datetime.strptime(card_ruling['date'],
                              "%Y-%m-%d").date(),
                              text=card_ruling['text'],
                              card=db_card)
    finally:
        try:
            db_cardrelease = models.CardRelease()
            db_cardrelease.expansion = expansion
            db_cardrelease.card = db_card

            if 'rarity' in card_json:
                db_rarity = models.Rarity.get_by(rarity=card_json['rarity'])
                if not db_rarity:
                    db_rarity = models.Rarity(rarity=card_json['rarity'],
                                              abbreviation=card_json['rarity'][0])
                db_cardrelease.rarity = db_rarity

            if 'multiverseid' in card_json:
                db_cardrelease.multiverse_id = card_json['multiverseid']

            if 'flavor' in card_json:
                db_cardrelease.flavor_text = card_json['flavor']

            db_cardrelease.mtgoprice = models.MTGOPrice()

        except Exception as e:
            print e
            print card_json


def main(argv):
    if not argv.input_file:
        print "You must specify an input file to parse."
        sys.exit()
    else:
        parse_mtgojson(argv.input_file, argv)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file",
                        help="The MTG JSON File to be parsed")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s",
                       "--set",
                       action="store_true",
                       help="Set Mode. For parsing individual sets.")
    args = parser.parse_args()
    main(args)
