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
    card_text = mtgcard.find_card(trigger.group(2)).get_card_text()
    bot.reply(card_text)


@willie.module.commands("rulings")
def rulings(bot, trigger):
    output_text = ""
    input_text = trigger.group(2).split("|")
    card_name = input_text[0]
#TODO: Move this logic into the model.
    if len(input_text) > 1:
        ruling_no = input_text[1]
        try:
            ruling_no = int(ruling_no)
        except ValueError:
            bot.reply("That is is not a number. Try .ruling CardName | 1")
            return
    else:
        ruling_no = None
    card_rulings = mtgcard.find_card(card_name).get_rulings()
    if ruling_no is None:
        output_text = card_rulings[0]
    else:
        if ruling_no >= len(input_text):
            output_text = card_rulings[-1]
        else:
            output_text = card_rulings[int(ruling_no)]
    bot.reply(output_text + " --- " + len(card_rulings))


@willie.module.commands("flavor")
def flavor(bot, trigger):
    find_card = mtgcard.find_card(trigger.group(2))
    for flavor in find_card.get_flavor_text():
        bot.reply(flavor)
