"""

Tests for the 'final_prog_with_limit_offset' method in the 'final_prog' module.
There are no tests for the "incorrect" input (e.g. a char instead of a digit),
because all conditions for raising errors are in the module with server and we
can't check them via tests.

"""

import final_prog
import final_prog_old
import unittest

class TheTests(unittest.TestCase):    
    # @unittest.skip
    # WHAT'S WRONG??
    def test_1(self):
        """
        The result must be as without any limits and offsets.
        """
        db = "war_and_peace"
        query = "князь Андрей"
        win_len = 3
        doc_lim = 4
        doc_off = 0
        lim_off_list = [(1000,0),(1000,0),(1000,0),(1000,0)]
        result = final_prog.Result().final_prog_with_limit_offset(db,query,win_len,doc_lim,doc_off,lim_off_list)
        ideal = final_prog_old.Result().final_prog_from_db(db,query,win_len)
        print(ideal)
        self.assertEqual(result,ideal)

        #windows_dict = engine.get_context_for_words(query,int(window_length),doc_limit,doc_offset)
        #result = engine.make_windows_sentences(windows_dict,lim_off_list)
        
    @unittest.skip
    def test_2(self):
        """
        With limits and offsets for documents.
        """
        db = "war_and_peace"
        query = "князь Андрей"
        win_len = 3
        doc_lim = 1
        doc_off = 2
        lim_off_list = [(100,0)]
        result = final_prog.Result().final_prog_with_limit_offset(db,query,win_len,doc_lim,doc_off,lim_off_list)
        ideal = ""

        self.assertEqual(result,ideal)
        
    @unittest.skip
    def test_3(self):
        """
        With limits and offsets for citations.
        """
        
    @unittest.skip
    def test_4(self):
        """
        With limits and offsets for both documents and citations.
        """

        
if __name__ == '__main__': 
    unittest.main()            
