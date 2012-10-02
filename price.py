"""
prices.py - Phenny Magic: The Gathering Price Lookup Module
A module for the IRC Bot Phenny that allows a user to get the TCG Player
prices for cards.

Author: John Cleaver

License: All Rights Reserved.
         Because the TCG Player API is not openly available, this source
         code shall remain private. If it is to be released openly, the api
         information must be removed.
"""
import urllib
import xml.etree.ElementTree as ET
from collections import OrderedDict

partner_key = "TCGTEST"
secret_api_url = ""
tcg_player_url = secret_api_url + "pk=" + partner_key + "&s=" + "&p="


def price(phenny, input):
    card_dict = parse_tcg_player_xml(get_tcg_price(input.group(2)))
    output_string = input.nick + ": " + input.group(2)
    for key, val in card_dict.items():
        output_string += " | " + key + ": " + val

    phenny.say(output_string)

price.commands = ['price']
price.priority = 'medium'


def get_tcg_price(card_name):
    url = tcg_player_url + card_name
    xml_return = urllib.urlopen(url)

    return xml_return


def parse_tcg_player_xml(xml):
    tree = ET.parse(xml)
    root = tree.getroot()

    card = OrderedDict([('Hi', root[0][1].text),
                        ('Low', root[0][2].text),
                        ('Avg', root[0][3].text),
                        ('Link', root[0][4].text)])

    return card
