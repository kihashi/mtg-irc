mtg-irc
=======

A set of modules and supporting libraries for the [Willie][] IRC bot.

This version is a major update. There are now many more features as well as the infrastructure to add many more.


Dependencies
------------

1. [Willie][]
2. [SQLAlchemy][]
3. [Elixir][]
4. [Paver][] (For easier install)

Installation
------------

I have a pavement file that should automate most of the setup tasks for you. There are a couple steps:

1. Download Card Data
2. Add static data (Colors, Rarities, etc.) to the database.
3. Add Card data to the database (This step takes some time).
4. Add pricing data to the database.
5. Run tests.

Using pavement, we can narrow this down to:

```
paver fromcleanall
paver deploy
```

Note that the deploy task assumes that Willie is in the same directory as `mtg-irc`. This needs to be changed in the future.

Commands
--------

```
.card, .price, .eprice, .flavor, .rulings
```
