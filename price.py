'''
prices.py - Willie Magic: The Gathering Price Lookup Module
A module for the IRC Bot Willie that allows a user to get the TCG Player
prices for cards.

Author: John Cleaver

License: BSD 3 Clause
'''
import requests
import xml.etree.ElementTree as ET
from collections import OrderedDict
import string
import willie

partner_key = "MTGIRC" #This is the partner code assigned with you TCGPlayer API account.
secret_api_url = "" #This is the URL that the TCGPlayer Rep assigns you for API access.
get_vars = {"pk":partner_key, "s":"", "p":""}


@willie.modules.commands('price')
def price(bot, trigger):
    """Gets the TCG Player Prices for a specified card."""



def get_tcg_price(card_name):
    """ Makes the API call and returns the resultsing XML. """
    get_vars[p] = card_name
    try:
        r = requests.get(url, params=get_vars)
        r.raise_for_status()
        return r.text
    except HTTPError as e:
        return "TCGPlayer is either down or is having problems. Try again later."


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


class tcgprice():
    def __init__(self, card, hi, low, avg, link):
        self.card = card
        self.hi = hi
        self.low = low
        self.avg = avg
        self.link = link

    def __str__(self):
        return repr(self.card + " | " + "Avg: " + self.avg + " | " + "Low: " + self.low + " | " + "High: " + self.high + " | " + "Link: " + self.link)


class NoUrlException(Exception):
    def __str__(self):
        return repr("""The TCG API URL is not present.
                    Enter it and reload the module.""")
