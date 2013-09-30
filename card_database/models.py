from elixir import *

metadata.bind = "sqlite:///cards.sqlite"
metadata.bind.echo = True


class MagicCard(Entity):
    layout = ManyToOne('Layout')
    name = Field(Unicode(50))
    alt_side = OneToOne('MagicCard')
    mana_cost = Field(Unicode(30))
    converted_mana_cost = Field(Integer)
    colors = ManyToMany('Color')
    supertypes = ManyToMany('SuperType')
    card_types = ManyToMany('CardType')
    subtypes = ManyToMany('SubType')
    rarity = ManyToOne('Rarity')
    rules_text = Field(UnicodeText())
    power = Field(Unicode(30))
    toughness = Field(Unicode(30))
    loyalty = Field(Integer)
    expansions = ManyToMany('Expansion')
    rulings = OneToMany('Ruling')

    def get_card_text(self):
        card_string = self.name

        if self.mana_cost:
            card_string += " | " + self.mana_cost

        card_string += " |"

        for supers in self.supertypes:
            card_string += " " + supers

        for types in self.card_types:
            card_string += " " + types

        if self.subtypes:
            card_string += " --"
            for subs in self.subtypes:
                card_string += " " + subs

        if self.rules_text:
            card_string += " | " + self.rules_text

        if self.power and self.toughness:
            card_string += " | " + self.power + "/" + self.toughness

        if self.loyalty:
            card_string += " | " + self.loyalty

        if self.expansions:
            card_string += " | "
            for expansion in self.expansions:
                card_string += expansion + ", "
            card_string = card_string[0, -2]

        if self.rarity:
            card_string += " | " + self.rarity

        if self.alt_side:
            card_string += " | " + "Alt: " + self.alt_side

        return card_string

    def get_rulings(self, ruling_number=None):
        if ruling_number is None:
            return self.rulings
        else:
            return self.rulings[ruling_number]


class Ruling(Entity):
    date = Field(Date)
    text = Field(UnicodeText())
    card = ManyToOne('MagicCard')

    def __repr__(self):
        return "[{DATE}]: {TEXT}".format(DATE=self.date, TEXT=self.text)


class Color(Entity):
    color = Field(Unicode(10))
    cards = ManyToMany('MagicCards')

    def __repr__(self):
        return self.color


class SuperType(Entity):
    supertype = Field(Unicode(30))
    cards = ManyToMany('MagicCard')

    def __repr__(self):
        return self.supertype


class CardType(Entity):
    cardtype = Field(Unicode(30))
    cards = ManyToMany('MagicCard')

    def __repr__(self):
        return self.cardtype


class SubType(Entity):
    subtype = Field(Unicode(30))
    cards = ManyToMany('MagicCard')

    def __repr__(self):
        return self.subtype


class Rarity(Entity):
    rarity = Field(Unicode(10))
    abbreviation = Field(Unicode(1))
    cards = OneToMany

    def __repr__(self):
        return self.abbreviation


class Expansion(Entity):
    expansion = Field(Unicode(30))
    abbreviation = Field(Unicode(10))
    cards = ManyToMany('MagicCard')

    def __repr__(self):
        return self.abbreviation
