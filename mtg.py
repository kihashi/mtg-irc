# -*- coding: utf-8 -*-
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
from urllib import quote


@willie.module.commands("price")
def price(bot, trigger):
    if trigger.group(2) is not None:
        mtgcard.models.setup()
        try:
            card_name = mtgcard.find_card(trigger.group(2)).name
        except mtgcard.CardNotFoundError as e:
            bot.reply(u"Could not find the card: {CARD}".format(CARD=unicode(e)))
        else: 
            card_price = mtgprice.get_tcgplayer_price(card_name)
            bot.reply(card_price)
        mtgcard.models.close()
    else:
        bot.reply(u"Usage: '.price CARD_NAME'")


@willie.module.commands("eprice")
def eprice(bot, trigger):
    if trigger.group(2) is not None:
        mtgcard.models.setup()
        try:
            card = mtgcard.find_card(trigger.group(2))
        except mtgcard.CardNotFoundError as e:
            bot.reply(u"Could not find the card: {CARD}".format(CARD=unicode(e)))
        else:
            bot.reply(card.get_mtgoprice())
        mtgcard.models.close()
    else:
        bot.reply(u"Usage: '.eprice CARD_NAME'")


@willie.module.commands("card")
def card(bot, trigger):
    if trigger.group(2) is not None:
        mtgcard.models.setup()
        try:
            card_text = mtgcard.find_card(trigger.group(2)).get_card_text()
        except mtgcard.CardNotFoundError as e:
            card_text = (u"Could not find the card: {CARD}".format(CARD=unicode(e)))
        bot.reply(card_text)
        mtgcard.models.close()
    else:
        bot.reply(u"Usage: '.card CARD_NAME'")


@willie.module.commands("printed")
def printed(bot, trigger):
    if trigger.group(2) is not None:
        mtgcard.models.setup()
        try:
            card_text = mtgcard.find_card(trigger.group(2)).get_printed_text()
        except mtgcard.CardNotFoundError as e:
            card_text = u"Could not find the card: {CARD}".format(CARD=unicode(e))
        bot.reply(card_text)
        mtgcard.models.close()
    else:
        bot.reply("Usage: '.printed CARD_NAME'")


@willie.module.commands("legality")
def legality(bot, trigger):
    if trigger.group(2) is not None:
        mtgcard.models.setup()
        try:
            card_text = mtgcard.find_card(trigger.group(2)).get_legality()
        except mtgcard.CardNotFoundError as e:
            card_text = u"Could not find the card: {CARD}".format(CARD=unicode(e))
        bot.reply(card_text)
        mtgcard.models.close()
    else:
        bot.reply(u"Usage: '.legality CARD_NAME'")


@willie.module.commands("rulings")
def rulings(bot, trigger):
    if trigger.group(2) is not None:
        mtgcard.models.setup()
        input_text = trigger.group(2).split(u"|")
        card_name = input_text[0]
        if len(input_text) > 1:
            ruling_no = input_text[1]
            try:
                ruling_no = int(ruling_no)
            except ValueError:
                bot.reply(u"That is is not a number. Try .ruling CardName | 1")
                return
        else:
            ruling_no = None
        try:
            card_rulings = mtgcard.find_card(card_name).get_rulings(ruling_no)
        except mtgcard.CardNotFoundError as e:
            bot.reply(u"Could not find the card: {CARD}".format(CARD=unicode(e)))
        else:
            bot.reply(unicode(card_rulings[0]) + u" | " + unicode(card_rulings[1]) + u" of " + unicode(card_rulings[2]))
        mtgcard.models.close()
    else:
        bot.reply(u"Usage: '.rulings CARD_NAME [| RULING_NUMBER]'")


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
            bot.reply(u"Could not find the card: {CARD}".format(CARD=unicode(e)))
        except mtgcard.ExpansionNotFoundError as e:
            bot.reply(u"Could not find the expansion: {EXP}".format(EXP=unicode(e)))
        except mtgcard.ReleaseNotFoundError as e:
            bot.reply(e)
        mtgcard.models.close()
    else:
        bot.reply(u"Usage: .flavor CARD_NAME [| SET_CODE]'")


@willie.module.commands("image")
def image(bot, trigger):
    if trigger.group(2) is not None:
        mtgcard.models.setup()
        input_text = trigger.group(2).split(u"|")
        card_name = unicode(input_text[0])
        expansion_name = None
        if len(input_text) > 1:
            expansion_name = unicode(input_text[1].strip())
        try:
            card = mtgcard.find_card(card_name)
            if expansion_name is not None:
                expansion = mtgcard.find_expansion(expansion_name)
                release = mtgcard._find_release(card, expansion)
                bot.reply(willie.web.quote(u"http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=" + unicode(release.multiverse_id) + u"&type=card", u":/,=&?"))
            else:
                bot.reply(willie.web.quote(u"http://gatherer.wizards.com/Handlers/Image.ashx?name=" + card.name + u"&type=card", u":/,=&?'!Æt\"æÄäÁáÂâÖöÛûÜü"))
        except mtgcard.CardNotFoundError as e:
            bot.reply(u"Could not find the card: {CARD}".format(CARD=unicode(e)))
        except mtgcard.ExpansionNotFoundError as e:
            bot.reply(u"Could not find the expansion: {EXP}".format(EXP=unicode(e)))
        except mtgcard.ReleaseNotFoundError as e:
            bot.reply(e)
        mtgcard.models.close()
    else:
        bot.reply(u"Usage: .image CARD_NAME [| SET_CODE]'")
