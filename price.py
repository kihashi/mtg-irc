"""
prices.py - Willie Magic: The Gathering Price Lookup Module
A module for the IRC Bot Willie that allows a user to get the TCG Player
prices for cards.

Author: John Cleaver

License: BSD 3 Clause
"""
import urllib
import xml.etree.ElementTree as ET
from collections import OrderedDict
import string
import willie

partner_key = "MTGIRC" #This is the partner code assigned with you TCGPlayer API account.
secret_api_url = "" #This is the URL that the TCGPlayer Rep assigns you for API access.
tcg_player_url = secret_api_url + "pk=" + partner_key + "&s=" + "&p="


@willie.modules.commands('price')
def price(bot, trigger):
    """Gets the TCG Player Prices for a specified card."""
    card_dict = parse_tcg_player_xml(get_tcg_price(trigger.group(2)))
    if not card_dict:
        bot.say(trigger.nick + ": I don't recognize that card name.")
        return
    output_price = ""
    for key, val in card_dict.items():
        output_price += " | " + key + ": " + val

    bot.reply(string.capwords(trigger.group(2)) + output_price)


def get_tcg_price(card_name):
    """ Makes the API call and returns the resultsing XML. """
    url = tcg_player_url + card_name
    xml_return = urllib.urlopen(url)

    return xml_return


def parse_tcg_player_xml(xml):
    """ Converts the XML response from the API into an ordered dict. """
    tree = ET.parse(xml)
    root = tree.getroot()

    if not root:
        return None

    card = OrderedDict([('Hi', root[0][1].text),
                        ('Low', root[0][2].text),
                        ('Avg', root[0][3].text),
                        ('Link', root[0][4].text)])

    return card
