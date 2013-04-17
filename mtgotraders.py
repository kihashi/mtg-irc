'''
A set of helper methods to help get pricing information from MTGO Traders.

Author: John Cleaver
License: BSD 3 Clause License
'''

import re
import urllib

store_url = "http://www.mtgotraders.com/store/"
price_api_url = "" #Url can be obtained from MTGO Traders.

def get_raw_list():
    file = urllib.urlopen(price_api_url)
    return file

def parse_list(price_file):
    card_dict = {}
    for line in price_file:
        line_list = line.split("|")
        if line_list[3] in card_dict:
        
        else:
            if line_list[2] = "R":
                card_dict[line_list[3]] = { line_list[0]: { "reg_price": line_list[5], "link": line_list[6] } }
            else
