import text
section_words = {'start': -1, '1.1': 6, '1.2': 14, '1.3': 16}
the_text =  [('IN', '"in', 0), ('NOVVS', 'new\r\n', 1), ('FERO', '"to bear', 2), ('ANIMVS', '"spirit', 3), ('MVTO/2', 'to change\r\n', 4), ('DICO/2', '"to say', 5), ('FORMA', 'shape; beauty\r\n', 6), ('CORPVS', 'body\r\n', 7), ('DEVS', 'god\r\n', 8), ('COEPIO', 'to begin\r\n', 9), ('NAM', 'for\r\n', 10), ('VOS', 'you\r\n', 11), ('MVTO/2', 'to change\r\n', 12), ('ET/1', '"even', 13), ('ILLE', 'that\r\n', 14), ('ASPIRO', 'to breathe to or upon\r\n', 15), ('MEVS', '"my', 16)]
section_list ={'1.1': 'start', '1.2': '1.1', '1.3': '1.2'}
title = "Ovid, Test Jun5 2"
section_level =  2
language = "Latin"
book = text.Text(title, section_words, the_text, section_list, section_level, language)