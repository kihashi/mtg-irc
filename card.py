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

api_server = "http://ec2-107-21-148-64.compute-1.amazonaws.com:3000/"
json_url = api_server + "card/"
language_url = api_server + "language/"

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
rulings.commands = ['rulings']
rulings.priority = 'medium'

def sets(phenny, input):
    if not input.group(2):
        phenny.say(input.nick + 'Perhaps you meant ".set Storm Crow"?')
    else:
        card_json = get_card_json(input.group(2))
        if not card_json:
            phenny.say(input.nick + ": I could not find a card by that name.")
        else:
            phenny.say(input.nick + ": " + format_sets(card_json))
sets.commands = ['sets']
sets.priority = 'medium'

def image(phenny, input):
    if not input.group(2):
        phenny.say(input.nick + 'Perhaps you meant ".image Storm Crow"?')
    else:
        card_json = get_card_json(input.group(2))
        if not card_json:
            phenny.say(input.nick + ": I could not find a card by that name.")
        else:
            phenny.say(input.nick + ": " + format_image(card_json))
image.commands = ['image']
image.priority = 'medium'

def flavor(phenny, input):
    if not input.group(2):
        phenny.say(input.nick + 'Perhaps you meant ".image Storm Crow"?')
    else:
        card_json = get_card_json(input.group(2))
        if not card_json:
            phenny.say(input.nick + ": I could not find a card by that name.")
        else:
            for flavor_text in format_flavor_text(card_json):
                phenny.msg(input.nick, flavor_text)
flavor.commands = ['flavor']
flavor.priority = 'medium'

def get_card_json(card):
    card_url = json_url + card

    card_json = urllib.urlopen(card_url)
    card_dict = json.load(card_json)

    if "error" in card_dict:
        return None
    else:
        return card_dict

def get_language_json(card):
    card_url = language_url + card

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

    if card_dict['subtypes'] != []:
        output += " - "
        for subtype in card_dict['subtypes']:
            output += subtype + " "

    output += "| " + card_dict['text']

    if "power" in card_dict:
        output += " | " + str(card_dict['power']) + "/" + str(card_dict['toughness'])

    if "loyalty" in card_dict:
        output += " | " + str(card_dict['loyalty'])

    output = output.replace("\n", " ")

    return output

def format_rulings(card_dict):
    output = []
    if card_dict['rulings'] == []:
        output.append("There are no rulings for that card.")
    else:
        for ruling in card_dict['rulings']:
            output.append(ruling[0] + ": " + ruling[1])

    return output

def format_sets(card_dict):
    output = ''
    for version in card_dict['versions']:
        output += card_dict['versions'][version]['expansion'] + " - " + card_dict['versions'][version]['rarity'] + " | "

    return output

def format_image(card_dict):
    return card_dict['image_url']

def format_flavor_text(card_dict):
    output = []
    for version in card_dict['versions']:
        version_card_dict = get_card_json(version)
        output.append(version_card_dict['expansion'] + " - " + version_card_dict['flavor_text'])

    return output
