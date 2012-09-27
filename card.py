'''
card.py - Phenny Magic: the Gathering Card Lookup Module
A module for the IRC Bot Phenny that allows for one to get the Oracle text
for any Magic: the Gathering card by card name.

Author: John Cleaver
Site: https://github.com/kihashi/mtg-irc
License: BSD 3 Clause.
'''

cards = []

def card(phenny, input):
    card_list()
    if not input.group(2):
        phenny.say('Perhaps you meant ".card Storm Crow"?')
    else:
        string = cards[index_containing_substring(cards, input.group(2))]
        card_listing = string.split("\n")
        for line in card_listing:
            phenny.say(line)



card.commands = ['card']
card.priority = 'medium'

def card_list():
    file = open('modules/oracle.txt', 'r')

    internal_entry = ''

    for line in file:
        if line == '\n':
            cards.append(internal_entry)
            internal_entry = ''
        else:
            internal_entry += line

def index_containing_substring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
              return i
    return -1

