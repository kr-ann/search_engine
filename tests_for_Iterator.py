"""

Tests for the 'abstract_iterator'.

"""
import abstract_iterator as it
import unittest

class TheTests(unittest.TestCase):
    def test_1(self):
        first = [1,2,3,4]
        second = [5,6,7]
        third = [8,9,10,11,12]
        ideal = [1,2,3,4,5,6,7,8,9,10,11,12]

        result_1 = list(it.abstract_iterator([first,second,third]))
        result_2 = list(it.abstract_iterator([third,first,second]))

        self.assertEqual(result_1,ideal)
        self.assertEqual(result_2,ideal)

        result_3 = []
        with self.assertRaises(TypeError):
            # not iterable as an input (outer "list")
            for element in it.abstract_iterator(4):
                result_3.append(element)

        result_4 = []
        with self.assertRaises(TypeError):
            # not iterable as an input (inner "lists")
            for element in it.abstract_iterator([1,2,3,4]):
                result_4.append(element)
            
            
    def test_2(self):
        first = [2,6,9,15,100]
        second = [3,10,12,16]
        third = [0,1,2,15,99]
        ideal = [0,1,2,2,3,6,9,10,12,15,15,16,99,100]

        result_1 = list(it.abstract_iterator([first,second,third]))
        result_2 = list(it.abstract_iterator([third,first,second]))

        self.assertEqual(result_1,ideal)
        self.assertEqual(result_2,ideal)

    def test_3(self):
        first = [0,0]
        second = [0,0,0]
        third = [0,0,0,0]
        ideal = [0,0,0,0,0,0,0,0,0]
        
        result_1 = list(it.abstract_iterator([first,second,third]))
        result_2 = list(it.abstract_iterator([third,first,second]))

        self.assertEqual(result_1,ideal)
        self.assertEqual(result_2,ideal)
        
    def test_4(self):
        first = [1]
        second = [2]
        third = [3]
        ideal = [1,2,3]
        
        result_1 = list(it.abstract_iterator([first,second,third]))
        result_2 = list(it.abstract_iterator([third,first,second]))
            
        self.assertEqual(result_1,ideal)
        self.assertEqual(result_2,ideal)


if __name__ == '__main__': 
    unittest.main()
