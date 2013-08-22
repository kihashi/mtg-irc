from elixir import *

metadata.bind = "sqlite:///cards.sqlite"
metadata.bind.echo = True

class MagicCard(Entity):
    using_options(inheritance='multi')
    name = Field(Unicode(50))
    card_types = ManyToMany('CardType')
    expansions = ManyToMany('Expansion')
    rarity = ManyToOne('Rarity')
    supertypes = ManyToMany('SuperType')
    subtypes = ManyToMany('SubType')
    mana_cost = Field(Unicode(30))
    rules_text = Field(UnicodeText())

    def __repr__(self):
        sets_string = ''
        for key, value in self.expansions.iteritems():
            if sets_string != '':
                sets_string += ', '
            sets_string += key + '-' + value

        return "{NAME} | {MANA} | {TYPES} |" + \
               " {RULES} | {SETS}".format(NAME=self.name,
                                          MANA=self.mana_cost,
                                          SUPERTYPE=supertype,
                                          TYPE=self.card_type,
                                          RULES=self.rules_text,
                                          SETS=sets_string)


class CreatureCard(MagicCard):
    using_options(inheritance='multi')
    power = Field(Integer)
    toughness = Field(Integer)

    def __repr__(self):
        return MagicCard.__repr__(self) + " | {POWER}/{TOUGHNESS}".format(POWER=self.power,

