'''
prices.py - Willie Magic: The Gathering Price Lookup Module
A module for the IRC Bot Willie that allows a user to get the TCG Player
prices for cards.

Author: John Cleaver

License: BSD 3 Clause
'''
import requests
import xml.etree.ElementTree as ET
import sys
import argparse
import config
from unidecode import unidecode

get_vars = {"pk": config.tcgplayer_partner_code, "s": "", "p": ""}


def get_tcgplayer_price(card_name):
    card_name = sanitize(card_name)
    try:
        tcgxml = get_tcgplayer_xml(card_name)

    except requests.RequestException as e:
        return u"TCGPlayer is either down or is having problems." \
               + u" " \
               + u"Try again later." \
               + u" " \
               + unicode(e)
    else:
        try:
            if tcgxml == u"Product not found.":
                raise CardNotFoundError(card_name)
            tcgprice = parse_tcg_player_xml(card_name, tcgxml)
        except CardNotFoundError as e:
            return u"Could not find the card: " + unicode(e)
        except ET.ParseError as e:
            return u"TCGPlayer is not returning XML for that. Perhaps something went wrong?"
        else:
            return tcgprice


def get_tcgplayer_xml(card_name, url=config.tcgplayer_api_url):
    """ Makes the API call and returns the resulting XML. """
    if not url:
        raise NoUrlException()
    get_vars['p'] = unidecode(card_name)
    r = requests.get(url, params=get_vars)
    return r.text


def parse_tcg_player_xml(card_name, xml):
    """ Converts the XML response from the API into an ordered dict. """
    root = ET.fromstring(xml)

    if root.text is None:
        raise CardNotFoundError(card_name)

    card = TCGPrice(card_name,
                    root[0][1].text,
                    root[0][2].text,
                    root[0][3].text,
                    root[0][4].text,
                    root[0][5].text)

    return card


def sanitize(card_name):
    return card_name


class TCGPrice():
    def __init__(self, card, high, low, avg, foil, link):
        self.card = card
        self.high = high
        self.low = low
        self.avg = avg
        self.foil = foil
        self.link = link

    def __unicode__(self):
        return (self.card
                + u" | "
                + u"Avg: " + self.avg
                + u" | "
                + u"Low: " + self.low
                + u" | "
                + u"High: " + self.high
                + u" | "
                + u"Foil: " + self.foil
                + u" | "
                + u"Link: " + self.link)

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value


class NoUrlException(Exception):
    def __str__(self):
        return repr("""The TCG API URL is not present.
                    Enter it and reload the module.""")


class CardNotFoundError(Exception):
    def __init__(self, card_name):
        self.card_name = card_name

    def __str__(self):
        return self.card_name


def main(argv):
    if not argv.card:
        print "You must specify a card."
        sys.exit()
    else:
        print(get_tcgplayer_price(" ".join(argv.card)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("card", nargs="+", help="The Card to find.")
    args = parser.parse_args()
    main(args)
