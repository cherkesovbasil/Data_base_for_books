import os
import time
import re
from transliterate import translit, get_available_language_codes
from langdetect import detect

books_read = []
books_for_refactor = {}
root = ()
exceptions_for_transliteration = ['дйву', 'еxе', 'пдф']

for root, directory, name in os.walk('C:/Users/vasil/Desktop/мамины книги'):  # считывает все названия из выбранной папки
    books_read.append([root, name])
    print(get_available_language_codes())
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

    pseudo_tags = book_name
    split_tags = pseudo_tags.replace('.', ' ').split()
    tags = []
    for tag in split_tags:
        if tag != '(' and tag != ')' and tag != 'PDFDrive' and tag != '_' and tag != '-':
            if '(' not in tag and ')' not in tag and '_' not in tag:
                tags.append(tag.lower())

                # задел для перевода на русский (ищет только тру-английские слова)
                if tag.isalpha():
                    if detect(tag) == 'en':
                        pass
                    # задел для тринслитерации
                    else:
                        all_english_symbols = 'qwertyuiopasdfghjklzxcvbnm'
                        timer = 0
                        for symbol in tag:
                            if symbol in all_english_symbols:
                                timer += 1
                                if timer == len(tag):
                                    if translit(tag, 'ru') not in exceptions_for_transliteration:
                                        print(translit(tag, 'ru'))
                    # окончание модуля перевода-транслитерации

            if '(' in tag and ')' in tag and '_' not in tag:
                clear_tag = re.sub('[(|)]', '', tag)
                tags.append(clear_tag.lower())

                # задел для перевода на русский (ищет только тру-английские слова)
                if tag.isalpha():
                    if detect(tag) == 'en':
                        pass
                    # задел для тринслитерации
                    else:
                        all_english_symbols = 'qwertyuiopasdfghjklzxcvbnm'
                        timer = 0
                        for symbol in tag:
                            if symbol in all_english_symbols:
                                timer += 1
                                if timer == len(tag):
                                    if translit(tag, 'ru') not in exceptions_for_transliteration:
                                        print(translit(tag, 'ru'))
                    # окончание модуля перевода-транслитерации

            if '_' in tag:
                reformat_tag = re.sub('_', ' ', tag)
                split_on_words = reformat_tag.replace('_', ' ').split()
                for words in split_on_words:
                    tags.append(words.lower())

                    # задел для перевода на русский (ищет только тру-английские слова)
                    if words.isalpha():
                        if detect(words) == 'en':
                            pass
                        # задел для тринслитерации
                        else:
                            all_english_symbols = 'qwertyuiopasdfghjklzxcvbnm'
                            timer = 0
                            for symbol in words:
                                if symbol in all_english_symbols:
                                    timer += 1
                                    if timer == len(words):
                                        if translit(words, 'ru') not in exceptions_for_transliteration:
                                            print(translit(words, 'ru'))
                        # окончание модуля перевода-транслитерации

    book_format = tags[-1]

    books_for_refactor[books_read[0][1].index(book_name)] = [root, book_name, book_format, size, local_creation_time, local_modification_time, local_last_open_time, tags]  # прописывает в кортеж номер, директорию и название файла

for items in books_for_refactor.values():
    print(items)


