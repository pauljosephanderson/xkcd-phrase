import unittest

from xkcd_phrase import xkcd_phrase
from xkcd_phrase.lib.xkcd_default import DEFAULT_WORDFILE, SPECIAL_CHARS
from re import match

class TestGenerateWordlist(unittest.TestCase):
    """
    Test cases for function `generate_xkpassword`.
    """

    def shortDescription(self) -> None:
        return None

    def setUp(self) -> None:
        """
        Set up fixtures for this test case.
        """
        self.wordlist_small = xkcd_phrase.generate_wordlist(
            wordfile="tests/test_files/test_list", 
            min_length=5,
            max_length=9,
            valid_chars="[a-z]"
        )


    def test_delim(self) -> None:
        """
        Test delimiter is set correctly.
        """
        numwords=6
        interactive=False
        delimiter=""
        valid_delim=list(SPECIAL_CHARS.values())
        case="lower"
        acrostic=False
        no_numeric_char=False
        numeric_char_num=2
        no_special_char=False
        special_char_num=2
        testing=False
        result = xkcd_phrase.generate_xkphrase(self.wordlist_small, 
                                               numwords,
                                               interactive,
                                               delimiter,
                                               valid_delim,
                                               case,
                                               acrostic,
                                               numeric_char_num,
                                               special_char_num,
                                               testing
                                               )
        self.assertIsNotNone(match("([a-zA-Z]+(_|)+([0-9])+)+", result))


if __name__ == "__main__":
    test_cases = [
        TestGenerateWordlist,
    ]
    suites = [unittest.TestLoader().loadTestsFromTestCase(test_case) for test_case in test_cases]
    unittest.TextTestRunner(verbosity=2, buffer=True).run(unittest.TestSuite(suites))
