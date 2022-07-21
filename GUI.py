import read_and_write
from read_and_write import *


# вот сюда будут приходить все приколдэсы из функций обработки
# отсюда уходит запрос на считку директорий
# сюда приходит ответ по количеству файлов и ветвлению
# человек выбирает нужные параметры, работая со сгенерированным словарём
# отправляет обратно данные для переработки через циклическую функцию в препроцессинг
# если директория одна, то циклическая функция отрабатывает только 1 цикл


class Gui:
    """Графический интерфейс"""

    def __init__(self):
        self.processed_books = []

    def check_directory(self):

        # ДО ЭТОГО МОМЕНТА ОПРЕДЕЛЯЮТСЯ СЛЕДУЮЩИЕ ПЕРЕМЕННЫЕ:
        # - translation_trigger
        # - transliteration_trigger
        # ПО ЭТОМУ ДАЛЬШЕ ПОКА ЧТО БУДУТ КОСТЫЛИ False/True. Дописать и заменить

        #
        # При выборе галочкой перевода через гугл, сразу проверять его работоспособность и выдавать сообщение в ГУИ
        #

        direct = ask_and_check_directory()

        if direct == "Window were closed":
            # КОСТЫЛЬ ДО МОМЕНТА СОЗДАНИЯ ИНТЕРФЕЙСА
            print('Окно было закрыто')
            return

        if direct == "Can't read files":
            # КОСТЫЛЬ ДО МОМЕНТА СОЗДАНИЯ ИНТЕРФЕЙСА
            print('В выбранной директории нет файлов')
            return

        if direct == "No files read":
            # КОСТЫЛЬ ДО МОМЕНТА СОЗДАНИЯ ИНТЕРФЕЙСА
            print('Система смогла распознать только папки в выбранной директории')
            return

        print('\nсчитанные директории\n' + str(direct))

        #
        # ТУТ ПОЛЬЗОВАТЕЛЬ ВЫБИРАЕТ ТРЕБУЕМЫЕ ПАПКИ ДЛЯ ЗАГРУЗКИ В БАЗУ. ВЫБОР ПО ФАЙЛАМ, НАВЕРНОЕ, ДЕЛАТЬ НЕ СТОИТ.
        # ЭТО БУДЕТ ИЗБЫТОЧНО. ТЕМ БОЛЕЕ БАЗА ДАННЫХ БУДЕТ РАБОТАТЬ В ПЕРВУЮ ОЧЕРЕДЬ С ДИРЕКТОРИЯМИ ЦЕЛИКОМ
        #

        #
        # КОСТЫЛЬ. СЧИТАЕМ, ЧТО ПОЛЬЗОВАТЕЛЬ ВЫБРАЛ ВСЕ ДИРЕКТОРИИ
        #

        for depth in direct.values():
            for elements in depth:
                if elements['files_number'] != 0:
                    books = books_processing(translation_trigger=False, transliteration_trigger=True,
                                             filepath=elements['dirpath'])

                    for value in books.values():
                        self.processed_books.append(value)
        print('\nсчитанные данные:')
        for items in self.processed_books:
            print(items)


init_check = Gui()
init_check.check_directory()
