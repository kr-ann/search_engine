"""

Contains test for 1) the 'advanced_tokenize' method (previously 'tokenize')
and for 2) the 'iter_tokenize' methodin 'my_tokenizer_combined' module
(previously 'my_tokenizer3').


"""

import unittest
import my_tokenizer_combined

class TokenizerTests(unittest.TestCase):
    """
    The tests.
    """

    #tests for a method tokenize
    def test_1(self):
        """
        Tests how tokenizer works for a regular string with all types of tokens.
        """
        t = my_tokenizer_combined.Tokenizer()
        result = t.advanced_tokenize("a string: 12,$,3")
        self.assertEqual(len(result), 10)
        self.assertEqual(result[0].word, "a")
        self.assertEqual(result[0].kind, "alpha")
        self.assertEqual(result[1].word, " ")
        self.assertEqual(result[1].kind, "space")
        self.assertEqual(result[1].length, 1)
        self.assertEqual(result[3].word, ":")
        self.assertEqual(result[3].kind, "punct")
        self.assertEqual(result[3].length, 1)
        self.assertEqual(result[5].word, "12")
        self.assertEqual(result[5].kind, "digit")
        self.assertEqual(result[5].length, 2)
        self.assertEqual(result[7].word, "$")
        self.assertEqual(result[7].kind, "other")
        self.assertEqual(result[7].length, 1)

        self.assertIsInstance(result[0], my_tokenizer_combined.Advanced_Token)
        self.assertIsInstance(result[1], my_tokenizer_combined.Advanced_Token)
        self.assertIsInstance(result[3], my_tokenizer_combined.Advanced_Token)
        self.assertIsInstance(result[5], my_tokenizer_combined.Advanced_Token)
        self.assertIsInstance(result[7], my_tokenizer_combined.Advanced_Token)

    def test_2(self):
        """
        For a string that starts and (=or) ends with a space.
        """
        t = my_tokenizer_combined.Tokenizer()
        result = t.advanced_tokenize("  some string with spaces ")
        self.assertEqual(len(result), 9)
        self.assertEqual(result[0].word, "  ")
        self.assertEqual(result[0].length, 2)
        self.assertEqual(result[0].kind, "space")
        self.assertEqual(result[1].word, "some")
        self.assertEqual(result[1].kind, "alpha")
        self.assertEqual(result[8].word, " ")
        self.assertEqual(result[8].length, 1)
        self.assertEqual(result[8].kind, "space")

    def test_3(self):
        """
        For a string that starts and (=or) ends with a digit.
        """
        t = my_tokenizer_combined.Tokenizer()
        result = t.advanced_tokenize("1 some string with digits 5")
        self.assertEqual(len(result), 11)
        self.assertEqual(result[0].word, "1")
        self.assertEqual(result[0].length, 1)
        self.assertEqual(result[0].kind, "digit")
        self.assertEqual(result[2].word, "some")
        self.assertEqual(result[2].kind, "alpha")
        self.assertEqual(result[10].word, "5")
        self.assertEqual(result[10].length, 1)
        self.assertEqual(result[10].kind, "digit")

    def test_4(self):
        """
        For a string that starts and (=or) ends with a punctuation mark.
        """
        t = my_tokenizer_combined.Tokenizer()
        result = t.advanced_tokenize("_some string with punctuation_")
        self.assertEqual(len(result), 9)
        self.assertEqual(result[0].word, "_")
        self.assertEqual(result[0].length, 1)
        self.assertEqual(result[0].kind, "punct")
        self.assertEqual(result[1].word, "some")
        self.assertEqual(result[1].kind, "alpha")
        self.assertEqual(result[2].word, " ")
        self.assertEqual(result[2].length, 1)
        self.assertEqual(result[2].kind, "space")
        self.assertEqual(result[8].word, "_")
        self.assertEqual(result[8].length, 1)
        self.assertEqual(result[8].kind, "punct")

    def test_5(self):
        """
        For a string that starts and (=or) ends with an "other" unicode symbol.
        """
        t = my_tokenizer_combined.Tokenizer()
        result = t.advanced_tokenize("$some string with \"other\" symols$")
        self.assertEqual(len(result), 13)
        self.assertEqual(result[0].word, "$")
        self.assertEqual(result[0].length, 1)
        self.assertEqual(result[0].kind, "other")
        self.assertEqual(result[1].word, "some")
        self.assertEqual(result[1].kind, "alpha")
        self.assertEqual(result[2].word, " ")
        self.assertEqual(result[2].length, 1)
        self.assertEqual(result[2].kind, "space")
        self.assertEqual(result[12].word, "$")
        self.assertEqual(result[12].length, 1)
        self.assertEqual(result[12].kind, "other")

    def test_6(self):
        """
        For only one punctuation mark as an input string.
        """
        t = my_tokenizer_combined.Tokenizer()
        result = t.advanced_tokenize("!")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].word, "!")
        self.assertEqual(result[0].start, 1)
        self.assertEqual(result[0].end, 1)
        self.assertEqual(result[0].length, 1)
        self.assertEqual(result[0].kind, "punct")
        self.assertIsInstance(result[0], my_tokenizer_combined.Advanced_Token)
        
    def test_7(self):
        """
        For only one aplha-token as an input string.
        """
        t = my_tokenizer_combined.Tokenizer()
        result = t.advanced_tokenize("слово")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].word, "слово")
        self.assertEqual(result[0].start, 1)
        self.assertEqual(result[0].end, 5)
        self.assertEqual(result[0].length, 5)
        self.assertEqual(result[0].kind, "alpha")
        self.assertIsInstance(result[0], my_tokenizer_combined.Advanced_Token)

    def test_8(self):
        """
        For only one space-token as an input string.
        """
        t = my_tokenizer_combined.Tokenizer()
        result = t.advanced_tokenize(" ")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].word, " ")
        self.assertEqual(result[0].start, 1)
        self.assertEqual(result[0].end, 1)
        self.assertEqual(result[0].length, 1)
        self.assertEqual(result[0].kind, "space")
        self.assertIsInstance(result[0], my_tokenizer_combined.Advanced_Token)

    def test_9(self):
        """
        For only one digit-token as an input string.
        """
        t = my_tokenizer_combined.Tokenizer()
        result = t.advanced_tokenize("1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].word, "1")
        self.assertEqual(result[0].start, 1)
        self.assertEqual(result[0].end, 1)
        self.assertEqual(result[0].length, 1)
        self.assertEqual(result[0].kind, "digit")
        self.assertIsInstance(result[0], my_tokenizer_combined.Advanced_Token)

    def test_10(self):
        """
        For only one "other" unicode symbol as an input string.
        """
        t = my_tokenizer_combined.Tokenizer()
        result = t.advanced_tokenize("$")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].word, "$")
        self.assertEqual(result[0].start, 1)
        self.assertEqual(result[0].end, 1)
        self.assertEqual(result[0].length, 1)
        self.assertEqual(result[0].kind, "other")
        self.assertIsInstance(result[0], my_tokenizer_combined.Advanced_Token)

    def test_11(self):
        """
        For an empty string.
        """
        t = my_tokenizer_combined.Tokenizer()
        result = t.advanced_tokenize("")
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

    def test_12(self):
        """
        For a non-string (integer) object as an input.
        """
        t = my_tokenizer_combined.Tokenizer()
        with self.assertRaises(ValueError):
            t.advanced_tokenize(5)

    # tests for a generator iter_tokenize - here's only one, cause
    # they are almost the same as all the tests for the method
    def test_13(self):
        """
        Tests how generator tokenizer works for a regular string with
        all types of tokens.
        """
        t = my_tokenizer_combined.Tokenizer()
        result = list(t.iter_tokenize("a string: 12,$,3"))
        self.assertEqual(len(result), 10)
        self.assertEqual(result[0].word, "a")
        self.assertEqual(result[0].kind, "alpha")
        self.assertEqual(result[1].word, " ")
        self.assertEqual(result[1].kind, "space")
        self.assertEqual(result[1].length, 1)
        self.assertEqual(result[3].word, ":")
        self.assertEqual(result[3].kind, "punct")
        self.assertEqual(result[3].length, 1)
        self.assertEqual(result[5].word, "12")
        self.assertEqual(result[5].kind, "digit")
        self.assertEqual(result[5].length, 2)
        self.assertEqual(result[7].word, "$")
        self.assertEqual(result[7].kind, "other")
        self.assertEqual(result[7].length, 1)

        self.assertIsInstance(result[0], my_tokenizer_combined.Advanced_Token)
        self.assertIsInstance(result[1], my_tokenizer_combined.Advanced_Token)
        self.assertIsInstance(result[3], my_tokenizer_combined.Advanced_Token)
        self.assertIsInstance(result[5], my_tokenizer_combined.Advanced_Token)
        self.assertIsInstance(result[7], my_tokenizer_combined.Advanced_Token)
        
if __name__ == '__main__': # joins all the tests and runs them
    unittest.main()
