import os
import time
import re
from googletrans import Translator
from transliterate import translit, get_available_language_codes
from langdetect import detect

translator = Translator()
all_english_symbols = 'qwertyuiopasdfghjklzxcvbnm'

books_read = []
books_for_refactor = {}
root = ()
exceptions_for_translation = ['djvu', 'exe', 'pdf', 'fb2']
translated_tag = ''

for root, directory, name in os.walk('C:/Users/vasil/Desktop/мамины книги'):  # считывает все названия из выбранной папки
    books_read.append([root, name])
root = books_read[0][0]  # выписывает директорию считаных файлов

for book_name in books_read[0][1]:

    #  считывает размер файла и приводит его к виду мегабайт.хх
    read_sizes = os.path.getsize('C:/Users/vasil/Desktop/мамины книги/' + book_name)
    size = round(float(read_sizes / 1000000), 2)

    modification_time = os.path.getmtime('C:/Users/vasil/Desktop/мамины книги/' + book_name)
    local_modification_time = time.ctime(modification_time)

    creation_time = os.path.getctime('C:/Users/vasil/Desktop/мамины книги/' + book_name)
    local_creation_time = time.ctime(creation_time)

    last_open_time = os.path.getatime('C:/Users/vasil/Desktop/мамины книги/' + book_name)
    local_last_open_time = time.ctime(last_open_time)

    # забирает значение названия книги
    pseudo_tags = book_name
    split_tags = pseudo_tags.replace('.', ' ').split()

    tags = []
    english_tags = []

    def en_ru(tr_word):
        """функция перевода на русский и транслитерации"""

        global translated_tag
        global all_english_symbols

        # задел для тринслитерации
        timer = 0
        word = tr_word.lower()
        print(word + '\n***************without translation***************')
        for symbol in word:
            if symbol in all_english_symbols:
                timer += 1
                if timer == len(word):
                    trans = translator.translate(word, dest='ru')
                    translated_tag = trans.text.lower()
                    print(translated_tag + 'STOP\n\n\n')

        return translated_tag
            # окончание модуля перевода-транслитерации

    # фильтрация мусора
    for tag in split_tags:
        print('-----------------START:-----------------\n' + tag)
        if tag != '(' and tag != ')' and tag != 'PDFDrive' and tag != '_' and tag != '-':
            if '(' not in tag and ')' not in tag and '_' not in tag and '-' not in tag:

                tags.append(tag.lower())
                if tag not in exceptions_for_translation:
                    tr = en_ru(tag)


            elif '(' in tag or ')' in tag :
                clear_tag = re.sub('[(|)]', '', tag)
                while '(' in clear_tag and ')' in clear_tag:
                    clear_tag = re.sub('[(|)]', '', tag)

                tags.append(clear_tag.lower())
                tags.append(tag.lower())

                if clear_tag not in exceptions_for_translation:
                    tr = en_ru(clear_tag)


            if '_' in tag:
                reformat_tag = re.sub('_', ' ', tag)
                split_on_words = reformat_tag.replace('_', ' ').split()
                for words in split_on_words:

                    tags.append(words.lower())

                    if words not in exceptions_for_translation:
                        tr = en_ru(words)


    book_format = tags[-1]

    books_for_refactor[books_read[0][1].index(book_name)] = [root, book_name, book_format, size, local_creation_time, local_modification_time, local_last_open_time, tags]  # прописывает в кортеж номер, директорию и название файла

for items in books_for_refactor.values():
    print(items)


