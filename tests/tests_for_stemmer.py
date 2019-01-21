"""

Tests for the stemmer.

"""
import stemmer
import unittest

class TheTests(unittest.TestCase):
    def test_1(self):
        """ For the simplest stemmer. """

        max_flexion_len = 3

        result_1 = list(stemmer.gen_simplest_stemmer("слово", max_flexion_len))
        ideal_1 = ['слово', 'слов', 'сло', 'сл']
        
        self.assertEqual(result_1,ideal_1)

        with self.assertRaises(ValueError):
            # if the input is an empty string
            result = list(stemmer.gen_simplest_stemmer("", max_flexion_len))
        with self.assertRaises(ValueError):
            # if the input is not a string
            result = list(stemmer.gen_simplest_stemmer(5, max_flexion_len))

        result_2 = list(stemmer.gen_simplest_stemmer("дуб", max_flexion_len))
        ideal_2 = ["дуб"]
        # check that if a word is short we don't stem it
        self.assertEqual(result_2,ideal_2)

        result_3 = list(stemmer.gen_simplest_stemmer("мама", max_flexion_len))
        ideal_3 = ['мама', 'мам', 'ма', 'м']
        self.assertEqual(result_3,ideal_3)

            
    def test_2(self):
        """ For the stemmer in the Flections_Stemmer class. """
        
        flexions = ['', 'а', 'ы', 'о', 'ой', 'ами', 'у', 'е', 'и', 'ей']
        stemmer_obj = stemmer.Flections_Stemmer(flexions)

        with self.assertRaises(ValueError):
            # if the input is an empty string
            result = list(stemmer_obj.gen_stemmer(""))
        with self.assertRaises(ValueError):
            # if the input is not a string
            result = list(stemmer_obj.gen_stemmer(5))

        result_1 = list(stemmer_obj.gen_stemmer("дуб"))
        ideal_1 = ["дуб"]
        # check that if a word is short we don't stem it
        self.assertEqual(result_1,ideal_1)

        result_3 = list(stemmer_obj.gen_stemmer("мамами"))
        ideal_3 = ['мамами', 'мамам', 'мам']
        self.assertEqual(result_3,ideal_3)
        
        result_2 = list(stemmer_obj.gen_stemmer("мама"))
        ideal_2 = ['мама', 'мам']
        self.assertEqual(result_2,ideal_2)


    # the following tests are for the third stemmer
    def test_3:
        ### CODE CODE CODE ###


if __name__ == '__main__': 
    unittest.main()
