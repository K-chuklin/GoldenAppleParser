from main import GoldenAppleParser, ga_url
import unittest


class GoldenAppleParserTestCase(unittest.TestCase):

    def test_init(self):
        GA_parser = GoldenAppleParser(ga_url, 1).__init__(ga_url, 1)
        self.assertEqual(GA_parser.__init__(ga_url, 1), None, 1)

    def test_get_urls(self):
        GA_parser = GoldenAppleParser(ga_url, 1).get_urls()
        self.assertEqual(None, None)

    def test_parser(self):
        GA_parser = GoldenAppleParser(ga_url, 1).parser()
        self.assertEqual(None, None)

