import argparse
import io
import sys
import unittest
import unittest.mock as mock

from xkcd_phrase import xkcd_phrase
from xkcd_phrase.lib.xkcd_default import SPECIAL_CHARS

test_list = "tests/test_files/test_list"

class TestEmitPasswords(unittest.TestCase):
    """
    Test cases for function `emit_passwords`.
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
            valid_chars="[a-z]"
        )

        self.options = argparse.Namespace(
            interactive=False,
            num_words=6,
            acrostic=False,
            count=1,
            delimiter="",
            valid_chars="[a-z]",
            valid_delim=list(SPECIAL_CHARS.values()),
            separator="\n",
            numeric_char_num=2,
            numeric_char_append=True,
            special_char_num=2,
            special_char_append=False,
            case="lower",
            verbose=None,
            testing=False,
        )

        self.stdout_patcher = mock.patch.object(sys, "stdout", new_callable=io.StringIO)

    def test_emits_specified_count_of_passwords(self) -> None:
        """
        Should emit passwords numbering specified `count`.
        """
        self.options.count = 6
        with self.stdout_patcher as mock_stdout:
            xkcd_phrase.emit_phrase(wordlist=self.wordlist_small, options=self.options)
        output = mock_stdout.getvalue()
        expected_separator = self.options.separator
        expected_separator_count = self.options.count
        self.assertEqual(output.count(expected_separator), expected_separator_count)

    def test_emits_specified_separator_between_passwords(self) -> None:
        """
        Should emit specified separator text between each password.
        """
        self.options.count = 3
        self.options.separator = "!@#$%"
        with self.stdout_patcher as mock_stdout:
            xkcd_phrase.emit_phrase(wordlist=self.wordlist_small, options=self.options)
        output = mock_stdout.getvalue()
        expected_separator = self.options.separator
        expected_separator_count = self.options.count
        self.assertEqual(output.count(expected_separator), expected_separator_count)

    def test_emits_no_separator_when_specified_separator_empty(self) -> None:
        """
        Should emit no separator when empty separator specified.
        """
        self.options.count = 1
        self.options.separator = ""
        with self.stdout_patcher as mock_stdout:
            xkcd_phrase.emit_phrase(wordlist=self.wordlist_small, options=self.options)
        output = mock_stdout.getvalue()
        unwanted_separator = "\n"
        self.assertEqual(output.find(unwanted_separator), -1)

    def test_emits_no_digits_when_no_padding_digits_is_true(self) -> None:
        """
        Should emit no digits when numeric_char_num is 0.
        """
        self.options.numeric_char_num = 0
        with self.stdout_patcher as mock_stdout:
            xkcd_phrase.emit_phrase(wordlist=self.wordlist_small, options=self.options)
        output = mock_stdout.getvalue()
        self.assertEqual(any(map(str.isdigit, output)), False)

if __name__ == "__main__":
    test_cases = [
        TestEmitPasswords,
    ]
    suites = [unittest.TestLoader().loadTestsFromTestCase(test_case) for test_case in test_cases]
    unittest.TextTestRunner(verbosity=2, buffer=True).run(unittest.TestSuite(suites))
