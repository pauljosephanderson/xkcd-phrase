import sys
import unittest
import unittest.mock as mock

from xkcd_phrase import xkcd_phrase


class TestInit(unittest.TestCase):
    """
    Test cases for function `init`.
    """

    def setUp(self) -> None:
        """
        Set up fixtures for this test case.
        """

        self.args = [
            "--min=6",
            "--max=6",
            "-n=3",
        ]

    def test_init(self) -> None:
        """
        Test init() function.
        """
        with mock.patch.object(sys, "argv", self.args):
            with mock.patch.object(xkcd_phrase, "main", return_value=42):
                with mock.patch.object(xkcd_phrase, "__name__", "__main__"):
                    with mock.patch.object(xkcd_phrase.sys, "exit") as mock_exit:
                        xkcd_phrase.init()
                        assert mock_exit.call_args[0][0] == 42


if __name__ == "__main__":
    test_cases = [
        TestInit,
    ]
    suites = [unittest.TestLoader().loadTestsFromTestCase(test_case) for test_case in test_cases]
    unittest.TextTestRunner(verbosity=2, buffer=True).run(unittest.TestSuite(suites))
