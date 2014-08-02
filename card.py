'''
card.py - Willie Magic: the Gathering Card Lookup Module
A module for the IRC Bot Willie that allows for one to get the Oracle text
for any Magic: the Gathering card by card name.

Author: John Cleaver
Site: https://github.com/kihashi/mtg-irc
License: BSD 3 Clause.
'''

from card_database import models
import sys
import argparse
import pprint


def find_card(input_card):
    '''
    Returns the card object that matches the input name.
    '''

    input_card = sanitize(input_card)
    models.setup()
    try:
        return find_card_by_name(input_card)
    except CardNotFoundError:
        try:
            return find_card_by_search_name(input_card)
        except CardNotFoundError:
            return find_cards_like(input_card)
    models.close()


def sanitize(input):
    '''
    Makes sure that the input string is clean.
    '''

    return unicode(input.strip())


def find_card_by_name(input_card):
    db_card = models.MagicCard.get_by(name=input_card)
    if not db_card:
        raise CardNotFoundError(input_card)
    else:
        return db_card


def find_card_by_search_name(input_card):
    db_card = models.MagicCard.get_by(search_name=
                                      input_card.lower()
                                      .replace("'", "")
                                      .replace(",", ""))
    if not db_card:
        raise CardNotFoundError(input_card)
    else:
        return db_card


def find_cards_like(input_card):
    # TODO: Implement this method.
    raise CardNotFoundError(input_card)


def find_expansion(exp_abbrev):
    q = models.Expansion.get_by(abbreviation=exp_abbrev)
    if not q:
        raise ExpansionNotFoundError(exp_abbrev)
    else:
        return q


def find_release_by_name(card_name, expansion_abbreviation):
    card = find_card(card_name)
    expansion = find_expansion(expansion_abbreviation)
    card_release = _find_release(card, expansion)
    return card_release


def _find_release(card, expansion):
    card_release = models.CardRelease.get_by(card=card,
                                             expansion=expansion)
    if card_release is not None:
        return card_release
    else:
        raise ReleaseNotFoundError(card, expansion)


class CardNotFoundError(Exception):
    def __init__(self, card_name):
        self.card_name = card_name

    def __str__(self):
        return self.card_name


class ExpansionNotFoundError(Exception):
    def __init__(self, exp_abbrev):
        self.expansion = exp_abbrev

    def __str__(self):
        return self.expansion


class ReleaseNotFoundError(Exception):
    def __init__(self, card, expansion):
        self.card = card
        self.expansion = expansion

    def __str__(self):
        return self.card.name + " is not in " + str(self.expansion)


def main(argv):
    if not argv.card:
        print("You must specify a card.")
        sys.exit()
    else:
        try:
            card_obj = find_card(" ".join(argv.card))
            if argv.text:
                print(card_obj.get_card_text())
            elif argv.rulings:
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(card_obj.get_rulings())
            elif argv.flavor:
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(card_obj.get_flavor_text())
            else:
                print(card_obj.get_card_text())
        except CardNotFoundError as e:
            print("Could not find the card: " + str(e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("card", nargs="+", help="The Card to find.")
    parser.add_argument("-r",
                        "--rulings",
                        action="store_true",
                        help="Get the rulings for the specified card.")
    parser.add_argument("-t",
                        "--text",
                        action="store_true",
                        help="Get the text for a specific card.")
    parser.add_argument("-f",
                        "--flavor",
                        action="store_true",
                        help="Get the flavor texts for a specific card")
    args = parser.parse_args()
    main(args)
