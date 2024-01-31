from main import GoldenAppleParser, ga_url
import unittest


class GoldenAppleParserTestCase(unittest.TestCase):

    def test_init(self):
        GA_parser = GoldenAppleParser(ga_url, 100).__init__(ga_url, 100)
        self.assertEqual(GA_parser.__init__(ga_url, 100), None, 100)
