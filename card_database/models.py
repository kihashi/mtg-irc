from elixir import *
import datetime

metadata.bind = u"sqlite:///cards.sqlite"
metadata.bind.echo = False


def setup():
    setup_all()
    create_all()


def close():
    session.commit()


class MagicCard(Entity):
    using_options(shortnames=True)

    layout = ManyToOne(u'Layout')
    name = Field(Unicode(50))
    search_name = Field(Unicode(50))
    alt_side = ManyToOne(u'MagicCard')
    mana_cost = Field(Unicode(30))
    converted_mana_cost = Field(Integer)
    colors = ManyToMany(u'Color')
    supertypes = ManyToMany(u'SuperType')
    card_types = ManyToMany(u'CardType')
    subtypes = ManyToMany(u'SubType')
    rules_text = Field(UnicodeText())
    printed_text = Field(UnicodeText())
    power = Field(Unicode(30))
    toughness = Field(Unicode(30))
    loyalty = Field(Integer)
    releases = OneToMany(u"CardRelease")
    rulings = OneToMany(u'Ruling')
    nicknames = OneToMany(u"CardNick")
    legality = OneToMany(u"Legality")

    def get_card_text(self):
        card_string = self.name

        if self.mana_cost:
            card_string += u" | " + self.mana_cost

        card_string += u" |"

        for supers in self.supertypes:
            card_string += u" " + unicode(supers)

        for types in self.card_types:
            card_string += u" " + unicode(types)

        if self.subtypes:
            card_string += u" --"
            for subs in self.subtypes:
                card_string += u" " + unicode(subs)

        if self.rules_text:
            card_string += u" | " + self.rules_text

        if self.power and self.toughness:
            card_string += u" | " + self.power + u"/" + self.toughness

        if self.loyalty:
            card_string += u" | " + str(self.loyalty)

        if self.releases:
            card_string += u" | "
            for release in self.releases:
                card_string += unicode(release.expansion).upper() + u"-" + unicode(release.rarity).upper() + u", "
            card_string = card_string[:-2]

        if self.alt_side:
            card_string += u" | " + u"Alt: " + unicode(self.alt_side)

        return card_string

    def get_printed_text(self):
        if self.printed_text is not None:
            return self.name + u" | " + self.printed_text

    def get_rulings(self, ruling_number=None, get_all=None):
        if get_all is not None:
            return self.rulings
        if len(self.rulings) < 1:
            return (None, 0, 0)
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
            for release in self.releases:
                if release.get_flavor_text() is not None:
                    return release.get_flavor_text()
            else:
                return None
        else:
            # expansion_set = Expansion.query.filter(Expansion.cards.has(())
            # if not expansion_set:
            #     raise ExpansionNotFoundError
            # release = CardRelease.query.get_by(card=self,expansion=flavor_expansion)
            return u""

    def get_legality(self):
        legality_text = self.name
        for l in self.legality:
            legality_text += u" | " + l.format_name.format_name + u": " + l.legality

        return legality_text

    def get_mtgoprice(self):
        output = self.name
        for release in self.releases:
            if release.mtgoprice.price is not None:
                output += u" | " + str(release.mtgoprice)
        if output == self.name:
            return None
        else:
            return output


class Ruling(Entity):
    using_options(shortnames=True)

    date = Field(Date)
    text = Field(UnicodeText())
    card = ManyToOne(u'MagicCard')

    def __unicode__(self):
        return u"[{DATE}]: {TEXT}".format(DATE=self.date, TEXT=self.text)

    def __str__(self):
        return self.__unicode__()


class Color(Entity):
    using_options(shortnames=True)

    color = Field(Unicode(10))
    abbreviation = Field(Unicode(1))
    cards = ManyToMany(u'MagicCard')

    def __unicode__(self):
        return self.color

    def __str__(self):
        return self.__unicode__()


class SuperType(Entity):
    using_options(shortnames=True)

    supertype = Field(Unicode(30))
    cards = ManyToMany(u'MagicCard')

    def __unicode__(self):
        return self.supertype

    def __str__(self):
        return self.__unicode__()


class CardType(Entity):
    using_options(shortnames=True)

    magictype = Field(Unicode(30))
    cards = ManyToMany(u'MagicCard')

    def __unicode__(self):
        return self.magictype

    def __str__(self):
        return self.__unicode__()


class SubType(Entity):
    using_options(shortnames=True)

    subtype = Field(Unicode(30))
    cards = ManyToMany(u'MagicCard')

    def __unicode__(self):
        return self.subtype

    def __str__(self):
        return self.__unicode__()


class Rarity(Entity):
    using_options(shortnames=True)

    rarity = Field(Unicode(10))
    abbreviation = Field(Unicode(5))
    cards = OneToMany(u"CardRelease")

    def __unicode__(self):
        return self.abbreviation

    def __str__(self):
        return self.__unicode__()


class Expansion(Entity):
    using_options(shortnames=True)

    name = Field(Unicode(30))
    abbreviation = Field(Unicode(10))
    old_code = Field(Unicode(10))
    gatherer_code = Field(Unicode(10))
    mtgo_code = Field(Unicode(10))
    cards = OneToMany(u"CardRelease")

    def __unicode__(self):
        return self.abbreviation

    def __str__(self):
        return self.__unicode__()

    def get_name(self):
        return self.name


class CardRelease(Entity):
    using_options(shortnames=True)

    expansion = ManyToOne(u"Expansion")
    card = ManyToOne(u"MagicCard")
    rarity = ManyToOne(u"Rarity")
    flavor_text = Field(Unicode(50))
    multiverse_id = Field(Integer)
    mtgoprice = OneToOne(u"MTGOPrice", inverse=u'release')

    def __unicode__(self):
        return self.card.name + u"-" + unicode(self.expansion)

    def __str__(self):
        return self.__unicode__()

    def get_flavor_text(self):
        if self.flavor_text is None:
            return None
        else:
            return u"[{EXPANSION}]: {TEXT}".format(EXPANSION=self.expansion, TEXT=self.flavor_text)


class Layout(Entity):
    using_options(shortnames=True)

    layout = Field(Unicode(30))
    abbreviation = Field(Unicode(2))

    def __unicode__(self):
        return self.abbreviation

    def __str__(self):
        return self.__unicode__()


class MTGOPrice(Entity):
    using_options(shortnames=True)

    release = ManyToOne(u"CardRelease")
    price = Field(Float)
    foil_price = Field(Float)
    link = Field(Unicode(30))
    last_fetch = Field(DateTime)

    def __unicode__(self):
        return u"[{EXP}]: {PRICE}".format(EXP=self.release.expansion.abbreviation, PRICE=unicode(self.price))

    def __str__(self):
        return self.__unicode__()


class CardNick(Entity):
    using_options(shortnames=True)

    card = ManyToOne(u"MagicCard")
    nickname = Field(Unicode(50))


class Format(Entity):
    using_options(shortnames=True)

    format_name = Field(Unicode(50))
    legality = OneToMany(u"Legality")


class Legality(Entity):
    using_options(shortnames=True)

    card = ManyToOne(u"MagicCard")
    format_name = ManyToOne(u"Format")
    legality = Field(Unicode(50))
