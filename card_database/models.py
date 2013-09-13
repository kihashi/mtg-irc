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


class Ruling(Entity):
    date = Field(Date)
    text = Field(UnicodeText())
    card = ManyToOne('MagicCard')


class Color(Entity):
    color = Field(Unicode(10))
    cards = ManyToMany('MagicCards')


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
