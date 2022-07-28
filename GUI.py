from read_and_write import *
from tkinter import *
from tkinter import font
# + вот сюда будут приходить все приколдэсы из функций обработки
# + отсюда уходит запрос на считку директорий
# + сюда приходит ответ по количеству файлов и ветвлению
# человек выбирает нужные параметры, работая со сгенерированным словарём
# + отправляет обратно данные для переработки через циклическую функцию в препроцессинг
# + если директория одна, то циклическая функция отрабатывает только 1 цикл


class Gui:
    """Графический интерфейс"""

    def __init__(self):
        self.box = None

    def open_db(self):
        #
        # Временная замена отображения списка баз данных
        #

        something = ["uno", 'duo', 'пятое', 'десятое', 'всякая непонятная херобора',
                     'оооооооооооооооооооооочень мноооооооооооого тееееееееееееееееееееееееееекста !!!!!!!!!!!!!!',
                     "ПРОСТО СТРАННАЯ ШТУКА КАПСОМ", 'gjxtve ,s b y]lf', 'почему бы и да', "тут есть нешта живое?",
                     '2', '3', '4', '5']
        for smth in something:
            self.box.insert(END, smth)
        print('AAAAAAAAAAAAAAAAAAAAAAA')


    def new_db_generation(self):
        generation_window = Tk()
        generation_window.title("Базы данных")
        large_font = font.Font(weight='bold', size=12)

        # disables the ability to zoom the page
        generation_window.resizable(False, False)

        # frame for the main interface
        frame_for_buttons_start_window = LabelFrame(generation_window)
        frame_for_buttons_start_window.pack(side=TOP)

        # outputs the information about the absolute error in the GUI
        open_btn = Button(frame_for_buttons_start_window, text="Открыть БД", relief=GROOVE, width=30)
        open_btn.pack(side=LEFT)
        new_db_btn = Button(frame_for_buttons_start_window, text="Создать новую БД", relief=GROOVE, width=30)
        new_db_btn.pack(side=LEFT)
        delete_db_btn = Button(frame_for_buttons_start_window, text="Удалить БД", relief=GROOVE, width=30, cursor='X_cursor')
        delete_db_btn.pack(side=LEFT)

        # sets the size of the window and places it in the center of the screen
        generation_window.update_idletasks()  # Updates information after all frames are created
        s = generation_window.geometry()
        s = s.split('+')
        s = s[0].split('x')
        width_main_window = int(s[0])
        height_main_window = int(s[1])

        w = generation_window.winfo_screenwidth()
        h = generation_window.winfo_screenheight()
        h = h // 2
        w = w - width_main_window - 12
        h = h - height_main_window // 2
        generation_window.geometry('+{}+{}'.format(w, h))
        print('BBBBBBBBBBBBBBBBBBBBBBB')

    def delete_db(self):
        print('DDDDDDDDDDDDDDDDDDDDDDD')

    def init_start_window(self):
        """Запускает первичное окно с возможностью первичного просмотра баз данных, добавления, удаления, открытия"""

        start_window = Tk()
        start_window.title("Базы данных")
        large_font = font.Font(weight='bold', size=12)

        # disables the ability to zoom the page
        start_window.resizable(False, False)

        # frame for the main interface
        frame_for_list_of_dbs = LabelFrame(start_window)
        frame_for_list_of_dbs.pack(side=TOP)
        frame_for_buttons_start_window = LabelFrame(start_window)
        frame_for_buttons_start_window.pack(side=TOP)

        self.box = Listbox(frame_for_list_of_dbs, width=71, selectbackground='grey70', font=large_font)
        self.box.pack(side=LEFT)
        scroll = Scrollbar(frame_for_list_of_dbs, command=self.box.yview)
        scroll.pack(side=LEFT, fill=Y)
        self.box.config(yscrollcommand=scroll.set)

        # outputs the information about the absolute error in the GUI
        open_btn = Button(frame_for_buttons_start_window, text="Открыть БД", relief=GROOVE, width=30, command=self.open_db)
        open_btn.pack(side=LEFT)
        new_db_btn = Button(frame_for_buttons_start_window, text="Создать новую БД", relief=GROOVE, width=30, command=self.new_db_generation)
        new_db_btn.pack(side=LEFT)
        delete_db_btn = Button(frame_for_buttons_start_window, text="Удалить БД", relief=GROOVE, width=30, cursor='X_cursor', command=self.delete_db)
        delete_db_btn.pack(side=LEFT)

        # sets the size of the window and places it in the center of the screen
        start_window.update_idletasks()  # Updates information after all frames are created
        s = start_window.geometry()
        s = s.split('+')
        s = s[0].split('x')
        width_main_window = int(s[0])
        height_main_window = int(s[1])

        w = start_window.winfo_screenwidth()
        h = start_window.winfo_screenheight()
        w = w // 2
        h = h // 2
        w = w - width_main_window // 2
        h = h - height_main_window // 2
        start_window.geometry('+{}+{}'.format(w, h))

        start_window.mainloop()


init_check = Gui()
init_check.init_start_window()


def check_directory():

    # ДО ЭТОГО МОМЕНТА ОПРЕДЕЛЯЮТСЯ СЛЕДУЮЩИЕ ПЕРЕМЕННЫЕ:
    # - translation_trigger
    # - transliteration_trigger
    # ПО ЭТОМУ ДАЛЬШЕ ПОКА ЧТО БУДУТ КОСТЫЛИ False/True. Дописать и заменить

    #
    # При выборе галочкой перевода через гугл, сразу проверять его работоспособность и выдавать сообщение в ГУИ
    #
    processed_books = []
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
                    processed_books.append(value)
    print('\nсчитанные данные:')
    for items in processed_books:
        print(items)


# check_directory()
