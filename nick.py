'''
This module contains a dictionary of card nicknames.

Author: John Cleaver
License: BSD 3 Clause.
'''

import card as mtgcard

nicknames = {
    u"Dark Confidant": u"Bob",
    u"Solemn Simulacrum": u"Jens",
    u"Sylvan Safekeeper": u"Olle",
    u"Avalanche Riders": u"Darwin",
    u"Rootwater Thief": u"Mike",
    u"Meddling Mage": u"Chris",
    u"Shadowmage Infiltrator": u"Finkel",
    u"Voidmage Prodigy": u"Kai",
    u"Rakdos Augermage": u"Terry",
    u"Ranger of Eos": u"Ruel",
    u"Snapcaster Mage": u"Tiago",
    u"Solemn Simulacrum": u"Sad Robot",
    u"Skithiryx, the Blight Dragon": u"Skittles",
    u"Prodigal Sorcerer": u"Tim",
    u"Putrid Imp": u"Pimp",
    u"Phyrexian Negator": u"The Rock",
    u"Primeval Titan": u"Prime Time",
    u"Oblivion Stone": u"O-Stone",
    u"Oblivion Stone": u"O Stone",
    u"Thragtusk": u"Swagtusk",
    u"Jace Beleren": u"Baby Jace",
    u"Jace, The Mind Sculptor": u"Papa Jace",
    u"Jace, Memory Adept": u"Emo Jace",
    u"Jace, Architect of Thought": u"New New Jace",
    u"Magister Sphinx": u"Two Punch Steve",
    u"Assemble the Legion": u"Dirty South"
}


def main():
    mtgcard.models.setup()
    for cardname, cardnickname in nicknames.iteritems():
        try:
            card = mtgcard.find_card(cardname)
            db_nick = mtgcard.models.CardNick()
            db_nick.nickname = cardnickname
            card.nicknames.append(db_nick)
        except mtgcard.CardNotFoundError:
            pass
    mtgcard.models.close()

if __name__ == '__main__':
    main()
