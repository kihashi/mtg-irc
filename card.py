'''
card.py - Willie Magic: the Gathering Card Lookup Module
A module for the IRC Bot Willie that allows for one to get the Oracle text
for any Magic: the Gathering card by card name.

Author: John Cleaver
Site: https://github.com/kihashi/mtg-irc
License: BSD 3 Clause.
'''

import card_database.models as models
import sys
import argparse


def find_card(input_card):
    '''
    Returns the card object that matches the input name.
    '''

    input_card = sanitize(input_card)
    models.setup()
    try:
        return find_card_by_name(input_card)
    except NameNotFoundError:
        try:
            return find_card_by_search_name(input_card)
        except SearchNameNotFoundError:
            return find_cards_like(input_card)
    models.close()


def sanitize(input):
    '''
    Makes sure that the input string is clean.
    '''

    return unicode(input)


def find_card_by_name(input_card):
    db_card = models.MagicCard.get_by(name=input_card)
    if not db_card:
        raise NameNotFoundError(input_card)
    else:
        return db_card


def find_card_by_search_name(input_card):
    db_card = models.MagicCard.get_by(search_name=
                                      input_card.lower()
                                      .replace("'", "")
                                      .replace(",", ""))
    if not db_card:
        raise SearchNameNotFoundError(input_card)
    else:
        return db_card


def find_cards_like(input_card):
    raise LikeCardsNotFoundError(input_card)


class CardNotFoundError(Exception):
    def __init__(self, card_name):
        self.card_name = card_name

    def __str__(self):
        return repr(self.card_name)


class NameNotFoundError(CardNotFoundError):
    pass


class SearchNameNotFoundError(CardNotFoundError):
    pass


class LikeCardsNotFoundError(CardNotFoundError):
    pass


def main(argv):
    if not argv.card:
        print "You must specify a card."
        sys.exit()
    else:
        try:
            print(find_card(" ".join(argv.card)).get_card_text())
        except CardNotFoundError as e:
            print("Could not find the card: " + str(e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("card", nargs="+", help="The Card to find.")
    args = parser.parse_args()
    main(args)
