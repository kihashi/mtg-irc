'''
card.py - Phenny Magic: the Gathering Card Lookup Module
A module for the IRC Bot Phenny that allows for one to get the Oracle text
for any Magic: the Gathering card by card name.

Author: John Cleaver
Site: https://github.com/kihashi/mtg-irc
License: BSD 3 Clause.
'''
from modules import nick
import re

def card(phenny, input):
    """Gets the text for a specified card."""
    if not input.group(2):
        phenny.say(input.nick + 'Perhaps you meant ".card Storm Crow"?')
    else:
        card_name = input.group(2)
        if card_name.lower().title() in nick.nicknames:
            card_name = nick.nicknames[input.group(2).lower().title()]
        card_text = get_card(card_name)
        if card_text:
            phenny.reply(card_text)
        else:
            phenny.reply("I could not find a card by that name.")
card.commands = ['card']
card.priority = 'medium'
card.example = '.card Storm Crow'


def get_card(card_name):
    found_card = False
    card_text = ''

    with open('modules/oracle.txt') as oracle_db:
        for line in oracle_db.readlines():
            if found_card:
                if line == "\n":
                    return card_text
                else:
                    card_text += " | " + line.strip("\n")
            else:
                if re.match(card_name + "\n", line, re.IGNORECASE):
                    found_card = True
                    card_text = line.strip("\n")

    return None
