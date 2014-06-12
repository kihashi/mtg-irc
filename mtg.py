'''
mtg.py

A willie front-end for MTG Functions.
Author: John Cleaver
License: BSD 3-clause
'''

import willie
from willie.modules import price as mtgprice
from willie.modules import card as mtgcard
from willie.modules import card_database


@willie.module.commands("price")
def price(bot, trigger):
    card_price = mtgprice.get_tcgplayer_price(trigger.group(2))
    bot.reply(card_price)


@willie.module.commands("card")
def card(bot, trigger):
    card_text = mtgcard.find_card(trigger.group(2)).get_card_text()
    bot.reply(card_text)


@willie.module.commands("rulings")
def rulings(bot, trigger):
    card_rulings = mtgcard.find_card(trigger.group(2))
    bot.reply(card_rulings.get_rulings())

@willie.module.commands("flavor")
def flavor(bot, trigger):
    find_card = mtgcard.find_card(trigger.group(2))
    bot.reply(find_card.get_flavor_text())
