'''
This file adds expansions that are used by MTGOtraders.

Adds several expansions that exist for card pricing but not for cards.
As well, it adds serveral set abbreviations that do not exist.

Author: John Cleaver <cleaver.john.k@gmail.com>
license: BSD 3-Clause
'''

import card as mtgcard
from card_database import models

expansions = {
    u"ULG": u"UL",
    u"UDS": u"UD"
}


models.setup()
promo = models.Expansion(name=u"Promotional",
                         abbreviation=u"PRM",
                         )
for k, v in expansions.iteritems():
    mtgcard.find_expansion(k).mtgo_code = v
models.close()
