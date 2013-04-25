'''
A set of helper methods to help get pricing information from MTGO Traders.

Author: John Cleaver
License: BSD 3 Clause License
'''

import urllib

store_url = "http://www.mtgotraders.com/store/"
price_api_url = "***REMOVED***"  # Url can be obtained from MTGO Traders.


def get_raw_list():
    file = urllib.urlopen(price_api_url)
    return file


def parse_list(price_file):
    card_dict = {}
    for line in price_file:
        line_list = line.split("|")
        if line_list[0] != "BOOSTER" and line_list[0] != "" and line_list[1] != "EVENT":
            if line_list[3].lower() not in card_dict:
                card_dict[line_list[3].lower()] = {}

            if line_list[0] not in card_dict[line_list[3].lower()]:
                card_dict[line_list[3].lower()][line_list[0]] = {}

            if line_list[2] == "R":
                card_dict[line_list[3].lower()][line_list[0]]["reg_price"] = line_list[5]
            else:
                card_dict[line_list[3].lower()][line_list[0]]["foil_price"] = line_list[5]

            card_dict[line_list[3].lower()][line_list[0]]["link"] = store_url + line_list[6]

    return card_dict


def main():
    raw_list = get_raw_list()
    card_dict = parse_list(raw_list)

    print(card_dict['Garruk, Primal Hunter'])

if __name__ == '__main__':
    main()