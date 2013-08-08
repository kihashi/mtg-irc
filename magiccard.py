'''
A Class to hold all of the information about a MtG card.

Author: John Cleaver
License: BSD 3 Clause
'''


class MagicCard():
    def __init__(self,
                 name,
                 card_types,
                 expansions,
                 rarity,
                 supertypes=None,
                 subtypes=None,
                 mana_cost=None,
                 rules_text=None):

        self.name = name
        self.supertypes = supertypes
        self.card_types = card_types
        self.expansions = expansions
        self.mana_cost = mana_cost
        self.rules_text = rules_text

    def __str__(self):
        sets_string = ''
        for key, value in self.expansions.iteritems():
            if sets_string != '':
                sets_string += ', '
            sets_string += key + '-' + value

        return "{NAME} | {MANA} | {TYPES} |" +
               " {RULES} | {SETS}".format(NAME=self.name,
                                          MANA=self.mana_cost,
                                          SUPERTYPE=supertype,
                                          TYPE=self.card_type,
                                          RULES=self.rules_text,
                                          SETS=sets_string)


class CreatureCard(MagicCard):
    def __init__(self,
                 name,
                 card_types,
                 expansions,
                 rarity,
                 supertypes=None,
                 subtypes=None,
                 mana_cost=None,
                 rules_text=None,
                 power=None,
                 toughness=None):

        MagicCard.__init__(self,
                           name,
                           card_types,
                           expansions,
                           rarity,
                           supertypes,
                           subtypes,
                           mana_cost,
                           rules_text)
        self.power = power
        self.toughness = toughness

    def __str__(self):
        sets_string = MagicCard.__str__(self)
        return sets_string += " | {POWER}/{TOUGHNESS}".format(POWER=self.power,
                                                              TOUGHNESS=self.toughness)

class PlaneswalkerCard(MagicCard):
    def __init__(self,
                 name,
                 card_types,
                 expansions,
                 rarity,
                 supertypes=None,
                 subtypes=None,
                 mana_cost=None,
                 rules_text=None,
                 loyalty=None):

        MagicCard.__init__(self,
                           name,
                           card_types,
                           expansions,
                           rarity,
                           supertypes,
                           subtypes,
                           mana_cost,
                           rules_text)

        self.loyalty = loyalty

