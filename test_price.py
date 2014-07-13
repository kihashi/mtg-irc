'''
test_price.py

A Unit Test Module for the MTG Price module.

Author: John Cleaver
License: BSD 3-Clause
'''

import unittest
import price


class PriceTestCase(unittest.TestCase):
    """Tests for price.py."""

    def test_xml_return(self):
        """Tests to see if we get back XML from TCGPlayer"""
        self.assertIn("<?xml",
                      price.get_tcgplayer_xml("Snap"),
                      "Looks like we did not get back XML from TCGPlayer.")

    def test_html_error(self):
        """Tests to see what happens when TCGPlayer is down"""
        self.assertRaises(price.requests.RequestException,
                          price.get_tcgplayer_xml,
                          "Snap",
                          "http://localhost/")

    def test_xml_parse(self):
        """Tests if the XML was parsed correctly."""
        card_name = "Bayou"
        xml = price.get_tcgplayer_xml(card_name)
        card_price = price.parse_tcg_player_xml(card_name, xml)
        self.assertIsInstance(card_price,
                              price.TCGPrice)
        for key, value in card_price:
            self.assertTrue(value != "")

    def test_card_not_found(self):
        """Tests to see what happens when a card does not exist."""
        card_name = "nonexistingcard"
        xml = price.get_tcgplayer_xml(card_name)
        self.assertRaises(price.CardNotFoundError,
                          price.parse_tcg_player_xml,
                          card_name,
                          xml)

if __name__ == "__main__":
    unittest.main()
