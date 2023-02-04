import unittest
import contextlib

from xkcd_phrase import xkcd_phrase
from xkcd_phrase.lib.xkcd_default import DEFAULT_WORDFILE, SPECIAL_CHARS

class TestGenerateSpecialChar(unittest.TestCase):
    """
    Test cases for special Characters.
    """

    def shortDescription(self) -> None:
        return None

    def setUp(self) -> None:
        """
        Set up fixtures for this test case.
        """
        self.wordlist_default = xkcd_phrase.generate_wordlist(
            wordfile=DEFAULT_WORDFILE, 
            min_length=5,
            max_length=9,
            valid_chars="[a-z]"
        )

        self.special_char_test_list = xkcd_phrase.choose_words(self.wordlist_default, 
            num_words = 5,
            acrostic = False
        )

    """
    Test whether Special Characters are coming through at all
    """
    def test_good_special(self):
        special_count = 0
        num_words = 5
        special_char_num = 2
        delimiter = " "
        valid_delim=list(SPECIAL_CHARS.values())

        result = xkcd_phrase.special_char_sub(self.special_char_test_list,
            num_words,
            special_char_num,
            delimiter,
            valid_delim
            )

        for i in range(num_words):
            if not result[i].isalnum():
                special_count +=1
        
        self.assertGreater(special_count, 0)
            
    """
    Test whether the number of Special Characters specified
    are coming through 
    """
    def test_special_char_num(self):
        special_count = 0
        num_words = 5
        special_char_num = 2

        result = xkcd_phrase.special_char_sub(self.special_char_test_list, 
            num_words, 
            special_char_num,
            delimiter = " ",
            valid_delim=list(SPECIAL_CHARS.values()),
            )
        
        for i in range(num_words):
            if not result[i].isalnum():
                special_count +=1
        
        self.assertEqual(special_count, special_char_num)
                      
if __name__ == "__main__":
    test_cases = [
        TestGenerateSpecialChar,
    ]
    suites = [unittest.TestLoader().loadTestsFromTestCase(test_case) for test_case in test_cases]
    unittest.TextTestRunner(verbosity=2, buffer=True).run(unittest.TestSuite(suites))
