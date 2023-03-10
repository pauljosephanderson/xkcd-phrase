import unittest

from xkcd_phrase import xkcd_phrase


class TestSetCase(unittest.TestCase):
    """
    Test cases for function `set_case`.
    """

    def shortDescription(self) -> None:
        return None

    def test_set_case(self) -> None:
        """
        Test set_case works correctly.
        """
        words = "this is only a test".lower().split()
        words_before = set(words)

        results = {}

        results["lower"] = xkcd_phrase.set_case(words, method="lower")
        results["upper"] = xkcd_phrase.set_case(words, method="upper")
        results["alternating"] = xkcd_phrase.set_case(words, method="alternating")
        results["random"] = xkcd_phrase.set_case(words, method="random", testing=True)
        results["first"] = xkcd_phrase.set_case(words, method="first")
        results["capitalize"] = xkcd_phrase.set_case(words, method="capitalize")

        words_after = set(word.lower() for group in list(results.values()) for word in group)

        # Test that no words have been fundamentally mutated by any of the methods
        self.assertTrue(words_before == words_after)

        # Test that the words have been uppered or lowered respectively.
        self.assertTrue(all(word.islower() for word in results["lower"]))
        self.assertTrue(all(word.isupper() for word in results["upper"]))
        self.assertTrue(all(word.istitle() for word in results["first"]))
        self.assertTrue(all(word.istitle() for word in results["capitalize"]))
        # Test that the words have been correctly uppered randomly.
        expected_random_result_1_py3 = ["THIS", "IS", "ONLY", "a", "test"]
        expected_random_result_2_py3 = ["THIS", "IS", "a", "test", "ALSO"]
        expected_random_result_1_py2 = ["this", "is", "only", "a", "TEST"]
        expected_random_result_2_py2 = ["this", "is", "a", "TEST", "also"]

        words_extra = "this is a test also".lower().split()
        observed_random_result_1 = results["random"]
        observed_random_result_2 = xkcd_phrase.set_case(words_extra, method="random", testing=True)

        self.assertIn(
            observed_random_result_1,
            (expected_random_result_1_py2, expected_random_result_1_py3),
        )
        self.assertIn(
            observed_random_result_2,
            (expected_random_result_2_py2, expected_random_result_2_py3),
        )


if __name__ == "__main__":
    test_cases = [
        TestSetCase,
    ]
    suites = [unittest.TestLoader().loadTestsFromTestCase(test_case) for test_case in test_cases]
    unittest.TextTestRunner(verbosity=2, buffer=True).run(unittest.TestSuite(suites))
