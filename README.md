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
