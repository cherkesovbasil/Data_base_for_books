import os
import time
import re
from tkinter import filedialog
from googletrans import Translator
from transliterate import translit


class Pre_processing:
    """функция для считывания названия из выбранной директории и первичной обработки"""

    def __init__(self):
        self.books_for_post_processing = {}
        self.filepath = filedialog.askdirectory()
        print(self.filepath)

    def books_processing(self):
        """выгребает все нужные значения из файлов, создает все тэги"""

        if self.filepath == '':
            return

        translator = Translator()
        all_english_symbols = 'qwertyuiopasdfghjklzxcvbnm'
        books_read = []
        exceptions_for_translation = ['pdfdrive', 'drive']
        exceptions_for_splitting = ['PDFDrive']

        for root, directory, name in os.walk(self.filepath):  # считывает все названия из выбранной папки
            books_read.append([root, name])
        root = books_read[0][0]  # выписывает директорию считаных файлов

        for book_name in books_read[0][1]:

            #  считывает размер файла и приводит его к виду "мегабайт.хх"
            read_sizes = os.path.getsize(self.filepath + '/' + book_name)
            size = round(float(read_sizes / 1000000), 2)

            modification_time = os.path.getmtime(self.filepath + '/' + book_name)
            local_modification_time = time.ctime(modification_time)

            creation_time = os.path.getctime(self.filepath + '/' + book_name)
            local_creation_time = time.ctime(creation_time)

            last_open_time = os.path.getatime(self.filepath + '/' + book_name)
            local_last_open_time = time.ctime(last_open_time)

            # забирает значение названия книги
            pseudo_tags = book_name

            # предобработка с килянием ненудных символов и разбиванием слов пробелами
            pseudo_tags = pseudo_tags.replace('.', ' ')
            pseudo_tags = pseudo_tags.replace(',', ' ')
            pseudo_tags = pseudo_tags.replace('-', ' ')
            pseudo_tags = pseudo_tags.replace('_', ' ')
            pseudo_tags = pseudo_tags.replace('(', ' ')
            pseudo_tags = pseudo_tags.replace(')', ' ')
            split_tags_with_glued = pseudo_tags.split()
            tags = []

            # разделяет склееные слова в стиле ПервыеСловаВторыеСлова на рус и en, и фильтрует одиночные символы +
            # слова полностью из верхнего регистра
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

                translated_tag = ''
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
                tag = tag.lower()
                if len(tag) > 1:
                    tags.append(tag)

                    # перевод на английский с проверкой на английские буквы
                    if tag.isalpha():
                        for alpha in all_english_symbols:
                            if alpha in tag and tag not in exceptions_for_translation and tag != split_tags[-1]:
                                tr = en_ru(tag)
                                if len(tr) > 1 and tr != '0' and tr not in tag:
                                    translation.append(tr)

                                # модуль транслитерации с заменой "W" и "Q"
                                if len(tag) > 1:
                                    transliterated = translit(tag, 'ru')
                                    transliterated = transliterated.replace("w", "в")
                                    transliterated = transliterated.replace("q", "кв")
                                    if transliterated not in translation and transliterated not in tag:
                                        transliteration.append(transliterated)
                                break

            book_format = tags[-1]

            self.books_for_post_processing[books_read[0][1].index(book_name)] = [root, book_name, book_format,
                                                                                 size,
                                                                                 local_creation_time,
                                                                                 local_modification_time,
                                                                                 local_last_open_time, tags,
                                                                                 translation,
                                                                                 transliteration]
        return self.books_for_post_processing


init_books = Pre_processing()
books = init_books.books_processing()
print(books)
if books:
    for items in books.values():
        print(items)
else:
    print('ОКНО ВЫБОРА ПАПКИ ДЛЯ СЧИТЫВАНИЯ В БАЗУ БЫЛО ЗАКРЫТО')
