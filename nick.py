'''
This module contains a dictionary of card nicknames.

Author: John Cleaver
License: BSD 3 Clause.
'''

import card as mtgcard

nicknames = {
    "Dark Confidant": "Bob",
    "Solemn Simulacrum": "Jens",
    "Sylvan Safekeeper": "Olle",
    "Avalanche Riders": "Darwin",
    "Rootwater Thief": "Mike",
    "Meddling Mage": "Chris",
    "Shadowmage Infiltrator": "Finkel",
    "Voidmage Prodigy": "Kai",
    "Rakdos Augermage": "Terry",
    "Ranger of Eos": "Ruel",
    "Snapcaster Mage": "Tiago",
    "Solemn Simulacrum": "Sad Robot",
    "Skithiryx, the Blight Dragon": "Skittles",
    "Prodigal Sorcerer": "Tim",
    "Putrid Imp": "Pimp",
    "Phyrexian Negator": "The Rock",
    "Primeval Titan": "Prime Time",
    "Oblivion Stone": "O-Stone",
    "Oblivion Stone": "O Stone",
    "Thragtusk": "Swagtusk",
    "Jace Beleren": "Baby Jace",
    "Jace, The Mind Sculptor": "Papa Jace",
    "Jace, Memory Adept": "Emo Jace",
    "Jace, Architect of Thought": "New New Jace",
    "Magister Sphinx": "Two Punch Steve",
    "Assemble the Legion": "Dirty South"
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
