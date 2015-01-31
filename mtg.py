'''
mtg.py

A willie front-end for MTG Functions.
Author: John Cleaver
License: BSD 3-clause
'''

import willie
from willie.modules import price as mtgprice
from willie.modules import card as mtgcard
from willie.modules import mtgotraders as mtgotraders


@willie.module.commands("price")
def price(bot, trigger):
    if trigger.group(2) is not None:
        mtgcard.models.setup()
        card_price = mtgprice.get_tcgplayer_price(trigger.group(2))
        bot.reply(card_price)
        mtgcard.models.close()
    else:
        bot.reply("Usage: '.price CARD_NAME'")


@willie.module.commands("eprice")
def eprice(bot, trigger):
    if trigger.group(2) is not None:
        mtgcard.models.setup()
        try:
            card = mtgcard.find_card(trigger.group(2))
        except mtgcard.CardNotFoundError as e:
            bot.reply("Could not find the card: {CARD}".format(CARD=str(e)))
        else:
            bot.reply(card.get_mtgoprice())
        mtgcard.models.close()
    else:
        bot.reply("Usage: '.eprice CARD_NAME'")


@willie.module.commands("card")
def card(bot, trigger):
    if trigger.group(2) is not None:
        mtgcard.models.setup()
        try:
            card_text = mtgcard.find_card(trigger.group(2)).get_card_text()
        except mtgcard.CardNotFoundError as e:
            card_text = "Could not find the card: {CARD}".format(CARD=str(e))
        bot.reply(card_text)
        mtgcard.models.close()
    else:
        bot.reply("Usage: '.card CARD_NAME'")


@willie.module.commands("rulings")
def rulings(bot, trigger):
    if trigger.group(2) is not None:
        mtgcard.models.setup()
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
        mtgcard.models.close()
    else:
        bot.reply("Usage: '.rulings CARD_NAME [| RULING_NUMBER]'")


@willie.module.commands("flavor")
def flavor(bot, trigger):
    if trigger.group(2) is not None:
        mtgcard.models.setup()
        input_text = trigger.group(2).split("|")
        card_name = input_text[0]
        expansion_name = None
        if len(input_text) > 1:
            expansion_name = input_text[1].strip()
        try:
            card = mtgcard.find_card(card_name)
            if expansion_name is not None:
                expansion = mtgcard.find_expansion(expansion_name)
                release = mtgcard._find_release(card, expansion)
                bot.reply(release.flavor_text)
            else:
                bot.reply(card.get_flavor_text())
        except mtgcard.CardNotFoundError as e:
            bot.reply("Could not find the card: {CARD}".format(CARD=str(e)))
        except mtgcard.ExpansionNotFoundError as e:
            bot.reply("Could not find the expansion: {EXP}".format(EXP=str(e)))
        except mtgcard.ReleaseNotFoundError as e:
            bot.reply(str(e))
        mtgcard.models.close()
    else:
        bot.reply("Usage: .flavor CARD_NAME [| SET_CODE]'")
