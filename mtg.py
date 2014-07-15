'''
mtg.py

A willie front-end for MTG Functions.
Author: John Cleaver
License: BSD 3-clause
'''

import willie
from willie.modules import price as mtgprice
from willie.modules import card as mtgcard


@willie.module.commands("price")
def price(bot, trigger):
    card_price = mtgprice.get_tcgplayer_price(trigger.group(2))
    bot.reply(card_price)


@willie.module.commands("card")
def card(bot, trigger):
    try:
        card_text = mtgcard.find_card(trigger.group(2)).get_card_text()
    except mtgcard.CardNotFoundError as e:
        card_text = "Could not find the card: {CARD}".format(CARD=str(e))
    bot.reply(card_text)


@willie.module.commands("rulings")
def rulings(bot, trigger):
    input_text = trigger.group(2).split("|")
    card_name = input_text[0]
    if len(input_text) > 1:
        ruling_no = input_text[1]
        try:
            ruling_no = int(ruling_no)
        except ValueError:
            bot.reply("That is is not a number. Try .ruling CardName | 1")
            return
    else:
        ruling_no = None
    try:
        card_rulings = mtgcard.find_card(card_name).get_rulings(ruling_no)
    except mtgcard.CardNotFoundError as e:
        bot.reply("Could not find the card: {CARD}".format(CARD=str(e)))
    else:
        bot.reply(str(card_rulings[0]) + " | " + str(card_rulings[1]) + " of " + str(card_rulings[2]))


@willie.module.commands("flavor")
def flavor(bot, trigger):
    try:
        card = mtgcard.find_card(trigger.group(2))
    except mtgcard.CardNotFoundError as e:
        bot.reply("Could not find the card: {CARD}".format(CARD=str(e)))
    else:
        bot.reply(card.get_flavor_text())
