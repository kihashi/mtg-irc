'''
A Class to hold all of the information about a MtG card.

Author: John Cleaver
License: BSD 3 Clause
'''


class MagicCard():
    def __init__(self,
                 name,
                 card_type,
                 expansions,
                 supertype=None,
                 mana_cost=None,
                 rules_text=None):

        self.name = name
        self.supertype = supertype
        self.card_type = card_type
        self.expansions = expansions
        self.mana_cost = mana_cost
        self.rules_text = rules_text

    def __str__(self):
        sets_string = ''
        for key, value in self.expansions.iteritems():
            if sets_string != '':
                sets_string += ', '
            sets_string += key + '-' + value

        return "{NAME} | {MANA} | {SUPERTYPE} {TYPE} |" +
               " {RULES} | {SETS}".format(NAME=self.name,
                                          MANA=self.mana_cost,
                                          SUPERTYPE=supertype,
                                          TYPE=self.card_type,
                                          RULES=self.rules_text,
                                          SETS=sets_string)


class CreatureCard(MagicCard):
    def __init__(self, name, card_type, subtypes, expansions, power, toughness, supertype=None, mana_cost=None, rules_text=None):
        MagicCard.__init__(name, u'Creature', expansions, supertype, mana_cost, rules_text)
        self.power = power
        self.toughness = toughness
        self.subtypes = subtypes

    def __str__(self):
        sets_string = ''
        subtypes_string = ''

        for key, value in self.expansions.iteritems():
            if sets_string != '':
                sets_string += ', '
            sets_string += key + '-' + value

        for sub in self.subtypes:
            subtypes_string += " " + sub

        return "{NAME} | {MANA} | {SUPERTYPE} {TYPE} -- {SUBS} | {RULES} | {SETS}".format(NAME=self.name, MANA=self.mana_cost, SUPERTYPE=supertype, TYPE=self.card_type, SUBS=subtypes_string, RULES=self.rules_text, SETS=sets_string)
