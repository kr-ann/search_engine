"""

Contains test for for the create_db_index method in the
my_indexer_combined module.

"""

import unittest
import my_indexer_combined
import os
import shelve

class IndexerTests(unittest.TestCase):
    """
    The tests.
    """

    def test_1(self):
        """
        Tests how indexer works for one regular file with regular strings.
        """
        ind = my_indexer_combined.Indexer()
        file = open("file1.txt","w")
        file.write("19 Этот файл содержит несколько строк,\rчтобы мы могли искать токены в файл_ах,\rа еще здесь должны быть повторяющиеся\rтокены и еще повторяющиеся цифры:\r19 19\rи еще здесь: 19")
        file.close()
        
        ind.create_db_index('test_db','file1.txt')
        ideal = {'19': {'file1.txt': [my_indexer_combined.File_Position(1,2,1),
                                      my_indexer_combined.File_Position(1,2,5),
                                      my_indexer_combined.File_Position(4,5,5),
                                      my_indexer_combined.File_Position(14,15,6)]},
                 'Этот': {'file1.txt': [my_indexer_combined.File_Position(4,7,1)]},
                 'файл': {'file1.txt': [my_indexer_combined.File_Position(9,12,1),
                                        my_indexer_combined.File_Position(32,35,2)]},
                 'содержит': {'file1.txt': [my_indexer_combined.File_Position(14,21,1)]},
                 'несколько': {'file1.txt': [my_indexer_combined.File_Position(23,31,1)]},
                 'строк': {'file1.txt': [my_indexer_combined.File_Position(33,37,1)]},
                 'чтобы': {'file1.txt': [my_indexer_combined.File_Position(1,5,2)]},
                 'мы': {'file1.txt': [my_indexer_combined.File_Position(7,8,2)]},
                 'могли': {'file1.txt': [my_indexer_combined.File_Position(10,14,2)]},
                 'искать': {'file1.txt': [my_indexer_combined.File_Position(16,21,2)]},
                 'токены': {'file1.txt': [my_indexer_combined.File_Position(23,28,2),
                                          my_indexer_combined.File_Position(1,6,4)]},
                 'в': {'file1.txt': [my_indexer_combined.File_Position(30,30,2)]},
                 'ах': {'file1.txt': [my_indexer_combined.File_Position(37,38,2)]},
                 'а': {'file1.txt': [my_indexer_combined.File_Position(1,1,3)]},
                 'еще': {'file1.txt': [my_indexer_combined.File_Position(3,5,3),
                                       my_indexer_combined.File_Position(10,12,4),
                                       my_indexer_combined.File_Position(3,5,6)]},
                 'здесь': {'file1.txt': [my_indexer_combined.File_Position(7,11,3),
                                         my_indexer_combined.File_Position(7,11,6)]},
                 'должны': {'file1.txt': [my_indexer_combined.File_Position(13,18,3)]},
                 'быть': {'file1.txt': [my_indexer_combined.File_Position(20,23,3)]},
                 'повторяющиеся': {'file1.txt': [my_indexer_combined.File_Position(25,37,3),
                                                 my_indexer_combined.File_Position(14,26,4)]},
                 'и': {'file1.txt': [my_indexer_combined.File_Position(8,8,4),
                                     my_indexer_combined.File_Position(1,1,6)]},
                 'цифры': {'file1.txt': [my_indexer_combined.File_Position(28,32,4)]}}
        db = shelve.open("test_db")
        self.assertEqual(dict(db),ideal)
        db.close()
        os.remove("file1.txt")
        os.remove("test_db.bak")
        os.remove("test_db.dat")
        os.remove("test_db.dir")

    def test_2(self):
        """
        Tests how indexer works for two regular files with regular strings.
        """
        ind = my_indexer_combined.Indexer()
        
        file = open("file1.txt","w")
        file.write("19 Этот файл содержит несколько строк,\rчтобы мы могли искать токены в файл_ах,\rа еще здесь должны быть повторяющиеся\rтокены и еще повторяющиеся цифры:\r19 19\rи еще здесь: 19")
        file.close()

        file = open("file2.txt","w")
        file.write("другие слова и другие токены,\rа также цифры 19 и еще что-то\r19")
        file.close()
        
        ind.create_db_index('test_db','file1.txt')
        ind.create_db_index('test_db','file2.txt')
        
        ideal = {'19': {'file1.txt': [my_indexer_combined.File_Position(1,2,1),
                                  my_indexer_combined.File_Position(1,2,5),
                                  my_indexer_combined.File_Position(4,5,5),
                                  my_indexer_combined.File_Position(14,15,6)],
                'file2.txt': [my_indexer_combined.File_Position(15,16,2),
                                my_indexer_combined.File_Position(1,2,3)]},
        'Этот': {'file1.txt': [my_indexer_combined.File_Position(4,7,1)]},
        'файл': {'file1.txt': [my_indexer_combined.File_Position(9,12,1),
                                my_indexer_combined.File_Position(32,35,2)]},
        'содержит': {'file1.txt': [my_indexer_combined.File_Position(14,21,1)]},
        'несколько': {'file1.txt': [my_indexer_combined.File_Position(23,31,1)]},
        'строк': {'file1.txt': [my_indexer_combined.File_Position(33,37,1)]},
        'чтобы': {'file1.txt': [my_indexer_combined.File_Position(1,5,2)]},
        'мы': {'file1.txt': [my_indexer_combined.File_Position(7,8,2)]},
        'могли': {'file1.txt': [my_indexer_combined.File_Position(10,14,2)]},
        'искать': {'file1.txt': [my_indexer_combined.File_Position(16,21,2)]},
        'токены': {'file1.txt': [my_indexer_combined.File_Position(23,28,2),
                                    my_indexer_combined.File_Position(1,6,4)],
                    'file2.txt': [my_indexer_combined.File_Position(23,28,1)]},
         'в': {'file1.txt': [my_indexer_combined.File_Position(30,30,2)]},
         'ах': {'file1.txt': [my_indexer_combined.File_Position(37,38,2)]},
         'а': {'file1.txt': [my_indexer_combined.File_Position(1,1,3)],
               'file2.txt': [my_indexer_combined.File_Position(1,1,2)]},
         'еще': {'file1.txt': [my_indexer_combined.File_Position(3,5,3),
                                my_indexer_combined.File_Position(10,12,4),
                                my_indexer_combined.File_Position(3,5,6)],
                 'file2.txt': [my_indexer_combined.File_Position(20,22,2)]},
         'здесь': {'file1.txt': [my_indexer_combined.File_Position(7,11,3),
                                my_indexer_combined.File_Position(7,11,6)]},
         'должны': {'file1.txt': [my_indexer_combined.File_Position(13,18,3)]},
         'быть': {'file1.txt': [my_indexer_combined.File_Position(20,23,3)]},
         'повторяющиеся': {'file1.txt': [my_indexer_combined.File_Position(25,37,3),
                                        my_indexer_combined.File_Position(14,26,4)]},
         'и': {'file1.txt': [my_indexer_combined.File_Position(8,8,4),
                            my_indexer_combined.File_Position(1,1,6)],
               'file2.txt': [my_indexer_combined.File_Position(14,14,1),
                               my_indexer_combined.File_Position(18,18,2)]},
         'цифры': {'file1.txt': [my_indexer_combined.File_Position(28,32,4)],
                   'file2.txt': [my_indexer_combined.File_Position(9,13,2)]},
         'другие': {'file2.txt': [my_indexer_combined.File_Position(1,6,1),
                                my_indexer_combined.File_Position(16,21,1)]},
         'слова': {'file2.txt': [my_indexer_combined.File_Position(8,12,1)]},
         'также': {'file2.txt': [my_indexer_combined.File_Position(3,7,2)]},
         'что': {'file2.txt': [my_indexer_combined.File_Position(24,26,2)]},
         'то': {'file2.txt': [my_indexer_combined.File_Position(28,29,2)]}}

        db = shelve.open("test_db")
        self.assertEqual(dict(db),ideal)
        db.close()
        os.remove("file1.txt")
        os.remove("file2.txt")
        os.remove("test_db.bak")
        os.remove("test_db.dat")
        os.remove("test_db.dir")

    def test_3(self):
        """
        Tests how indexer works if we give it two same files one after another.
        """
        ind = my_indexer_combined.Indexer()

        file = open("file2.txt","w")
        file.write("другие слова и другие токены,\rа также цифры 19 и еще что-то\r19")
        file.close()
        
        ind.create_db_index('test_db','file2.txt')
        ind.create_db_index('test_db','file2.txt')
        
        ideal = {'19': {'file2.txt':[my_indexer_combined.File_Position(15,16,2),
                                my_indexer_combined.File_Position(1,2,3),
                                my_indexer_combined.File_Position(15,16,2),
                                my_indexer_combined.File_Position(1,2,3)]},
         'токены': {'file2.txt':[my_indexer_combined.File_Position(23,28,1),
                                 my_indexer_combined.File_Position(23,28,1)]},
         'а': {'file2.txt': [my_indexer_combined.File_Position(1,1,2),
                             my_indexer_combined.File_Position(1,1,2)]},
         'еще': {'file2.txt': [my_indexer_combined.File_Position(20,22,2),
                               my_indexer_combined.File_Position(20,22,2)]},
         'и': {'file2.txt': [my_indexer_combined.File_Position(14,14,1),
                             my_indexer_combined.File_Position(18,18,2),
                             my_indexer_combined.File_Position(14,14,1),
                             my_indexer_combined.File_Position(18,18,2)]},
         'цифры': {'file2.txt': [my_indexer_combined.File_Position(9,13,2),
                                 my_indexer_combined.File_Position(9,13,2)]},
         'другие': {'file2.txt': [my_indexer_combined.File_Position(1,6,1),
                                  my_indexer_combined.File_Position(16,21,1),
                                  my_indexer_combined.File_Position(1,6,1),
                                  my_indexer_combined.File_Position(16,21,1)]},
         'слова': {'file2.txt': [my_indexer_combined.File_Position(8,12,1),
                                 my_indexer_combined.File_Position(8,12,1)]},
         'также': {'file2.txt': [my_indexer_combined.File_Position(3,7,2),
                                 my_indexer_combined.File_Position(3,7,2)]},
         'что': {'file2.txt': [my_indexer_combined.File_Position(24,26,2),
                               my_indexer_combined.File_Position(24,26,2)]},
         'то': {'file2.txt': [my_indexer_combined.File_Position(28,29,2),
                              my_indexer_combined.File_Position(28,29,2)]}}

        db = shelve.open("test_db")
        self.assertEqual(dict(db),ideal)
        db.close()
        os.remove("file2.txt")
        os.remove("test_db.bak")
        os.remove("test_db.dat")
        os.remove("test_db.dir")

    def test_4(self):
        """
        Tests how indexer works for an empty file.
        """
        ind = my_indexer_combined.Indexer()

        file = open("empty.txt","w")
        file.write("")
        file.close()
        
        ind.create_db_index('test_db','empty.txt')

        db = shelve.open("test_db")
        self.assertEqual(dict(db),{})
        db.close()
        os.remove("empty.txt")
        os.remove("test_db.bak")
        os.remove("test_db.dat")
        os.remove("test_db.dir")

if __name__ == '__main__': # joins all the tests and runs them
    unittest.main()
