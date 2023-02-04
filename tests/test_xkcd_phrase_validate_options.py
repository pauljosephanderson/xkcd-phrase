import argparse
import io
import os
import sys
import unittest
import unittest.mock as mock

from xkcd_phrase import xkcd_phrase
from xkcd_phrase.lib.xkcd_default import (
    DEFAULT_WORDFILE,
    VALID_CHARS,
    SPECIAL_CHARS
)

test_list = "tests/test_files/test_list"

class TestValidateOptions(unittest.TestCase):
    """
    Test cases for function `validate_options`.
    """

    def shortDescription(self) -> None:
        return None

    def setUp(self) -> None:
        """
        Set up fixtures for this test case.
        """
        self.wordlist_small = xkcd_phrase.generate_wordlist(
            wordfile=test_list, 
            min_length=5,
            max_length=9,
            valid_chars=VALID_CHARS
        )

        self.options_incorrect_min_length = argparse.Namespace(
            wordfile=test_list, 
            min_length=1,
            max_length=6,
            num_words = 4,
            acrostic = False,
            numeric_char_num = 2,
            numeric_char_append = False,
            special_char_num = 2,
            special_char_append = False,
            no_special_char = False,
            delimiter = " ",
            valid_delim=list(SPECIAL_CHARS.values()),
            valid_chars=VALID_CHARS,
            count = 1,
        )

        self.options_incorrect_max_length = argparse.Namespace(
            wordfile=test_list, 
            min_length=7,
            max_length=6,
            num_words = 4,
            acrostic = False,
            numeric_char_num = 2,
            numeric_char_append = False,
            special_char_num = 2,
            special_char_append = False,
            no_special_char = False,
            delimiter = " ",
            valid_delim=list(SPECIAL_CHARS.values()),
            valid_chars=VALID_CHARS,
            count = 1,
        )

        self.options_low_numwords = argparse.Namespace(
            wordfile=test_list, 
            min_length=1,
            max_length=6,
            num_words = -12,
            acrostic = False,
            numeric_char_num = 2,
            numeric_char_append = False,
            special_char_num = 2,
            special_char_append = False,
            no_special_char = False,
            delimiter = " ",
            valid_delim=list(SPECIAL_CHARS.values()),
            valid_chars=VALID_CHARS,
            count = 1,
        )

        self.options_low_word_count = argparse.Namespace(
            wordfile=test_list, 
            min_length=1,
            max_length=6,
            num_words = 4,
            acrostic = False,
            numeric_char_num = 2,
            numeric_char_append = False,
            special_char_num = 2,
            special_char_append = False,
            no_special_char = False,
            delimiter = " ",
            valid_delim=list(SPECIAL_CHARS.values()),
            valid_chars=VALID_CHARS,
            count = -2,
        )

        self.options_delimiter = argparse.Namespace(
            wordfile=test_list, 
            min_length=1,
            max_length=6,
            num_words = 4,
            acrostic = False,
            numeric_char_num = 2,
            numeric_char_append = False,
            special_char_num = 2,
            special_char_append = False,
            no_special_char = False,
            delimiter = "[",
            valid_delim=list(SPECIAL_CHARS.values()),
            valid_chars=VALID_CHARS,
            count = -2,
        )

        self.options_incorrect_wordfile = argparse.Namespace(
            wordfile="test_list2", 
            min_length=7,
            max_length=7,
            num_words = 4,
            acrostic = False,
            numeric_char_num = 2,
            numeric_char_append = False,
            special_char_num = 2,
            special_char_append = False,
            no_special_char = False,
            delimiter = " ",
            valid_chars=VALID_CHARS,
            count = 1,            
        )

        self.options_default_wordfile = argparse.Namespace(
            max_length=7,
            min_length=7,
            num_words = 4,
            acrostic = False,
            numeric_char_num = 2,
            numeric_char_append = False,
            special_char_append = False,
            special_char_num = 2,
            no_special_char = False,
            delimiter = " ",
            valid_delim=list(SPECIAL_CHARS.values()),
            valid_chars=VALID_CHARS,
            count = 1,
            wordfile=None
        )
        
        self.args = [
            "--min=6",
            "--max=6",
            "-n=3",
        ]

        self.stdout_patcher = mock.patch.object(sys, "stdout", new_callable=io.StringIO)

    def test_validate_options_incorrect_min_length(self) -> None:
        """
        Testing validate options incorrect max length.
        """
        with self.stdout_patcher as mock_stdout:
            xkcd_phrase.validate_options(options=self.options_incorrect_min_length)
        output = mock_stdout.getvalue()
        self.assertEqual(len(output.strip()), 85)

    def test_validate_options_incorrect_max_length(self) -> None:
        """
        Testing validate options incorrect max length.
        """
        with self.stdout_patcher as mock_stdout:
            xkcd_phrase.validate_options(options=self.options_incorrect_max_length)
        output = mock_stdout.getvalue()
        self.assertEqual(len(output.strip()), 91)

    def test_validate_options_low_numwords(self) -> None:
        """
        Testing validate options low numwords.
        """
        with self.stdout_patcher as mock_stdout:
            xkcd_phrase.validate_options(options=self.options_low_numwords)
        output = mock_stdout.getvalue()
        self.assertEqual(len(output.strip()), 207)

    def test_validate_options_low_word_count(self) -> None:
        """
        Testing validate options low word count.
        """
        with self.stdout_patcher as mock_stdout:
            xkcd_phrase.validate_options(options=self.options_low_word_count)
        output = mock_stdout.getvalue()
        self.assertEqual(len(output.strip()), 210)

    def test_validate_options_delimiter(self) -> None:
        """
        Testing validate options low word count.
        """
        with self.stdout_patcher as mock_stdout:
            xkcd_phrase.validate_options(options=self.options_delimiter)
        output = mock_stdout.getvalue()
        self.assertEqual(len(output.strip()), 373)

    def test_validate_options_default_char_set(self) -> None:
        """
        Test custom char set.
        """
        #self.args.append("-v 'a-p,t")
        with mock.patch.object(sys, "argv", self.args):
            with self.stdout_patcher as mock_stdout:
                xkcd_phrase.main()
        output = mock_stdout.getvalue()
        print(output)
        self.assertEqual(len(output.strip()), 20)

    def test_validate_options_custom_char_set(self) -> None:
        """
        Test custom char set.
        """
        self.args.append("-va-p")
        with mock.patch.object(sys, "argv", self.args):
            with self.stdout_patcher as mock_stdout:
                xkcd_phrase.main()
        output = mock_stdout.getvalue()
        print(output)
        self.assertEqual(len(output.strip()), 20)

    def test_validate_options_bad_custom_char_set(self) -> None:
        """
        Test custom char set.
        """
        self.args.append("-va")
        with mock.patch.object(sys, "argv", self.args):
            with self.stdout_patcher as mock_stdout:
                xkcd_phrase.main()
        output = mock_stdout.getvalue()
        print(output)
        self.assertEqual(len(output.strip()), 136)


    def test_validate_options_incorrect_wordfile(self) -> None:
        """
        Testing validate options incorrect wordfile.
        """
        with self.stdout_patcher as mock_stdout:
            xkcd_phrase.validate_options(options=self.options_incorrect_wordfile)
        output = mock_stdout.getvalue()
        self.assertEqual(output.strip()[-8:], "eff-long".strip())
        
    def test_validate_options_default_wordfile(self) -> None:
        """
        Testing validate options default_wordfile.
        """
        xkcd_phrase.DEFAULT_WORDFILE = DEFAULT_WORDFILE
        with self.stdout_patcher as mock_stdout:
            xkcd_phrase.validate_options(
                options=self.options_default_wordfile,
                testing=True,
            )
        output = mock_stdout.getvalue()
        self.assertEqual(output.strip()[-8:], "eff-long".strip())


if __name__ == "__main__":
    test_cases = [
        TestValidateOptions,
    ]
    suites = [unittest.TestLoader().loadTestsFromTestCase(test_case) for test_case in test_cases]
    unittest.TextTestRunner(verbosity=2, buffer=True).run(unittest.TestSuite(suites))
