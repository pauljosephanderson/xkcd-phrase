import argparse
import io
import sys
import unittest
import unittest.mock as mock

from xkcd_phrase import xkcd_phrase
from xkcd_phrase.lib.xkcd_default import DEFAULT_WORDFILE

class TestEntropy(unittest.TestCase):
    """
    Test cases for function `main`.
    """

    def shortDescription(self) -> None:
        return None

    def setUp(self) -> None:
        """
        Set up fixtures for this test case.
        """
        self.wordlist = xkcd_phrase.generate_wordlist(
            wordfile=DEFAULT_WORDFILE, 
            min_length=6,
            max_length=6,
            valid_chars="[a-z]"
        )
        
        self.wordlist_abcdeg = xkcd_phrase.generate_wordlist(
            wordfile=DEFAULT_WORDFILE, 
            valid_chars="[a-e,g]"
        )

        self.args = [
            "-n=5",
        ]

        self.stdout_patcher = mock.patch.object(sys, "stdout", new_callable=io.StringIO)

    def test_entropy(self) -> None:
        """
        Test help function.
        """
        entropy = False
        
        self.args.append("-V")
        with mock.patch.object(sys, "argv", self.args):
            with self.stdout_patcher as mock_stdout:
                xkcd_phrase.main()
        output = mock_stdout.getvalue()
        print(output)
        search_for = ") = "
        entropy_start = output.rfind(search_for)
        entropy_start += len(search_for)-1
        entropy_sub_str = output.strip()[entropy_start:]
        print(entropy_sub_str)
        entropy_finish = entropy_sub_str.find("\n")
        entropy_val = float(entropy_sub_str.strip()[:entropy_finish])
        
        if isinstance(entropy_val, float):
            entropy = True
            
        self.assertEqual(entropy, True)

    def test_entropy_poss_char_first(self) -> None:
        """
        Test help function.
        """
        entropy = False
        
        self.args.append("-V")
        with mock.patch.object(sys, "argv", self.args):
            with self.stdout_patcher as mock_stdout:
                xkcd_phrase.main()
        output = mock_stdout.getvalue()
#        print(output)
        search_for = "comprising:\n\t"
        entropy_start = output.find(search_for)
        entropy_start += len(search_for)-1
        entropy_sub_str = output.strip()[entropy_start:]
        entropy_finish = entropy_sub_str.find(" alphabetic characters")
        entropy_val = int(entropy_sub_str.strip()[:entropy_finish])
        print(entropy_val)
        
        self.assertEqual(entropy_val, 52)

    def test_entropy_poss_char_lower(self) -> None:
        """
        Test help function.
        """
        entropy = False
        
        self.args.append("-VClower")
        with mock.patch.object(sys, "argv", self.args):
            with self.stdout_patcher as mock_stdout:
                xkcd_phrase.main()
        output = mock_stdout.getvalue()
#        print(output)
        search_for = "comprising:\n\t"
        entropy_start = output.find(search_for)
        entropy_start += len(search_for)-1
        entropy_sub_str = output.strip()[entropy_start:]
        entropy_finish = entropy_sub_str.find(" alphabetic characters")
        entropy_val = int(entropy_sub_str.strip()[:entropy_finish])
        print(entropy_val)
        
        self.assertEqual(entropy_val, 26)

    def test_entropy_poss_char_restricted(self) -> None:
        """
        Test help function.
        """
        entropy = False
        
        self.args.append("-Vv[a-f,g]")
        with mock.patch.object(sys, "argv", self.args):
            with self.stdout_patcher as mock_stdout:
                xkcd_phrase.main()
        output = mock_stdout.getvalue()
#        print(output)
        search_for = "comprising:\n\t"
        entropy_start = output.find(search_for)
        entropy_start += len(search_for)-1
        entropy_sub_str = output.strip()[entropy_start:]
        entropy_finish = entropy_sub_str.find(" alphabetic characters")
        entropy_val = int(entropy_sub_str.strip()[:entropy_finish])
        print(entropy_val)
        
        self.assertEqual(entropy_val, 52)

if __name__ == "__main__":
    test_cases = [
        TestEntropy,
    ]
    suites = [unittest.TestLoader().loadTestsFromTestCase(test_case) for test_case in test_cases]
    unittest.TextTestRunner(verbosity=2, buffer=True).run(unittest.TestSuite(suites))
