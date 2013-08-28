'''
eprice.py

A module for the Phenny IRC bot that allows users to get prices of digital
versions of Magic The Gathering Cards.

Author: John Cleaver
License: BSD 3 Clause
'''

from modules import mtgotraders as mtgo
import datetime
card_dict = {}
last_time_fetched = None


def eprice(phenny, input):
    """Gets the MTGO Price for a specified card."""
    if not is_valid(input.group(2)):
        phenny.reply("Perhaps you mean '.eprice Grizzly Bears'")
    else:
        card_name = clean_input(input.group(2))
        if (datetime.datetime.today()-last_time_fetched).days >= 1:
            get_card_list()

        output = ""
        if card_name.lower() in card_dict:
            card = card_dict[card_name.lower()]
            output += card_name
            for edition in card:
                if 'reg_price' in card[edition]:
                    output += " | " + edition + ": " + card[edition]['reg_price']

            if 'link' in card[edition]:
                output += " | " + card.values()[0]['link'][:-5]

            phenny.reply(output)
        else:
            phenny.reply("I don't recognize that card.")
eprice.commands = ['eprice', 'mtgoprice', 'pricemtgo']
eprice.priority = 'medium'


def is_valid(card_name):
    if card_name == "":
        return False
    else:
        return True


def clean_input(card_name):
    return card_name.lower().title()


def get_card_list():
    global card_dict
    global last_time_fetched
    card_dict = mtgo.parse_list(mtgo.get_raw_list())
    last_time_fetched = datetime.datetime.today()

get_card_list()
