'''
A set of helper methods to help get pricing information from MTGO Traders.

Author: John Cleaver
License: BSD 3 Clause License
'''

import requests
import config


def get_raw_list(url):
    r = requests.get(url)
    r.raise_for_status()
    return r.text


def parse_list(price_text):
    card_dict = {}
    for line in price_text:
        line_list = line.split("|")
        if line_list[0] != "BOOSTER" \
           and \
           line_list[0] != "" \
           and \
           line_list[1] != "EVENT":
            if line_list[3].lower() not in card_dict:
                card_dict[line_list[3].lower()] = {}

            if line_list[0] not in card_dict[line_list[3].lower()]:
                card_dict[line_list[3].lower()][line_list[0]] = {}

            if line_list[2] == "R":
                card_dict[line_list[3].lower()][line_list[0]]["reg_price"] \
                    = line_list[5]
                card_dict[line_list[3].lower()][line_list[0]]["link"] \
                    = store_url + line_list[6]
            else:
                card_dict[line_list[3].lower()][line_list[0]]["foil_price"] \
                    = line_list[5]

    return card_dict


def main():
    parse_list(get_raw_list(config.mtgotraders_api_url))

if __name__ == '__main__':
    main()
