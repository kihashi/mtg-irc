'''
card.py - Willie Magic: the Gathering Card Lookup Module
A module for the IRC Bot Willie that allows for one to get the Oracle text
for any Magic: the Gathering card by card name.

Author: John Cleaver
Site: https://github.com/kihashi/mtg-irc
License: BSD 3 Clause.
'''

import willie
import card_database as db


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
    input = sanitize(input)
    #First try an exact match
    db_card = db.models.MagicCard.get_by(name=input)
    if db_card:
        bot.reply(db_card.get_card_text)
    else:
        #Try to find cards that have a similar name
        #db_card = models.MagicCard.query.filter(models.MagicCard.name.like("%" + input + "%")).all()
        bot.reply("I could not find a card by that name.")


def sanitize(input):
    '''
    Makes sure that the input string is clean.
    '''

    return input
