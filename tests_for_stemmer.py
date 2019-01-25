"""

Tests for the stemmer.

"""
import stemmer
import unittest
import shelve

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
        
        flexions = ['', 'а', 'ы', 'о', 'ой', 'ами', 'у', 'е', 'и', 'ей', 'для_проверки', 'и_ещё']
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

        result_2 = list(stemmer_obj.gen_stemmer("мама"))
        ideal_2 = ['мам']
        self.assertEqual(result_2,ideal_2)
        
        result_3 = list(stemmer_obj.gen_stemmer("мамами"))
        ideal_3 = ['мамам', 'мам']
        self.assertEqual(result_3,ideal_3)
        
        result_4 = list(stemmer_obj.gen_stemmer("это_для_проверки"))
        ideal_4 = ['это_для_проверк','это_']
        self.assertEqual(result_4,ideal_4)

        result_5 = list(stemmer_obj.gen_stemmer("и_ещё"))
        ideal_5 = []
        self.assertEqual(result_5,ideal_5)

        del stemmer_obj


    def test_3(self):
        """ For the BD_Stemmer. """
        
        stems_bd = shelve.open('C:\\Users\\boss\\Documents\\Python Scripts\\Search\\bd_stems')
        flections_bd = shelve.open('C:\\Users\\boss\\Documents\\Python Scripts\\Search\\bd_flections')

        stemmer_obj = stemmer.BD_Stemmer(stems_bd, flections_bd)

        result_1 = list(stemmer_obj.gen_stemmer("друзьями"))
        ideal_1 = ['друз']
        self.assertEqual(result_1,ideal_1)

        result_2 = list(stemmer_obj.gen_stemmer("другями"))
        ideal_2 = []
        self.assertEqual(result_2,ideal_2)
        
        stems_bd.close()
        flections_bd.close()
        del stemmer_obj
    
    def test_4(self):
        """ For lemmatization in BD_Stemmer. """
        
        stems_bd = shelve.open('C:\\Users\\boss\\Documents\\Python Scripts\\Search\\bd_stems')
        flections_bd = shelve.open('C:\\Users\\boss\\Documents\\Python Scripts\\Search\\bd_flections')

        stemmer_obj = stemmer.BD_Stemmer(stems_bd, flections_bd)

        result_1 = list(stemmer_obj.gen_stemmer("друзьями", lemmatisation=True))
        ideal_1 = ['друг']
        self.assertEqual(ideal_1,result_1)

        result_2 = list(stemmer_obj.gen_stemmer("другями", lemmatisation=True))
        ideal_2 = []
        self.assertEqual(result_2,ideal_2)

        result_3 = list(stemmer_obj.gen_stemmer("листочком", lemmatisation=True))
        ideal_3 = ['листочек']
        self.assertEqual(result_3,ideal_3)

        
        stems_bd.close()
        flections_bd.close()
        del stemmer_obj

    def test_5(self):
        """ For the Final_Stemmer that controls the three previous ones. """

        stemmer_obj = stemmer.Final_Stemmer('bd_stems', 'bd_flections')

        result_1 = list(stemmer_obj.decide_and_return('друзьями'))
        ideal_1 = ['друз']
        self.assertEqual(result_1,ideal_1)

        result_2 = list(stemmer_obj.decide_and_return('другями'))
        ideal_2 = ['другям', 'друг']
        self.assertEqual(result_2,ideal_2)

        result_3 = list(stemmer_obj.decide_and_return('fdgdfh'))
        ideal_3 = ['fdgdfh', 'fdgdf', 'fdgd', 'fdg']
        self.assertEqual(result_3,ideal_3)
        
        del stemmer_obj


if __name__ == '__main__': 
    unittest.main()
