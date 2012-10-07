'''
card.py - Phenny Magic: the Gathering Card Lookup Module
A module for the IRC Bot Phenny that allows for one to get the Oracle text
for any Magic: the Gathering card by card name.

Author: John Cleaver
Site: https://github.com/kihashi/mtg-irc
License: BSD 3 Clause.
'''
import json
import urllib

json_url = "http://localhost:3000/card/"

def card(phenny, input):
    if not input.group(2):
        phenny.say(input.nick + 'Perhaps you meant ".card Storm Crow"?')
    else:
        card_json = get_card_json(input.group(2))
        if not card_json:
            phenny.say(input.nick + ": I could not find a card by that name.")
        else:
            phenny.say(input.nick + ": " + format_text(card_json))
card.commands = ['card']
card.priority = 'medium'

def rulings(phenny, input):
    if not input.group(2):
        phenny.say(input.nick + 'Perhaps you meant ".rulings Storm Crow"?')
    else:
        card_json = get_card_json(input.group(2))
        if not card_json:
            phenny.say(input.nick + ": I could not find a card by that name.")
        else:
            for ruling in format_rulings(card_json):
                phenny.msg(input.nick, ruling)
            else:
                phenny.msg(input.nick, "There are no rulings for that card.")
rulings.commands = ['rulings']
rulings.priority = 'medium'

def get_card_json(card):
    card_url = json_url + card

    card_json = urllib.urlopen(card_url)
    card_dict = json.load(card_json)

    if "error" in card_dict:
        return None
    else:
        return card_dict

def format_text(card_dict):
    output = card_dict['name'] + " | " + card_dict['mana_cost'] + " | "

    for card_type in card_dict['types']:
        output += card_type + " "

    output += "| " + card_dict['text']

    output = output.replace("\n", " ")

    return output

def format_rulings(card_dict):
    output = []
    for ruling in card_dict['rulings']:
        output.append(ruling[0] + ": " + ruling[1])

    return output
