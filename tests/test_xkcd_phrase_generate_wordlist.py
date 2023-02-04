import unittest

from xkcd_phrase import xkcd_phrase
from xkcd_phrase.lib.xkcd_default import DEFAULT_WORDFILE

class TestGenerateWordlist(unittest.TestCase):
    """
    Test cases for function `generate_wordlist`.
    """

    def shortDescription(self) -> None:
        return None

    def setUp(self) -> None:
        """
        Set up fixtures for this test case.
        """
        test_list = "tests/test_files/test_list"
        
        self.wordlist_full = xkcd_phrase.generate_wordlist(
            wordfile=DEFAULT_WORDFILE,
            min_length=5,
            max_length=8,
            valid_chars="[a-z]"
        )
        self.wordlist_small = xkcd_phrase.generate_wordlist(
            wordfile=test_list, 
            min_length=5,
            max_length=9,
            valid_chars="[a-z]"
        )

        self.wordlist_abcdef = xkcd_phrase.generate_wordlist(
            wordfile=test_list, 
            min_length=5,
            max_length=9,
            valid_chars="[a-f]"
        )

        self.wordlist_abcdeg = xkcd_phrase.generate_wordlist(
            wordfile=test_list, 
            min_length=5,
            max_length=9,
            valid_chars="[a-e,g]"
        )

    def test_loadwordfile(self) -> None:
        """
        Test load wordlist is correct.
        """
        self.assertEqual(len(self.wordlist_full), 5667)

    def test_regex(self) -> None:
        """
        Test regex.
        """
        self.assertNotIn("__$$$__", self.wordlist_small)

    def test_validchar1(self) -> None:
        """
        Test valid_chars
        """
        self.assertEqual(len(self.wordlist_abcdef), 1)

    def test_validchar2(self) -> None:
        """
        Test valid_chars
        """
        self.assertEqual(len(self.wordlist_abcdeg), 1)


if __name__ == "__main__":
    test_cases = [
        TestGenerateWordlist,
    ]
    suites = [unittest.TestLoader().loadTestsFromTestCase(test_case) for test_case in test_cases]
    unittest.TextTestRunner(verbosity=2, buffer=True).run(unittest.TestSuite(suites))
