import os
import time
import re
from tkinter import filedialog
from googletrans import Translator


def books_processing(translation_trigger=False, transliteration_trigger=False, filepath=False):
    """Выгребает все нужные значения из файлов, создает все теги"""

    translator = Translator()
    all_english_symbols = 'qwertyuiopasdfghjklzxcvbnm'
    books_read = []
    exceptions_for_translation = ['pdfdrive', 'drive', 'doc']
    exceptions_for_splitting = ['PDFDrive']
    books_for_post_processing = {}

    for root, directory, name in os.walk(str(filepath)):  # считывает все названия из выбранной папки
        books_read.append([root, name])
    root = books_read[0][0]  # выписывает директорию считанных файлов
    for book_name in books_read[0][1]:

        #  считывает размер файла и приводит его к виду "мегабайт.хх"
        read_sizes = os.path.getsize(str(filepath) + '/' + str(book_name))
        size = round(float(read_sizes / 1000000), 2)

        modification_time = os.path.getmtime(str(filepath) + '/' + str(book_name))
        local_modification_time = time.ctime(modification_time)

        creation_time = os.path.getctime(str(filepath) + '/' + str(book_name))
        local_creation_time = time.ctime(creation_time)

        last_open_time = os.path.getatime(str(filepath) + '/' + str(book_name))
        local_last_open_time = time.ctime(last_open_time)

        # забирает значение названия книги
        pseudo_tags = book_name

        # предобработка с килянием ненужных символов и разбиванием слов пробелами
        elements_to_clear = [
            (',', ' '), ('-', ' '), ('_', ' '), ('(', ' '), (')', ' '), ('[', ' '), (']', ' '),
            ("'", ''), ("~", ' '), ("$", ' '), (".", ' ')
        ]

        for initial_element, final_element in elements_to_clear:
            pseudo_tags = pseudo_tags.replace(initial_element, final_element)

        split_tags_with_glued = pseudo_tags.split()

        # разделяет склеенные слова в стиле ПервыеСловаВторыеСлова на рус и en, и фильтрует одиночные символы +
        # слова полностью из верхнего регистра
        tags = []
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
                        for words in splits.split():
                            if len(words) > 1 and words not in split_tags:
                                split_tags.append(words)

        def en_ru(tr_word):
            """Функция перевода на русский и транслитерации"""

            translated_tag = ''
            # перевод на русский через сервисы гугла
            word = tr_word.lower()
            timer = 0
            for symbol in word:
                if symbol in all_english_symbols:
                    timer += 1
                    if timer == len(word):
                        trans = translator.translate(word, dest='ru')
                        translated_tag = trans.text

            return translated_tag.lower()

        #
        # простая транслитерация
        #
        # при проверке в оригинале слова убирать мягкие знаки, делать "ш" == "щ", "у" == "ю", "э" == "е",
        # "ы" == "и", "е" == "и", "ц" == "к", "иан" == "аен" == "айен",  "а" == "э", "е" == "йэ" == "йо",
        # "ю" == "йу", "я" == "йа", "в" == "уэ", "и" == "ай""
        #

        def transliterate(word):

            # Словарь с заменами
            slovar = {
                'sch': 'щ', 'ch': 'ч', 'shh': 'ш', 'sh': 'ш', 'zh': 'ж', 'yo': 'е', 'jo': 'е', 'je': 'е',
                'yu': 'ю', 'ju': 'ю', 'ya': 'я', 'ja': 'я', 'ph': 'ф',

                'a': 'а', 'b': 'б', 'c': 'ц', 'd': 'д', 'e': 'е', 'f': 'ф', 'g': 'г', 'h': 'х', 'i': 'и',
                'j': 'й', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'q': 'к', 'r': 'р',
                's': 'с', 't': 'т', 'u': 'у', 'v': 'в', 'w': 'в', 'x': 'кз', 'y': 'ы', 'z': 'з',

                'ґ': 'г', 'ї': 'и', 'є': 'е', 'Є': 'е'
            }

            # Циклически заменяем все буквы в строке
            for key in slovar:
                word = word.replace(key, slovar[key])

            return word

        # генерация тегов на русском и английском
        translation = []
        transliteration = []

        for tag in split_tags:
            tag = tag.lower()
            if len(tag) > 1:
                tags.append(tag)

                # перевод на английский с проверкой на английские буквы
                if translation_trigger and tag.isalpha():
                    for alpha in all_english_symbols:
                        if alpha in tag and tag not in exceptions_for_translation and tag != split_tags[-1]:
                            tr = en_ru(tag)
                            if len(tr) > 1 and tr not in tag:
                                translation.append(tr)
                                break

                # пропускает через простой модуль транслитерации
                if transliteration_trigger and tag.isalpha() and tag != split_tags[-1] \
                        and tag not in exceptions_for_translation:
                    transliterated = transliterate(tag)
                    if transliterated not in translation and transliterated not in tag:
                        transliteration.append(transliterated)

        book_format = tags[-1]

        books_for_post_processing[books_read[0][1].index(book_name)] = \
            {
             'root': root,
             'book_name': book_name,
             'book_format': book_format,
             'size': size,
             'local_creation_time': local_creation_time,
             'creation_time': creation_time,
             'local_modification_time': local_modification_time,
             'modification_time': modification_time,
             'local_last_open_time': local_last_open_time,
             'last_open_time': last_open_time,
             'tags': tags,
             'translation': translation,
             'transliteration': transliteration
             }

    return books_for_post_processing


def ask_and_check_directory():
    """
    Первично проверяет наличие файлов и глубину их залегания.
    Возвращает словарь:

        {глубина_1: [[директория, количество файлов], [директория, количество файлов]], глубина_2: [[...]], ...}

    """
    filepath = filedialog.askdirectory()

    # если путь был выбран
    if filepath:
        file_names = os.listdir(filepath)
        print(file_names)

        # проверить наличие файлов в выбранной директории
        file_trigger = False
        if file_names:
            check_for_files = os.walk(filepath)
            for dirpath, dirnames, filenames in check_for_files:
                if filenames:
                    file_trigger = True
                    break

            # если триггер сработал, передаёт пути в ГУИ для возможности выбора и предпросмотра
            if file_trigger:
                directories = {}
                # узнает глубину директории и количество файлов внутри
                for dirpath, dirnames, filenames in os.walk(filepath):
                    depth = dirpath.count("\\")
                    directories.setdefault(depth, []).append({'dirpath': dirpath, 'files_number': len(filenames)})
                return directories

            else:
                return "No files read"

        else:
            return "Can't read files"

    else:
        return "Window were closed"
