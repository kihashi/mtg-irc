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

# This is the partner code assigned with you TCGPlayer API account.
partner_key = "MTGIRC"
# This is the URL that the TCGPlayer Rep assigns you for API access.
secret_api_url = ""
get_vars = {"pk": partner_key, "s": "", "p": ""}


def get_tcgplayer_price(card_name):
    card_name = sanitize(card_name)
    try:
        tcgxml = get_tcgplayer_xml(card_name)
    except requests.RequestException as e:
        return "TCGPlayer is either down or is having problems." \
               + " " \
               + "Try again later." \
               + " " \
               + str(e)
    else:
        try:
            tcgprice = parse_tcg_player_xml(card_name, tcgxml)
        except CardNotFoundError as e:
            return "Could not find the card: " + str(e)
        else:
            return tcgprice


def get_tcgplayer_xml(card_name, url=secret_api_url):
    """ Makes the API call and returns the resultsing XML. """
    get_vars['p'] = card_name
    r = requests.get(url, params=get_vars)
    r.raise_for_status()
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
                    root[0][4].text)

    return card


def sanitize(card_name):
    return card_name


class TCGPrice():
    def __init__(self, card, high, low, avg, link):
        self.card = card
        self.high = high
        self.low = low
        self.avg = avg
        self.link = link

    def __str__(self):
        return (self.card
                + " | "
                + "Avg: " + self.avg
                + " | "
                + "Low: " + self.low
                + " | "
                + "High: " + self.high
                + " | "
                + "Link: " + self.link)

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
