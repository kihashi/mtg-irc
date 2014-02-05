from elixir import *

metadata.bind = "sqlite:///cards.sqlite"
metadata.bind.echo = False


def setup():
    setup_all()
    create_all()


def close():
    session.commit()


class MagicCard(Entity):
    using_options(shortnames=True)

    layout = ManyToOne('Layout')
    name = Field(Unicode(50))
    search_name = Field(Unicode(50))
    alt_side = ManyToOne('MagicCard')
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
            card_string += " " + str(supers)

        for types in self.card_types:
            card_string += " " + str(types)

        if self.subtypes:
            card_string += " --"
            for subs in self.subtypes:
                card_string += " " + str(subs)

        if self.rules_text:
            card_string += " | " + self.rules_text

        if self.power and self.toughness:
            card_string += " | " + self.power + "/" + self.toughness

        if self.loyalty:
            card_string += " | " + self.loyalty

        if self.expansions:
            card_string += " | "
            for expansion in self.expansions:
                card_string += str(expansion).upper() + ", "
            card_string = card_string[:-2]

        if self.rarity:
            card_string += " | " + str(self.rarity)

        if self.alt_side:
            card_string += " | " + "Alt: " + str(self.alt_side)

        return card_string

    def get_rulings(self, ruling_number=None):
        if ruling_number is None:
            return self.rulings
        else:
            return self.rulings[ruling_number]


class Ruling(Entity):
    using_options(shortnames=True)

    date = Field(Date)
    text = Field(UnicodeText())
    card = ManyToOne('MagicCard')

    def __repr__(self):
        return "[{DATE}]: {TEXT}".format(DATE=self.date, TEXT=self.text)


class Color(Entity):
    using_options(shortnames=True)

    color = Field(Unicode(10))
    abbreviation = Field(Unicode(1))
    cards = ManyToMany('MagicCard')

    def __repr__(self):
        return self.color


class SuperType(Entity):
    using_options(shortnames=True)

    supertype = Field(Unicode(30))
    cards = ManyToMany('MagicCard')

    def __repr__(self):
        return self.supertype


class CardType(Entity):
    using_options(shortnames=True)

    cardtype = Field(Unicode(30))
    cards = ManyToMany('MagicCard')

    def __repr__(self):
        return self.cardtype


class SubType(Entity):
    using_options(shortnames=True)

    subtype = Field(Unicode(30))
    cards = ManyToMany('MagicCard')

    def __repr__(self):
        return self.subtype


class Rarity(Entity):
    using_options(shortnames=True)

    rarity = Field(Unicode(10))
    abbreviation = Field(Unicode(5))
    cards = OneToMany

    def __repr__(self):
        return self.abbreviation


class Expansion(Entity):
    using_options(shortnames=True)

    expansion = Field(Unicode(30))
    abbreviation = Field(Unicode(10))
    cards = ManyToMany('MagicCard')

    def __repr__(self):
        return self.abbreviation


class Layout(Entity):
    using_options(shortnames=True)

    layout = Field(Unicode(30))
    abbreviation = Field(Unicode(2))

    def __repr__(self):
        return self.abbreviation
