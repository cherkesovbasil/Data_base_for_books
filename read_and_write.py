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
exceptions_for_splitting = ['PDFDrive']
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

    pseudo_tags = pseudo_tags.replace('.', ' ')
    pseudo_tags = pseudo_tags.replace(',', ' ')
    pseudo_tags = pseudo_tags.replace('-', ' ')
    pseudo_tags = pseudo_tags.replace('_', ' ')
    pseudo_tags = pseudo_tags.replace('(', ' ')
    pseudo_tags = pseudo_tags.replace(')', ' ')
    split_tags_with_glued = pseudo_tags.split()
    tags = []
    english_tags = []

    # разделяет склееные слова в стиле ПервыеСловаВторыеСлова на рус и en, и фильтрует одиночные символы + слова полностью из верхнего регистра
    split_tags = []
    for words_for_splitting in split_tags_with_glued:
        if words_for_splitting.lower() not in exceptions_for_splitting and len(words_for_splitting) > 1:
            after_splitting_words = []
            split_tags.append(words_for_splitting)
            number_of_upper_symbols = sum(i.isupper() for i in words_for_splitting)
            if number_of_upper_symbols >= 2 and number_of_upper_symbols != len(words_for_splitting):
                after_splitting_words.append(re.sub(r'(?<=\w)(?=[A-Z])', '   ', words_for_splitting))
                after_splitting_words.append(re.sub(r'(?<=\w)(?=[А-Я])', '   ', words_for_splitting))
                for splits in after_splitting_words:
                    for items in splits.split():
                        if len(items) > 1 and items not in split_tags:
                            split_tags.append(items)

    def en_ru(tr_word='0'):
        """функция перевода на русский и транслитерации"""

        global translated_tag
        global all_english_symbols

        # перевод на русский через сервисы гугла
        word = tr_word.lower()
        timer = 0
        for symbol in word.lower():
            if symbol in all_english_symbols:
                timer += 1
                if timer == len(word):
                    trans = translator.translate(word, dest='ru')
                    translated_tag = trans.text.lower()

        return translated_tag


    # генерация тегов на русском и английском
    translation = []
    transliteration = []

    for tag in split_tags:
        if len(tag) > 1:
            tags.append(tag.lower())

            # перевод на английский с проверкой на английские буквы
            if tag.lower() and tag.isalpha():
                for alpha in all_english_symbols:
                    if alpha in tag and tag not in exceptions_for_translation:
                        tr = en_ru(tag)
                        if len(tr) > 1:
                            translation.append(tr)

                            # модуль транслитерации с заменой "W"
                            transliterated = translit(tag, 'ru').lower()
                            transliterated = transliterated.replace("w", "в")
                            if transliterated not in translation:
                                transliteration.append(transliterated)
                            break

    book_format = tags[-1]
    books_for_refactor[books_read[0][1].index(book_name)] = [root, book_name, book_format, size, local_creation_time, local_modification_time, local_last_open_time, tags, translation, transliteration]  # прописывает в кортеж номер, директорию и название файла

for items in books_for_refactor.values():
    print(items)
