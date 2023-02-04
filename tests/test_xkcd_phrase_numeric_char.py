import io
import sys
import unittest
import unittest.mock as mock

from xkcd_phrase import xkcd_phrase
from xkcd_phrase.lib.xkcd_default import DEFAULT_WORDFILE

test_list = "tests/test_files/test_list"

class TestNumericChar(unittest.TestCase):
    """
    Test cases for numeric-char`.
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

        self.args = [
            "--min=6",
            "--max=6",
            "-n=3",
            "--numeric-char-num=2"
        ]

        self.stdout_patcher = mock.patch.object(sys, "stdout", new_callable=io.StringIO)

    def test_numeric_append(self) -> None:
        """
        Test --numeric-char-append
        """
        numeric = False
        xkcd_phrase.DEFAULT_WORDFILE = test_list
        self.args.append("--numeric-char-append")
        with mock.patch.object(sys, "argv", self.args):
            with self.stdout_patcher as mock_stdout:
                xkcd_phrase.main()
        output = mock_stdout.getvalue().strip()[-2:]
            
        self.assertEqual(output.isnumeric(), True)

    def test_no_numeric_char(self) -> None:
        """
        Test --no-numeric-char
        """
        xkcd_phrase.DEFAULT_WORDFILE = test_list
        self.args.append("--numeric-char-num=0")
        with mock.patch.object(sys, "argv", self.args):
            with self.stdout_patcher as mock_stdout:
                xkcd_phrase.main()
        output = ''.join(filter(str.isalnum, mock_stdout.getvalue())).isalpha()
            
        self.assertEqual(output, True)
            
    """
    Test whether the number of Numeric Characters specified
    are coming through 
    """
    def test_numeric_char_num(self) -> None:
        """
        Test --numeric-char-num
        """
        xkcd_phrase.DEFAULT_WORDFILE = test_list
        self.args.append("--numeric-char-num=4")
        self.args.append("--numeric-char-append")
        with mock.patch.object(sys, "argv", self.args):
            with self.stdout_patcher as mock_stdout:
                xkcd_phrase.main()
        output = mock_stdout.getvalue().strip()[-4:]
            
        self.assertEqual(output.isnumeric(), True)
            
                      


if __name__ == "__main__":
    test_cases = [
        TestNumericChar,
    ]
    suites = [unittest.TestLoader().loadTestsFromTestCase(test_case) for test_case in test_cases]
    unittest.TextTestRunner(verbosity=2, buffer=True).run(unittest.TestSuite(suites))
