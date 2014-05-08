'''
card.py - Willie Magic: the Gathering Card Lookup Module
A module for the IRC Bot Willie that allows for one to get the Oracle text
for any Magic: the Gathering card by card name.

Author: John Cleaver
Site: https://github.com/kihashi/mtg-irc
License: BSD 3 Clause.
'''

import willie
import willie.modules.card_database.models as models
import sys
import argparse


@willie.module.commands('card')
def card(bot, trigger):
    '''
    Returns the oracle text of the specified card as a reply to the user.

    Example:
    .card Storm Crow
    Storm Crow | {1}{U} | Creature  - Bird | Flying (This creature can't be blocked except by creatures with flying or reach.) | 1/2
    '''

    input = trigger.group(2)
    if not input:
        bot.reply("You must specify a card name when using this command.")
        return
    try:
        bot.say(find_card(input).get_card_text())
    except CardNotFoundError as e:
        bot.reply("I could not find a card by the name " + str(e))


def find_card(input_card):
    '''
    Returns the card object that matches the input name.
    '''

    input_card = sanitize(input_card)
    #First try an exact match
    db_card = models.MagicCard.get_by(name=input_card)
    if db_card:
        return db_card
    else:
        db_card = models.MagicCard.get_by(search_name=input_card.lower().replace("'", "").replace(",", ""))
        if db_card:
            return db_card
        else:
            raise CardNotFoundError(input_card)


def sanitize(input):
    '''
    Makes sure that the input string is clean.
    '''

    return unicode(input)


class CardNotFoundError(Exception):
    def __init__(self, card_name):
        self.card_name = card_name

    def __str__(self):
        return repr(self.card_name)


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
