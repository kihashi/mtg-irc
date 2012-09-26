'''
card.py - Phenny Magic: the Gathering Card Lookup Module
A module for the IRC Bot Phenny that allows for one to get the Oracle text
for any Magic: the Gathering card by card name.

Author: John Cleaver
Site: https://github.com/kihashi/mtg-irc
License: BSD 3 Clause.
'''

def card(phenny, input):
	return phenny.say('Perhaps you meant ".card Storm Crow"?')
card.commands = ['card']
card.priority = 'medium'
