import io
import sys
import unittest
import unittest.mock as mock

from xkcd_phrase import xkcd_phrase
from xkcd_phrase.lib.xkcd_default import DEFAULT_WORDFILE

test_list = "tests/test_files/test_list"

class TestMain(unittest.TestCase):
    """
    Test cases for function `main`.
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
            "--special-char-num=2"
        ]

        self.stdout_patcher = mock.patch.object(sys, "stdout", new_callable=io.StringIO)

    def test_main(self) -> None:
        """
        Test main function.
        """
        xkcd_phrase.DEFAULT_WORDFILE = test_list
        with mock.patch.object(sys, "argv", self.args):
            with self.stdout_patcher as mock_stdout:
                xkcd_phrase.main()
        output = mock_stdout.getvalue()
        self.assertEqual(len(output.strip()), 20)

    def test_main_help(self) -> None:
        """
        Test help function.
        """
        self.args.append("-h")
        with mock.patch.object(sys, "argv", self.args):
            with self.stdout_patcher as mock_stdout:
                xkcd_phrase.main()
        output = mock_stdout.getvalue()
#        print(output)
        self.assertEqual(len(output.strip()), 3276)

    def test_main_interactive(self) -> None:
        """
        Test main interactive.
        """

        sys.stdin = open("tests/test_files/stdin_main_interactive", "r")

        xkcd_phrase.DEFAULT_WORDFILE = test_list
        self.args.append("-i")
        with mock.patch.object(sys, "argv", self.args):
            with self.stdout_patcher as mock_stdout:
                xkcd_phrase.main()
        output = mock_stdout.getvalue()
        self.assertEqual(len(output.strip()), 134)

    def test_no_special(self) -> None:
        """
        Test --special-char-num=0
        """
        xkcd_phrase.DEFAULT_WORDFILE = test_list
        self.args.append("--special-char-num=0")
        self.args.append("--delimiter=''")
        with mock.patch.object(sys, "argv", self.args):
            with self.stdout_patcher as mock_stdout:
                xkcd_phrase.main()
        output = mock_stdout.getvalue().strip()[-18:].isalnum()
            
        self.assertEqual(output, True)

    def test_special_append(self) -> None:
        """
        Test --special-char-append
        """
        special_count = 0
        i = 0
        xkcd_phrase.DEFAULT_WORDFILE = test_list
        self.args.append("--special-char-append")
        with mock.patch.object(sys, "argv", self.args):
            with self.stdout_patcher as mock_stdout:
                xkcd_phrase.main()
        output = mock_stdout.getvalue().strip()[-2:]
        while i < len(output):
            if not output[i].isalnum():
                special_count +=1
                i+=1
            
        self.assertEqual(special_count, 2)

    def test_main_systemexit(self) -> None:
        """
        Test main interactive error.
        """
        expected_output = "Could not find word file".strip()

        xkcd_phrase.DEFAULT_WORDFILE = "test_list2"
        with mock.patch.object(sys, "argv", self.args):
            with self.stdout_patcher as mock_stdout:
                xkcd_phrase.main()
        output = mock_stdout.getvalue()
        self.assertEqual(output.strip()[:24], expected_output)

        sys.stdin = sys.__stdin__

    xkcd_phrase.DEFAULT_WORDFILE = DEFAULT_WORDFILE


if __name__ == "__main__":
    test_cases = [
        TestMain,
    ]
    suites = [unittest.TestLoader().loadTestsFromTestCase(test_case) for test_case in test_cases]
    unittest.TextTestRunner(verbosity=2, buffer=True).run(unittest.TestSuite(suites))
