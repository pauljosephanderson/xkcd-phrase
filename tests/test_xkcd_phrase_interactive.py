import argparse
import io
import sys
import unittest
import unittest.mock as mock

from xkcd_phrase import xkcd_phrase
from xkcd_phrase.lib.xkcd_default import DEFAULT_WORDFILE

class TestInteractiveInitialization(unittest.TestCase):
    """
    Test cases for interactive intialization.
    """

    def shortDescription(self) -> None:
        return None

    def setUp(self) -> None:
        """
        Set up fixtures for this test case.
        """
        self.wordlist_full = xkcd_phrase.generate_wordlist(
            wordfile=DEFAULT_WORDFILE,
            min_length=5,
            max_length=8,
            valid_chars="[a-z]"
        )

        self.options = argparse.Namespace(
            interactive=True,
            num_words=6,
            acrostic=False,
            testing=True,
        )

        self.stdout_patcher = mock.patch.object(sys, "stdout", new_callable=io.StringIO)

    def test_interactive_initialization(self) -> None:
        """
        Should test interactive intialization.
        """
        self.options.testtype = "NumWords"
        with self.stdout_patcher as mock_stdout:
            xkcd_phrase.initialize_interactive_run(options=self.options)
        output = mock_stdout.getvalue()
        self.assertEqual(output.strip(), str(2))

    def test_interactive_initialization_default_num_words(self) -> None:
        """
        Should test interactive intialization.
        """
        self.options.testtype = "NumWords0"
        with self.stdout_patcher as mock_stdout:
            xkcd_phrase.initialize_interactive_run(options=self.options)
        output = mock_stdout.getvalue()
        self.assertEqual(output.strip(), str(6))

    def test_interactive_initialization_error(self) -> None:
        """
        Should test interactive intialization.
        """
        self.options.testtype = "NumWordsError"
        with self.assertRaises(SystemExit):
            xkcd_phrase.initialize_interactive_run(options=self.options)


if __name__ == "__main__":
    test_cases = [
        TestInteractiveInitialization,
    ]
    suites = [unittest.TestLoader().loadTestsFromTestCase(test_case) for test_case in test_cases]
    unittest.TextTestRunner(verbosity=2, buffer=True).run(unittest.TestSuite(suites))
