import tkinter

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
        self.db_generation_window = None
        self.start_window = None
        self.delete_db_btn = None
        self.open_btn = None
        self.asc_generation_window = None
        self.new_db_btn = None
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

    def db_generation(self):
        self.start_window.destroy()
        self.asc_generation_window.destroy()

        def on_closing():
            self.db_generation_window.destroy()
            self.init_start_window()

        def check_directory():

            text.delete(0.0, END)
            text.tag_configure('highlightline', background='grey70', borderwidth=2, relief='groove')
            text.tag_configure('red', foreground='red', justify=CENTER, background='grey80', borderwidth=2, relief='groove')
            text.tag_configure('green', foreground='green', background='grey85', justify=CENTER, borderwidth=2, relief='groove')
            text.tag_configure('bg_gray_1', background='grey95', borderwidth=3, relief='sunken')

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
            text.insert(END, 'СЧИТАННЫЕ ДИРЕКТОРИИ\n', 'red')
            text.insert(END, '\n')
            dir_counter = 0
            for folder in direct.keys():
                for elements in range(0, len(direct[folder])):
                    dir_counter += 1
                    text.insert(END, 'ДИРЕКТОРИЯ ' + str(dir_counter) + '\n', "green")
                    text.insert(END, '\n', 'bg_gray_1')
                    text.insert(END, ' Название папки:    ', "highlightline")
                    path_name_reversed = str(direct[folder][elements]['dirpath'])[::-1]
                    if '\\' in path_name_reversed:
                        folder_name_reversed = path_name_reversed[:path_name_reversed.find('\\')]
                    else:
                        folder_name_reversed = path_name_reversed[:path_name_reversed.find('/')]
                    folder_name = folder_name_reversed[::-1]
                    text.insert(END, '\t' + folder_name + '\n', 'bg_gray_1')
                    text.insert(END, '\n', 'bg_gray_1')
                    text.insert(END, ' Адрес:             ', "highlightline")
                    text.insert(END, '\n', 'bg_gray_1')
                    text.insert(END, '\t' + str(direct[folder][elements]['dirpath']) + '\n', 'bg_gray_1')
                    text.insert(END, '\n', 'bg_gray_1')
                    text.insert(END, ' Количество файлов: ', "highlightline")
                    text.insert(END, '\t' + str(direct[folder][elements]['files_number']) + '\n\n', 'bg_gray_1')
                    text.insert(END, '\n')
            text['state'] = DISABLED

            #
            # ТУТ ПОЛЬЗОВАТЕЛЬ ВЫБИРАЕТ ТРЕБУЕМЫЕ ПАПКИ ДЛЯ ЗАГРУЗКИ В БАЗУ. ВЫБОР ПО ФАЙЛАМ, НАВЕРНОЕ, ДЕЛАТЬ НЕ СТОИТ.
            # ЭТО БУДЕТ ИЗБЫТОЧНО. ТЕМ БОЛЕЕ БАЗА ДАННЫХ БУДЕТ РАБОТАТЬ В ПЕРВУЮ ОЧЕРЕДЬ С ДИРЕКТОРИЯМИ ЦЕЛИКОМ
            #

            #
            # КОСТЫЛЬ. СЧИТАЕМ, ЧТО ПОЛЬЗОВАТЕЛЬ ВЫБРАЛ ВСЕ ДИРЕКТОРИИ
            #
            """
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
            """

        self.db_generation_window = Tk()
        self.db_generation_window.title("Режим")
        # команда при закрытии окна
        self.db_generation_window.protocol("WM_DELETE_WINDOW", on_closing)

        # disables the ability to zoom the page
        self.db_generation_window.resizable(False, False)

        # frame for the main interface
        frame_for_text_db_generation = LabelFrame(self.db_generation_window)
        frame_for_text_db_generation.pack(side=LEFT)
        frame_for_buttons_db_generation = LabelFrame(self.db_generation_window)
        frame_for_buttons_db_generation.pack(side=TOP)

        text = Text(frame_for_text_db_generation, width=70, height=30, cursor='arrow')
        text.pack(side=LEFT)

        Button(frame_for_buttons_db_generation, text="Выбрать папку", command=check_directory).pack(side=TOP)

        # sets the size of the window and places it in the center of the screen
        self.db_generation_window.update_idletasks()  # Updates information after all frames are created
        s = self.db_generation_window.geometry()
        s = s.split('+')
        s = s[0].split('x')
        width_window = int(s[0])
        height_window = int(s[1])

        w = self.db_generation_window.winfo_screenwidth()
        h = self.db_generation_window.winfo_screenheight()
        w = w // 2
        h = h // 2
        w = w - width_window // 2
        h = h - height_window // 2
        self.db_generation_window.geometry('+{}+{}'.format(w, h))

    # запускает стартовое окно с запросом на генерацию баз данных
    def ask_db_generation(self):
        self.open_btn['state'] = DISABLED
        self.new_db_btn['state'] = DISABLED
        self.delete_db_btn['state'] = DISABLED

        def on_closing():
            self.asc_generation_window.destroy()
            self.new_db_btn['state'] = NORMAL

        self.asc_generation_window = Tk()
        self.asc_generation_window.title("Режим")
        # команда при закрытии окна
        self.asc_generation_window.protocol("WM_DELETE_WINDOW", on_closing)

        # disables the ability to zoom the page
        self.asc_generation_window.resizable(False, False)

        # frame for the interface
        frame_for_buttons_start_window = LabelFrame(self.asc_generation_window)
        frame_for_buttons_start_window.pack(side=TOP)

        # outputs the information about the absolute error in the GUI
        open_db_generation_btn = Button(frame_for_buttons_start_window, text="Создать новую", relief=GROOVE, width=30, command=self.db_generation)
        open_db_generation_btn.pack(side=TOP)
        from_archive_btn = Button(frame_for_buttons_start_window, text="Разархивировать", relief=GROOVE, width=30, state=DISABLED)
        from_archive_btn.pack(side=TOP)

        # sets the size of the window and places it in the center of the screen
        self.asc_generation_window.update_idletasks()  # Updates information after all frames are created
        s = self.asc_generation_window.geometry()
        s = s.split('+')
        s = s[0].split('x')
        width_window = int(s[0])
        height_window = int(s[1])

        w = self.asc_generation_window.winfo_screenwidth()
        h = self.asc_generation_window.winfo_screenheight()
        w = w // 2
        h = h // 2
        w = w - width_window // 2
        h = h - height_window // 2
        self.asc_generation_window.geometry('+{}+{}'.format(w, h))
        self.asc_generation_window.mainloop()

    def delete_db(self):
        print('DDDDDDDDDDDDDDDDDDDDDDD')

    def init_start_window(self):
        """Запускает первичное окно с возможностью первичного просмотра баз данных, добавления, удаления, открытия"""

        self.start_window = Tk()
        self.start_window.title("Базы данных")
        large_font = font.Font(weight='bold', size=12)

        # disables the ability to zoom the page
        self.start_window.resizable(False, False)

        # frame for the main interface
        frame_for_list_of_dbs = LabelFrame(self.start_window)
        frame_for_list_of_dbs.pack(side=TOP)
        frame_for_buttons_start_window = LabelFrame(self.start_window)
        frame_for_buttons_start_window.pack(side=TOP)

        self.box = Listbox(frame_for_list_of_dbs, width=71, selectbackground='grey70', font=large_font)
        self.box.pack(side=LEFT)
        scroll = Scrollbar(frame_for_list_of_dbs, command=self.box.yview)
        scroll.pack(side=LEFT, fill=Y)
        self.box.config(yscrollcommand=scroll.set)

        # outputs the information about the absolute error in the GUI
        self.open_btn = Button(frame_for_buttons_start_window, text="Открыть", relief=GROOVE, width=30, command=self.open_db, state=DISABLED)
        self.open_btn.pack(side=LEFT)
        self.new_db_btn = Button(frame_for_buttons_start_window, text="Создать новую", relief=GROOVE, width=30, command=self.ask_db_generation)
        self.new_db_btn.pack(side=LEFT)
        self.delete_db_btn = Button(frame_for_buttons_start_window, text="Удалить", relief=GROOVE, width=30, cursor='X_cursor', command=self.delete_db, state=DISABLED)
        self.delete_db_btn.pack(side=LEFT)

        # sets the size of the window and places it in the center of the screen
        self.start_window.update_idletasks()  # Updates information after all frames are created
        s = self.start_window.geometry()
        s = s.split('+')
        s = s[0].split('x')
        width_main_window = int(s[0])
        height_main_window = int(s[1])

        w = self.start_window.winfo_screenwidth()
        h = self.start_window.winfo_screenheight()
        w = w // 2
        h = h // 2
        w = w - width_main_window // 2
        h = h - height_main_window // 2
        self.start_window.geometry('+{}+{}'.format(w, h))

        self.start_window.mainloop()


init_check = Gui()
init_check.init_start_window()
