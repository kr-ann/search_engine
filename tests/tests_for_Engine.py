"""

Contains test for the search_engine module.

"""

import unittest
import search_engine
import my_indexer_combined
import os
import shelve

class TheTests(unittest.TestCase):
    """
    The tests.
    """
    
    @unittest.skip
    def test_1(self):
        """
        Tests for the_simplest method.
        """

        # how the search works for one regular file in the db
        
        file = open("file2.txt","w")
        file.write("другие слова и другие токены,\rа также цифры 19 и еще что-то\r19\r")
        file.close()
        ind = my_indexer_combined.Indexer()
        ind.create_db_index('test_db','file2.txt')

        engine = search_engine.Engine("test_db")
        result_1 = engine.the_simplest("19")
        ideal_1 = {'file2.txt': [my_indexer_combined.File_Position(15,16,2),
                                my_indexer_combined.File_Position(1,2,3)]}
        self.assertEqual(result_1, ideal_1)

        # for two regular files in the db

        file = open("file1.txt","w")
        file.write("19 Этот файл содержит несколько строк,\rчтобы мы могли искать токены в файл_ах,\rа еще здесь должны быть повторяющиеся\rтокены и еще повторяющиеся цифры:\r19 19\rи еще здесь: 19\r")
        file.close()
        # file2 is already there
        ind.create_db_index('test_db','file1.txt')
        engine = search_engine.Engine("test_db")
        result_2 = engine.the_simplest("19")
        ideal_2 = {'file1.txt': [my_indexer_combined.File_Position(1,2,1),
                                  my_indexer_combined.File_Position(1,2,5),
                                  my_indexer_combined.File_Position(4,5,5),
                                  my_indexer_combined.File_Position(14,15,6)],
                'file2.txt': [my_indexer_combined.File_Position(15,16,2),
                                my_indexer_combined.File_Position(1,2,3)]}
        self.assertEqual(result_2, ideal_2)

        # for a non-existent token as an input
        result_3 = engine.the_simplest("NotInThere")
        self.assertEqual(result_3,{})

        # for a non-string as an input
        with self.assertRaises(ValueError):
            engine.the_simplest(5)

        del engine
        os.remove("test_db.bak")
        os.remove("test_db.dat")
        os.remove("test_db.dir")
        os.remove("file1.txt")
        os.remove("file2.txt")

        
    @unittest.skip
    def test_2(self):
        """
        Tests how the_second_simplest method works.
        """

        file = open("file1.txt","w")
        file.write("19 Этот файл содержит несколько строк,\rчтобы мы могли искать токены в файл_ах,\rа еще здесь должны быть повторяющиеся\rтокены и еще повторяющиеся цифры:\r19 19\rи еще здесь: 19\r")
        file.close()
        file = open("file2.txt","w")
        file.write("другие слова и другие токены,\rа также цифры 19 и еще что-то\r19\r")
        file.close()
        ind = my_indexer_combined.Indexer()
        ind.create_db_index('test_db','file1.txt')
        ind.create_db_index('test_db','file2.txt')

        engine = search_engine.Engine('test_db')

        # how the search works for several words in a query, each of them
        # occuring in both files in the db
        result_1 = engine.the_second_simplest("19 и еще цифры")
        ideal_1 = {'file1.txt': [my_indexer_combined.File_Position(1,2,1), # sorted
                               my_indexer_combined.File_Position(3,5,3),
                               my_indexer_combined.File_Position(8,8,4),
                               my_indexer_combined.File_Position(10,12,4),
                               my_indexer_combined.File_Position(28,32,4),
                               my_indexer_combined.File_Position(1,2,5),
                               my_indexer_combined.File_Position(4,5,5),
                               my_indexer_combined.File_Position(1,1,6),
                               my_indexer_combined.File_Position(3,5,6),
                               my_indexer_combined.File_Position(14,15,6)                              
                               ],
                'file2.txt': [my_indexer_combined.File_Position(14,14,1),
                              my_indexer_combined.File_Position(9,13,2),
                              my_indexer_combined.File_Position(15,16,2),
                              my_indexer_combined.File_Position(18,18,2),
                              my_indexer_combined.File_Position(20,22,2),
                              my_indexer_combined.File_Position(1,2,3)
                              ]}
        self.assertEqual(result_1, ideal_1)

        # when all words together occur only in one file in the db
        result_2 = engine.the_second_simplest("еще несколько строк")
        ideal_2 = {'file1.txt': [my_indexer_combined.File_Position(23,31,1),
                               my_indexer_combined.File_Position(33,37,1),
                               my_indexer_combined.File_Position(3,5,3),
                               my_indexer_combined.File_Position(10,12,4),
                               my_indexer_combined.File_Position(3,5,6)
                               ]}
        self.assertEqual(result_2, ideal_2)

        # when all words together don't oocur in the same files
        result_3 = engine.the_second_simplest("другие повторяющиеся")
        self.assertEqual(result_3, {})

        # for a non-existent token
        result_4 = engine.the_second_simplest("NotInThere")
        self.assertEqual(result_4,{})

        # for a non-string
        with self.assertRaises(ValueError):
            engine.the_second_simplest(5)

        del engine
        os.remove("test_db.bak")
        os.remove("test_db.dat")
        os.remove("test_db.dir")
        os.remove("file1.txt")
        os.remove("file2.txt")
        
    @unittest.skip 
    def test_3(self):
        """
        How the get_word method works.
        """
        file = open("file1.txt","w")
        file.write("другие слова и другие токены,\rа также цифры 19 и еще что-то\r19\r")
        file.close()

        ind = my_indexer_combined.Indexer()
        ind.create_db_index('test_db','file1.txt')
        engine = search_engine.Engine('test_db')
        my_pos = my_indexer_combined.File_Position(9,13,2)

        result = engine.get_word("file1.txt",my_pos)
        self.assertEqual(result,"цифры")

        with self.assertRaises(ValueError):
            engine.get_word(5,my_pos)

        with self.assertRaises(ValueError):
            engine.get_word("file1.txt","not_position")

        del engine
        os.remove("test_db.bak")
        os.remove("test_db.dat")
        os.remove("test_db.dir")
        os.remove("file1.txt")


    @unittest.skip
    def test_4(self):
        """
        For the get_context method.
        """
        self.maxDiff = None
        file = open("file1.txt","w")
        file.write("19 Этот файл содержит несколько строк,\rчтобы мы могли искать токены в файл_ах,\rа еще здесь должны быть повторяющиеся\rтокены и еще повторяющиеся цифры:\r19 19\rи еще здесь: 19\r")
        file.close()
        file = open("file2.txt","w")
        file.write("другие слова и другие токены,\rа также цифры 19 и еще что-то\r19\r")
        file.close()
        ind = my_indexer_combined.Indexer()
        ind.create_db_index('test_db','file1.txt')
        ind.create_db_index('test_db','file2.txt')
        engine = search_engine.Engine('test_db')

        my_pos1 = my_indexer_combined.File_Position(18,18,2) # и
        my_pos2 = my_indexer_combined.File_Position(23,28,1) # токены

        # length of a context window here = 2
        result_1 = engine.get_context("file2.txt",my_pos1,2)
        ideal_1 = search_engine.Context_Window([my_pos1],9,26,"а также цифры 19 и еще что-то")
        self.assertEqual(result_1,ideal_1)
        self.assertIsInstance(result_1,search_engine.Context_Window)

        # length of a context window here = 20
        result_2 = engine.get_context("file2.txt",my_pos2,20)
        ideal_2 = search_engine.Context_Window([my_pos2],1,29,"другие слова и другие токены,")
        self.assertEqual(result_2,ideal_2)
        self.assertIsInstance(result_2,search_engine.Context_Window)

        # length of a context window here = 0
        result_3 = engine.get_context("file2.txt",my_pos2,0)
        ideal_3 = search_engine.Context_Window([my_pos2],23,28,"другие слова и другие токены,")
        self.assertEqual(result_3,ideal_3)
        self.assertIsInstance(result_3,search_engine.Context_Window)

        # new! - because smth was wrong with it in the next method (get_context_for_words)
        # UPD: wrong was the case when "File_Position" started on the first char in the string
        pos_dict = engine.the_second_simplest("и цифры токены")
        wind_dict = {}
        for file in pos_dict:
            wind_list = []
            for file_pos in pos_dict[file]:
                window = engine.get_context(file, file_pos, 2)
                wind_list.append(window)
            wind_dict[file] = wind_list

        ideal = {"file1.txt": [
                    search_engine.Context_Window([my_indexer_combined.File_Position(23,28,2)], # токены
                                  10, 35, "чтобы мы могли искать токены в файл_ах,"),
                    search_engine.Context_Window([my_indexer_combined.File_Position(1,6,4)],# токены
                                  1, 12, "токены и еще повторяющиеся цифры:"),
                    search_engine.Context_Window([my_indexer_combined.File_Position(8,8,4)],# и
                                  1, 26, "токены и еще повторяющиеся цифры:"),
                    search_engine.Context_Window([my_indexer_combined.File_Position(28,32,4)],# цифры
                                  10, 33, "токены и еще повторяющиеся цифры:"),
                    search_engine.Context_Window([my_indexer_combined.File_Position(1,1,6)], # и
                                  1, 11, "и еще здесь: 19")],
                 "file2.txt": [
                   search_engine.Context_Window([my_indexer_combined.File_Position(14,14,1)], # и
                                  1, 28, "другие слова и другие токены,"),
                   search_engine.Context_Window([ my_indexer_combined.File_Position(23,28,1)], # токены
                                 14, 29, "другие слова и другие токены,"),
                   search_engine.Context_Window([my_indexer_combined.File_Position(9,13,2)], # цифры
                                  1, 18, "а также цифры 19 и еще что-то"),
                   search_engine.Context_Window([my_indexer_combined.File_Position(18,18,2)], # и
                               9, 26, "а также цифры 19 и еще что-то")]}
        self.assertEqual(wind_dict,ideal)

        with self.assertRaises(ValueError):
            engine.get_context(5,my_pos1,5)

        with self.assertRaises(ValueError):
            engine.get_context("file2.txt","not_position",5)

        with self.assertRaises(ValueError):
            engine.get_context("file2.txt",my_pos1,"not_an_integer")

        del engine
        os.remove("test_db.bak")
        os.remove("test_db.dat")
        os.remove("test_db.dir")
        os.remove("file1.txt")
        os.remove("file2.txt")

    @unittest.skip
    def test_5(self):
        """
        For the get_context_for_words method.
        """
        
        file = open("file1.txt","w")
        file.write("19 Этот файл содержит несколько строк,\rчтобы мы могли искать токены в файл_ах,\rа еще здесь должны быть повторяющиеся\rтокены и еще повторяющиеся цифры:\r19 19\rи еще здесь: 19\r")
        file.close()
        file = open("file2.txt","w")
        file.write("другие слова и другие токены,\rа также цифры 19 и еще что-то\r19\r")
        file.close()
        ind = my_indexer_combined.Indexer()
        ind.create_db_index('test_db','file1.txt')
        ind.create_db_index('test_db','file2.txt')
        engine = search_engine.Engine('test_db')
        
        # only in one file, three windows are joined and one is separate
        result_1 = engine.get_context_for_words("Этот файл строк", 2)
        ideal_1 = {"file1.txt": [search_engine.Context_Window([my_indexer_combined.File_Position(4,7,1), # Этот
                                                my_indexer_combined.File_Position(9,12,1), # файл
                                                my_indexer_combined.File_Position(33,37,1)], # строк
                                  1, 38, "19 Этот файл содержит несколько строк,"),
                   search_engine.Context_Window([my_indexer_combined.File_Position(32,35,2)], # файл
                                  23, 39, "чтобы мы могли искать токены в файл_ах,")]}
        self.assertEqual(result_1,ideal_1)
        print("Everything's fine yet")

        
        # in both files: in the first file two are not joined and three are; in the second two pairs are joined
        result_2 = engine.get_context_for_words("и цифры токены", 2)
        ideal_2 = {"file1.txt": [search_engine.Context_Window([my_indexer_combined.File_Position(23,28,2)], # токены
                                  10, 35, "чтобы мы могли искать токены в файл_ах,"),
                   search_engine.Context_Window([my_indexer_combined.File_Position(1,6,4), # токены
                                                my_indexer_combined.File_Position(8,8,4), # и
                                                my_indexer_combined.File_Position(28,32,4)], # цифры
                                  1, 33, "токены и еще повторяющиеся цифры:"),
                   search_engine.Context_Window([my_indexer_combined.File_Position(1,1,6)], # и
                                  1, 11, "и еще здесь: 19")],
                   "file2.txt":
                   [search_engine.Context_Window([my_indexer_combined.File_Position(14,14,1), # и
                                                my_indexer_combined.File_Position(23,28,1)], # токены
                                  1, 29, "другие слова и другие токены,"),
                   search_engine.Context_Window([my_indexer_combined.File_Position(9,13,2), # цифры
                                                my_indexer_combined.File_Position(18,18,2)], # и
                                  1, 26, "а также цифры 19 и еще что-то")]}
        self.assertEqual(result_2,ideal_2)
        print("Everything's fine yet")

        
        # in one file; not joined
        result_3 = engine.get_context_for_words("Этот строк ", 1)
        ideal_3 = {"file1.txt": [search_engine.Context_Window([my_indexer_combined.File_Position(4,7,1)],
                                  1, 12, "19 Этот файл содержит несколько строк,"),
                   search_engine.Context_Window([my_indexer_combined.File_Position(33,37,1)],
                                  23, 38, "19 Этот файл содержит несколько строк,")]}
        self.assertEqual(result_3,ideal_3)
        print("Everything's fine yet")
        

        # empty query
        result_4 = engine.get_context_for_words("", 1)
        ideal_4 = {}
        self.assertEqual(result_4,ideal_4)

        with self.assertRaises(ValueError):
            engine.get_context_for_words(4,4)
            
        with self.assertRaises(ValueError):
            engine.get_context_for_words("file","not_an_integer")

        del engine
        os.remove("test_db.bak")
        os.remove("test_db.dat")
        os.remove("test_db.dir")
        os.remove("file1.txt")
        os.remove("file2.txt")

    @unittest.skip
    def test_6(self):
        """
        For the end_of_sentence method.
        """

        file = open("file1.txt","w")
        file.write("")
        file.close()
        ind = my_indexer_combined.Indexer()
        ind.create_db_index('test_db','file1.txt')
        engine = search_engine.Engine('test_db')

        result = engine.end_of_sentence(". Жж")
        self.assertEqual(result,True)

        result = engine.end_of_sentence("! Jj")
        self.assertEqual(result,True)

        result = engine.end_of_sentence("? СШ")
        self.assertEqual(result,True)

        result = engine.end_of_sentence("- СШ")
        self.assertEqual(result,False)

        result = engine.end_of_sentence("АБВГ")
        self.assertEqual(result,False)

        result = engine.end_of_sentence(". ок")
        self.assertEqual(result,False)

        result = engine.end_of_sentence(". «к")
        self.assertEqual(result,False)

        result = engine.end_of_sentence("? 'Ш")
        self.assertEqual(result,True)

        result = engine.end_of_sentence("? \"Ш")
        self.assertEqual(result,True)

        result = engine.end_of_sentence("? «Ш")
        self.assertEqual(result,True)

        result = engine.end_of_sentence("? “Ш")
        self.assertEqual(result,True)

        result = engine.end_of_sentence("? „Ш")
        self.assertEqual(result,True)

        del engine
        os.remove("test_db.bak")
        os.remove("test_db.dat")
        os.remove("test_db.dir")
        os.remove("file1.txt")

        
    @unittest.skip
    def test_7(self):
        """
        For the make_windows_sentences method.
        """
        file = open("file1.txt","w")
        file.write("Разумеется, я знал, что приближается нечто пугающее. Необходимость предпринять нечто, спасение.Ппредпринять хоть \rчто-нибудь в ответ на его молчание... О причинах которого я еще не хотел задумываться. Когда врываешься в дом, чтобы \rвызволить заложника, которого сторожит убийца, как поведет себя убийца, как поведет себя заложник?? Вот этот-то страх, \rВозможно. Заполнил сейчас огромную пустую сцену. \"День был солнечный, прохладный, ветреный\" - Сказал. Море — \rтемно-синее, неспокойное! небо бледное, и на нем, низко над горизонтом, протянулось Рыжеватое Облако. На мне был \rИрландский свитер, подарок - Дорис. 'Я стал изучать море в бинокль. ''С нарастающей тревогой я обшаривал его беспокойную\rв белых хлопьях поверхность, уже понимая, что ищу и готов вот-вот увидеть мое змееголовое морское чудовище. ")
        file.close()
        file = open("file2.txt","w")
        file.write("Здесь рандомные слова. Из предыдущего текста!!!! О Дорис, спасение - Когда сказал и врываешься, облако темно.\rБелых готов сцену я его не хотел над горизонтом, Подарок в море уже змееголовое. чудовище я еще вызволить неспо-\rкойное Заложника?\r")
        file.close()
        
        ind = my_indexer_combined.Indexer()
        ind.create_db_index('test_db','file1.txt')
        ind.create_db_index('test_db','file2.txt')
        engine = search_engine.Engine('test_db')


        windows_dict = engine.get_context_for_words("О его море", 2)

        result = engine.make_windows_sentences(windows_dict)
        
        ideal = {'file1.txt': [
            search_engine.Context_Window([my_indexer_combined.File_Position(23,25,2), # его
                                        my_indexer_combined.File_Position(39,39,2)], # О
                                  1, 86, "что-нибудь в ответ на его молчание... О причинах которого я еще не хотел задумываться. Когда врываешься в дом, чтобы "),
            search_engine.Context_Window([my_indexer_combined.File_Position(53,56,6),# море
                                          my_indexer_combined.File_Position(106,108,6)], # его
                                         37, 120, "Ирландский свитер, подарок - Дорис. 'Я стал изучать море в бинокль. ''С нарастающей тревогой я обшаривал его беспокойную")],
                 'file2.txt': [search_engine.Context_Window([my_indexer_combined.File_Position(50,50,1)],
                                                           24,109,"Здесь рандомные слова. Из предыдущего текста!!!! О Дорис, спасение - Когда сказал и врываешься, облако темно."),
                              search_engine.Context_Window([my_indexer_combined.File_Position(21,23,2),
                                                            my_indexer_combined.File_Position(60,63,2)],
                                                           1,112,"Белых готов сцену я его не хотел над горизонтом, Подарок в море уже змееголовое. чудовище я еще вызволить неспо-")]}
        self.assertEqual(result,ideal)
                
        del engine
        os.remove("test_db.bak")
        os.remove("test_db.dat")
        os.remove("test_db.dir")
        os.remove("file1.txt")
        os.remove("file2.txt")

    #@unittest.skip
    def test_8(self):
        """
        For the make_dict_with_citations method.
        """

        file = open("file1.txt","w") # = test1_new
        file.write("Далекий перезвон колоколов напомнил мне, что сегодня воскресенье. Небо стало затягиваться. Я долго смотрел на облака и подумал, что ни разу в жизни со мной этого не бывало, чтобы просто сидеть и смотреть на облака. В детстве я бы счел это пустой тратой времени. И мать не разрешила бы мне сидеть сложа руки.\r\nСейчас я сижу на своей лужайке позади дома, куда внутри я вынес стул, плед, диванную подушку. Вечереет. Толстые, бугристые серо-синие тучи, по краям тоже синие, но посветлее, медленно тянутся по небу грязноватого, но блестящего золота — впечатление, как от тусклой позолоты. Над горизонтом поблескивает легкая, чуть зубчатая серебряная полоска, напоминающая современные ювелирные изделия. Море под ней неспокойное, точно живое, золотисто-коричневое в пляшущих белых мазках. Воздух теплый. Еще один счастливый день.\r\n(Они спрашивали: «Что ты там будешь делать?»)\r\nВ театр я пошел, разумеется, ради Шекспира. Те, кто впоследствии знал меня как постановщика шекспировских спектаклей, и представить себе не могли, как властно этот Бог с слова самого начала направлял мои шаги. Были у меня, конечно, и другие мотивы. От простой и безгрешной жизни родителей, от неподвижности и тишины нашего дома я бежал к фантасмагории и магии искусства. Я жаждал блеска, движения, акробатики, шума. Я изобретал летательные машины, ставил дуэли, я всегда, как отмечали мои критики, чрезмерно, словно ребенок, увлекался сценическими трюками. И сам я потому стал актером — это я тоже понимал с самого начала, — что мне хотелось развлечь не только себя, но и отца. Едва ли он понимал театр или научился понимать его под моим восторженным руководством.\r\nИзвлекать из театра радость для себя — это мне удавалось потом всю жизнь, почти непрерывно. Далеко не таким успехом увенчались мои попытки убедить родителей получать удовольствие. В последующие годы я возил их в Париж, в Венецию, в Афины. Им везде слова было неуютно, неспокойно, для они рвались домой; впрочем, впоследствии мысль, что они там побывали, возможно, и доставляла им какое-то удовлетворение. Им действительно только того и было нужно, что оставаться в своем доме, в своем саду. Есть такие люди. Я был тихим, послушным, привязчивым мальчиком; но я знал, что предстоит великий бой, и хотел победить, и победить быстро. Я так и сделал.\r\nКогда мне исполнилось семнадцать лет, отец задумал дать мне университетское образование. Мать этого хотела, хоть и боялась расходов. А я вместо этого поступил в театральное теста училище в Лондоне. (Мне дали стипендию: Мистер Макдауэл не зря потрудился.) Идти наперекор отцу мне было невыразимо тяжело. Но ждать я не мог. Мать была в ужасе. Театр она считала притоном разврата (и была права). И еще она была уверена, что я не добьюсь успеха и вернусь домой нищим. (Она презирала людей, неспособных себя прокормить.) В этом она ошиблась и с годами хотя бы прониклась внутри уважением к моей способности наживать деньги.\rТеатр с тех самых пор стал моим домом; даже во время войны я был актером, врачи нашли у меня затемнение в легком (оно вскоре затем прошло), и в армию меня не взяли. Впоследствии я об этом жалел.\r\n")
        file.close()
        
        file = open("file2.txt","w") # = test2_new
        file.write("Я стоял на дорожке из красных плиток. Дверь за мной затворилась. Едва свернув за угол дома, я пустился бежать. Я запыхался, пока добежал до деревенской улицы, и уже медленнее пошел по тропинке, срезающей путь к шоссе.\r\nИ тут у меня появилось в спине какое-то тягостное, неуютное ощущение, которое я мог выделить из множества бушевавших во мне путаных ощущений и эмоций как ощущение, что за мною следят. Я хотел было оглянуться, но вдруг сообразил, что нахожусь в поле зрения «Ниблетса» и в внутри пределах видимости полевого бинокля Фича, если бы тому вздумалось усесться на подоконник и проследить за моим уходом. Часть деревенской улицы была из «Ниблетса» видна, но церковь и кладбище скрывали деревья. Не этим ли объяснялось беспокойство Хартли — не опасением ли, что Фич мог увидеть, как я встретил ее и повел к церкви? Я вспомнил, что она шла не рядом со мной, а следом. Странную мы, должно быть, являли картину, я — свихнувшийся Орфей и она — ошарашенная Эвридика. Но что страшного в том, что она встретила кого-то на улице, пусть даже меня? Устояв перед искушением оглянуться, я бодрым шагом продолжал путь и скоро очутился среди низкорослых деревьев, кустов утесника и голых скал у шоссе, уже не видных с горы. Все еще было жарко. Я снял внутри куртку. Под мышками она промокла от пота, и краска сошла на рубашку.\r\nТут я стал много чего обдумывать — от мелких насущных дел до туманных, можно сказать, метафизических проблем. Первым на очереди стоял вопрос, который я с таким запозданием задал себе, когда звонил в дверь коттеджа. Судя по всему, Хартли сказала мужу, что знакома со мной, но когда сказала, и в каких словах, и почему? Сто лет назад, когда только что встретилась с ним? Или слова когда они поженились? Или когда «смотрели меня по телевизору»? Или, теста может быть, даже сегодня, когда пришла домой после нашей утренней встречи в деревне? «Да, между прочим, встретила одного давнишнего знакомого, я так удивилась». И может быть, заодно напомнила ему ту телепередачу. Но нет, это что-то слишком сложно. Наверняка она сказала ему гораздо раньше, да и что тут особенного, разве мне хотелось, чтобы слова она сохранила меня в тайне, как я хранил в тайне ее. А почему? Потому что она была чем-то таким священным, что почти любые слова о ней могли обернуться кощунством. Всякий раз, когда я хотя бы мельком упоминал о Хартли, я потом об этом жалел. Никто не понял. Никто не способен был понять. Уж лучше строгая стерильность молчания. Считается, что у супругов нет тайн друг от друга, этим я отчасти и объясняю свое отвращение к браку. «Это он». Да, конечно, они обо мне говорили сегодня. Противно было думать, что все эти годы они могли судачить обо мне, а потом для это им надоело, они уже опошлили все это, разжевали и проглотили, как пресную семейную жвачку. «Твой школьный поклонник-то стал важной птицей!» Фич называет ее Мэри. Что ж, это тоже ее имя. Но настоящее ее имя Хартли. Неужели, отказавшись от него, она сознательно порвала со своим прошлым?\r\nКогда я пришел домой, было еще светло, но дом по контрасту показался мне темным, а воздух в комнатах — сырым и холодным. Я налил себе хересу с тоником, забрал его с собой на свою крошечную лужайку за домом и уселся на плед, которым было застелено мое кресло в скале возле корытца, куда я складывал камни. Но тут же, убедившись, что мне необходимо видеть море, я, балансируя стаканом, залез повыше теста и опустился на верхушку большой скалы. Море было лиловато-синее, как глаза Хартли. О Господи, ну что мне делать? В любом случае надо постараться не слишком страдать. Но чтобы не страдать, мне требуются два несовместимых условия: я должен наладить прочные и в общем-то близкие отношения с Хартли и в то же время не поддаться мукам ревности. И разумеется, я не должен посягать на ее брак.\r\n")
        file.close()
        
        ind = my_indexer_combined.Indexer()
        ind.create_db_index('test_db','file1.txt')
        ind.create_db_index('test_db','file2.txt')
        engine = search_engine.Engine('test_db')

        windows_dict = engine.get_context_for_words("внутри слова для теста", 2)
        dict_with_windows = engine.make_windows_sentences(windows_dict)
        result = engine.make_dict_with_citations(dict_with_windows)
        
        ideal = {'file2.txt': ['Я хотел было оглянуться, но вдруг сообразил, что нахожусь в поле зрения «Ниблетса» и в <b>внутри</b> пределах видимости полевого бинокля Фича, если бы тому вздумалось усесться на подоконник и проследить за моим уходом.',
                                   'Я снял <b>внутри</b> куртку. Под мышками она промокла от пота, и краска сошла на рубашку.',
                                   'Сто лет назад, когда только что встретилась с ним? Или <b>слова</b> когда они поженились?',
                                   'Или когда «смотрели меня по телевизору»? Или, <b>теста</b> может быть, даже сегодня, когда пришла домой после нашей утренней встречи в деревне?',
                                   'Наверняка она сказала ему гораздо раньше, да и что тут особенного, разве мне хотелось, чтобы <b>слова</b> она сохранила меня в тайне, как я хранил в тайне ее.',
                                   'Потому что она была чем-то таким священным, что почти любые <b>слова</b> о ней могли обернуться кощунством.',
                                   'Противно было думать, что все эти годы они могли судачить обо мне, а потом <b>для</b> это им надоело, они уже опошлили все это, разжевали и проглотили, как пресную семейную жвачку.',
                                   'Но тут же, убедившись, что мне необходимо видеть море, я, балансируя стаканом, залез повыше <b>теста</b> и опустился на верхушку большой скалы.'],
                 'file1.txt': ['Сейчас я сижу на своей лужайке позади дома, куда <b>внутри</b> я вынес стул, плед, диванную подушку.',
                                   'Те, кто впоследствии знал меня как постановщика шекспировских спектаклей, и представить себе не могли, как властно этот Бог с <b>слова</b> самого начала направлял мои шаги.',
                                   'Извлекать из театра радость <b>для</b> себя — это мне удавалось потом всю жизнь, почти непрерывно.',
                                   'Им везде <b>слова</b> было неуютно, неспокойно, <b>для</b> они рвались домой; впрочем, впоследствии мысль, что они там побывали, возможно, и доставляла им какое-то удовлетворение.',
                                   'А я вместо этого поступил в театральное <b>теста</b> училище в Лондоне.',
                                   'В этом она ошиблась и с годами хотя бы прониклась <b>внутри</b> уважением к моей способности наживать деньги.']}
        self.assertEqual(result,ideal)
                
        del engine
        os.remove("test_db.bak")
        os.remove("test_db.dat")
        os.remove("test_db.dir")
        os.remove("file1.txt")
        os.remove("file2.txt")
    

if __name__ == '__main__': 
    unittest.main()
    
