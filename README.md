mtg-irc
=======

A module for the IRC Bot [Phenny][] that allows users to query magic cards.

[Phenny]: http://inamidst.com/phenny/

Dependencies
------------

1. [Phenny][]
2. [Tutor][]

[Phenny]: http://inamidst.com/phenny/
[Tutor]: https://github.com/davidchambers/tutor

NOTE: Tutor must be installed and running on a server that is accessible from the computer that Phenny is running on.

Installation
------------

1. Copy `card.py` into Phenny's `modules` folder.
2. Edit `card.py` to replace `api_server` with the address of the server on which `Tutor` is running.
3. Start Phenny.

Commands
--------

```
.card, .sets, .flavor, .rulings, .image
```

### Card Search

The `.card` command searches Gatherer for a card whose name matches the given card name and returns the rules text of
the card. The rules text is said by the bot in the channel where the command was issued.

```
(09:17) Kihashi: .card Storm Crow
(09:17) CardBot: Kihashi: Storm Crow | {1}{U} | Creature  - Bird | Flying (This creature can't be blocked except by creatures with flying or reach.) | 1/2
```

### Card Rulings

The `.rulings` command searches Gatherer for a card whose name matches the given name and returns a list of rulings for
the card. Note that because this command returns many statements, it is returned as a PM rather than being displayed in
the appropriate channel.

```
(09:23) Kihashi: .rulings humility
(09:23) CardBot: 2006-02-01: With a Humility and two Opalescences on the battlefield, if Humility has the latest timestamp, then all creatures are 1/1 with no abilities. If the timestamp order is Opalescence, Humility, Opalescence, the second Opalescence is 1/1, and the Humility and first Opalescence are 4/4.  If Humility has the earliest timestamp, then everything is 4/4.
(09:23) CardBot: 2007-02-01: Removes all creature abilities. This includes mana abilities. Animated lands will also lose the ability to tap for mana.
(09:23) CardBot: 2009-10-01: This is the current interaction between Humility and Opalescence: The type-changing effect applies at layer 4, but the rest happens in the applicable layers.  The rest of it will apply even if the permanent loses its ability before it's finished applying. So if Opalescence, Humility, and Worship are on the battlefield and Opalescence entered the battlefield before Humility, the following is true: Layer 4: Humility and Worship each b
(09:23) CardBot: 2009-10-01: You apply power/toughness changing effects in a series of sublayers in the following order: (a) effects from characteristic-defining abilities; (b) effects that set power and/or toughness to a specific number or value; (c) effects that modify power and/or toughness but don't set power and/or toughness to a specific number or value; (d) changes from counters; (e) effects that switch a creature's power and toughness. This card's effect 
```

### Card Editions

The `.sets` command searches Gatherer for a card whose name matches the given one and returns a list of sets the card
has been printed in as well as the card's rarity in each of these sets. The list is said by the bot in the channel
where the command was issued.

```
(11:26) Kihashi: .sets Birds of Paradise
(11:26) CardBot: Kihashi: Seventh Edition - Rare | Fourth Edition - Rare | Revised Edition - Rare | Limited Edition Alpha - Rare | Eighth Edition - Rare | Magic 2011 - Rare | Magic 2012 - Rare | Tenth Edition - Rare | Fifth Edition - Rare | Classic Sixth Edition - Rare | Unlimited Edition - Rare | Limited Edition Beta - Rare | Ravnica: City of Guilds - Rare | Magic 2010 - Rare | 
```

### Card Flavor Text

The `.flavor` command searches Gatherer for a card whose name matches the one given and returns a list of the flavor
text for each edition of the card. Note that because this command returns many statements, it is returned as a PM rather than being displayed in
the appropriate channel.

```
(11:59) Kihashi: .flavor Storm Crow
(12:00) CardBot: Ninth Edition - Storm crow descending, winter unending. Storm crow departing, summer is starting.
(12:00) CardBot: Portal - Storm crow descending, winter unending.  Storm crow departing, summer is starting.
(12:00) CardBot: Alliances - "It tells you that the worst is coming. Do you listen?—Lovisa Coldeyes,Balduvian Chieftain
(12:00) CardBot: Eighth Edition - Storm crow descending, winter unending. Storm crow departing, summer is starting.
(12:00) CardBot: Alliances - Watch for it Right on its tailfeathers will be a storm from your nightmares.
(12:00) CardBot: Classic Sixth Edition - Storm crow descending, winter unending.Storm crow departing, summer is starting.
(12:00) CardBot: Seventh Edition - Storm crow descending, winter unending.Storm crow departing, summer is starting.
(12:00) CardBot: Starter 1999 - Storm crow descending, winter unending.Storm crow departing, summer is starting.
```

### Card Image Link

The `.image` command searches Gatherer for a card whose name matches the one given and returns a URL to the image of the
card. The link is said by the bot in the channel where the command was issued.

```
(12:10) Kihashi: .image Pernicious Deed
(12:10)	CardBot: Kihashi: http://gatherer.wizards.com/Handlers/Image.ashx?name=Pernicious+Deed&type=card
```