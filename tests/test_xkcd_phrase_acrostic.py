import unittest
import contextlib

from xkcd_phrase import (xkcd_phrase)
from xkcd_phrase.lib.xkcd_default import DEFAULT_WORDFILE
from xkcd_phrase.lib.xkcd_utilities import (wordlist_to_worddict, find_acrostic)


class TestGenerateAcrostic(unittest.TestCase):
    """
    Test cases for acrostic.
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

    def test_good_acrostic(self):
        word = "face"
        result = find_acrostic(word, 
                wordlist_to_worddict(self.wordlist_small))       
        self.assertEqual("".join(map(lambda x: x[0], result)), word)

    def test_upper_case_acrostic(self):
        word = "FACE"
        result = find_acrostic(word, 
                wordlist_to_worddict(self.wordlist_small))       
        self.assertEqual("".join(map(lambda x: x[0], result)), word.lower())

    def test_bad_acrostic(self):
        word ="xylophone"
        wordList = wordlist_to_worddict(self.wordlist_small)
        with self.assertRaises(SystemExit) as cm, contextlib.redirect_stderr(find_acrostic(word, wordList)):
            self.assertEqual(cm.exception.code, 1)
            
    def test_bad_acrostic2(self):
        word ="F.A.C.E"
        wordList = wordlist_to_worddict(self.wordlist_small)
        with self.assertRaises(SystemExit) as cm, contextlib.redirect_stderr(find_acrostic(word, wordList)):
            self.assertEqual(cm.exception.code, 1)
            
if __name__ == "__main__":
    test_cases = [
        TestGenerateAcrostic,
    ]
    suites = [unittest.TestLoader().loadTestsFromTestCase(test_case) for test_case in test_cases]
    unittest.TextTestRunner(verbosity=2, buffer=True).run(unittest.TestSuite(suites))
