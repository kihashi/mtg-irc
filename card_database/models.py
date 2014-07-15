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
    rules_text = Field(UnicodeText())
    power = Field(Unicode(30))
    toughness = Field(Unicode(30))
    loyalty = Field(Integer)
    releases = OneToMany("CardRelease")
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
            card_string += " | " + str(self.loyalty)

        if self.releases:
            card_string += " | "
            for release in self.releases:
                card_string += str(release.expansion).upper() + "-" + str(release.rarity).upper() + ", "
            card_string = card_string[:-2]

        if self.alt_side:
            card_string += " | " + "Alt: " + str(self.alt_side)

        return card_string

    def get_rulings(self, ruling_number=None, get_all=None):
        if get_all is not None:
            return self.rulings
        if ruling_number is None:
            return (self.rulings[0], 1, len(self.rulings))
        else:
            if ruling_number >= len(self.rulings):
                ruling_number = len(self.rulings)
            elif ruling_number <= 0:
                ruling_number = 1
            return (self.rulings[ruling_number - 1], ruling_number, len(self.rulings))

    def get_flavor_text(self, flavor_expansion=None, get_all=None):
        if get_all is not None:
            flavor_array = []
            for release in self.releases:
                flavor_array.append(release.get_flavor_text())
            return flavor_array
        if flavor_expansion is None:
            return self.releases[-1].get_flavor_text()
        else:
            #TODO: return flavor text from the specific expansion.
            return ""


class Ruling(Entity):
    using_options(shortnames=True)

    date = Field(Date)
    text = Field(UnicodeText())
    card = ManyToOne('MagicCard')

    def __repr__(self):
        return u"[{DATE}]: {TEXT}".format(DATE=self.date, TEXT=self.text).encode('utf-8')


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

    magictype = Field(Unicode(30))
    cards = ManyToMany('MagicCard')

    def __repr__(self):
        return self.magictype


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
    cards = OneToMany("CardRelease")

    def __repr__(self):
        return self.abbreviation


class Expansion(Entity):
    using_options(shortnames=True)

    name = Field(Unicode(30))
    abbreviation = Field(Unicode(10))
    cards = OneToMany("CardRelease")

    def __repr__(self):
        return self.abbreviation


class CardRelease(Entity):
    using_options(shortnames=True)

    expansion = ManyToOne("Expansion")
    card = ManyToOne("MagicCard")
    rarity = ManyToOne("Rarity")
    flavor_text = Field(Unicode(50))
    multiverse_id = Field(Integer)

    def __str__(self):
        return str(self.card.name) + "-" + str(self.expansion)

    def get_flavor_text(self):
        return u"[{EXPANSION}]: {TEXT}".format(EXPANSION=self.expansion, TEXT=self.flavor_text).encode('utf-8')


class Layout(Entity):
    using_options(shortnames=True)

    layout = Field(Unicode(30))
    abbreviation = Field(Unicode(2))

    def __repr__(self):
        return self.abbreviation


class mtgoprice(Entity):
    using_options(shortnames=True)

    card = ManyToOne('MagicCard')
    expansion = ManyToOne('Expansion')
    price = Field(Float)
