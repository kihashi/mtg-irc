'''
A set of helper methods to help get pricing information from MTGO Traders.

Author: John Cleaver
License: BSD 3 Clause License
'''

import requests
import card as mtgcard
import config


def get_raw_list(url):
    r = requests.get(url)
    r.raise_for_status()
    return r.text


def parse_list(price_text):
    for line in price_text.splitlines():
        line_list = line.replace("<br>", "").strip().split("|")
        if line_list[0] != "BOOSTER":
            try:
                card_release = mtgcard.find_release_by_name(line_list[3],
                                                            line_list[0])
            except mtgcard.CardError as e:
                print "---------------------------"
                print type(e)
                print line
                print "Card: " + line_list[3]
                print "Set:" + line_list[0]
                print "Price: " + line_list[5]
            except IndexError as e:
                pass
            else:
                if line_list[2] == "R":
                    card_release.mtgoprice.price = float(line_list[5])
                else:
                    card_release.mtgoprice.foil_price = float(line_list[5])


def main():
    parse_list(get_raw_list(config.mtgotraders_api_url))

if __name__ == '__main__':
    main()
