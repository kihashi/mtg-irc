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
    rulings = ManyToMany('Ruling')

