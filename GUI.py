from read_and_write import *
from tkinter import *
from tkinter import font
import re
from googletrans import Translator


# + вот сюда будут приходить все приколдэсы из функций обработки
# + отсюда уходит запрос на считку директорий
# + сюда приходит ответ по количеству файлов и ветвлению
# человек выбирает нужные параметры, работая со сгенерированным словарём
# + отправляет обратно данные для переработки через циклическую функцию в препроцессинг
# + если директория одна, то циклическая функция отрабатывает только 1 цикл

class Gui:
    """Графический интерфейс"""

    def __init__(self):
        self.text = None
        self.googletrans_status = 'first_press'
        self.label = None
        self.entry = None
        self.pattern = None
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

    def db_generation(self):
        self.start_window.destroy()
        self.asc_generation_window.destroy()

        def on_closing():
            self.db_generation_window.destroy()
            self.init_start_window()

        def check_directory():

            # Задаёт стили текста для отображения в ГУИ
            load_text.tag_configure('highlightline', background='grey75', borderwidth=2, relief='groove',
                                    bgstipple='gray50')
            load_text.tag_configure('red', background=self.db_generation_window["bg"], foreground='red',
                                    justify=CENTER,
                                    borderwidth=1, relief='ridge')
            load_text.tag_configure('green', background='grey85', foreground='green', justify=CENTER,
                                    borderwidth=2,
                                    relief='groove')
            load_text.tag_configure('bg_gray_1', background='grey95', borderwidth=3, relief='sunken',
                                    bgstipple='gray25',
                                    lmargin1=50, lmargin2=50)
            load_text.tag_configure('bg_for_directory', background='grey95', borderwidth=3, relief='sunken',
                                    lmargin2=168,
                                    bgstipple='gray25')

            direct = ask_and_check_directory()
            load_text['state'] = NORMAL

            if direct == "Window were closed":
                # КОСТЫЛЬ ДО МОМЕНТА СОЗДАНИЯ ИНТЕРФЕЙСА
                print('Окно было закрыто')
                return

            elif direct == "Can't read files":
                choose_directory_btn['background'] = 'gray95'
                load_text.delete(0.0, END)
                load_text.insert(END, '\n')
                load_text.insert(END, 'В ВЫБРАННОЙ ДИРЕКТОРИИ ОТСУТСТВУЮТ ФАЙЛЫ!!!\n', 'red')
                load_text.insert(END, '\n')
                return

            elif direct == "No files read":
                load_text.delete(0.0, END)
                load_text.insert(END, '\n')
                load_text.insert(END, 'СИСТЕМА СМОГЛА РАСПОЗНАТЬ ТОЛЬКО ПАПКИ В ВЫБРАННОЙ ДИРЕКТОРИИ!!!\n', 'red')
                load_text.insert(END, '\n')
                choose_directory_btn['background'] = 'gray95'
                return

            else:
                # Считает количество директорий и файлов в них
                number_of_files = 0
                number_of_directories = 0
                for files in direct.values():
                    for file_number in files:
                        number_of_files += file_number['files_number']
                        number_of_directories += 1

                # Очистка интерфейса и загрузка в него данных
                load_text.delete(0.0, END)
                load_text.insert(END, 'СЧИТАННЫЕ ДИРЕКТОРИИ\n', 'red')
                load_text.insert(END, '\nколичество директорий:  ' + str(number_of_directories) +
                                 ' (обработано)\nколичество файлов:      ' + str(number_of_files) + '\n\n',
                                 'bg_gray_1')
                load_text.insert(END, '\n')

                dir_counter = 0
                empty_dir_counter = 0
                dir_without_files = {}
                for folder in direct.keys():
                    for elements in range(0, len(direct[folder])):
                        if direct[folder][elements]['files_number'] != 0:
                            dir_counter += 1
                            load_text.insert(END, 'ДИРЕКТОРИЯ №' + str(dir_counter) + '\n', "green")
                            load_text.insert(END, '\n', 'bg_gray_1')
                            load_text.insert(END, ' Название папки:    ', "highlightline")
                            path_name_reversed = str(direct[folder][elements]['dirpath'])[::-1]
                            if '\\' in path_name_reversed:
                                folder_name_reversed = path_name_reversed[:path_name_reversed.find('\\')]
                            else:
                                folder_name_reversed = path_name_reversed[:path_name_reversed.find('/')]
                            folder_name = folder_name_reversed[::-1]
                            load_text.insert(END, '\t' + folder_name + '\n', 'bg_for_directory')
                            load_text.insert(END, '\n', 'bg_gray_1')
                            load_text.insert(END, ' Количество файлов: ', "highlightline")
                            load_text.insert(END, '\t' + str(direct[folder][elements]['files_number']) + '\n',
                                             'bg_for_directory')
                            load_text.insert(END, '\n', 'bg_gray_1')
                            load_text.insert(END, ' Адрес:             ', "highlightline")
                            load_text.insert(END, '\t' + str(direct[folder][elements]['dirpath']) + '\n\n',
                                             'bg_for_directory')
                            load_text.insert(END, '\n')
                        else:
                            empty_dir_counter += 1
                            dir_without_files[str(empty_dir_counter)] = direct[folder][elements]['dirpath']

                # Создаёт графическое представление для наличия директорий без файлов, которые будут игнорироваться
                if dir_without_files:
                    dir_without_files_for_del = {}
                    for key, filename in dir_without_files.items():
                        readen_files = os.walk(filename)
                        for dirpath, dirnames, filenames in readen_files:
                            if filenames:
                                dir_without_files_for_del[key] = filename
                    for keys in dir_without_files_for_del.keys():
                        del dir_without_files[keys]

                    if len(dir_without_files) == 1:
                        load_text.insert(END, 'ПУСТАЯ ДИРЕКТОРИЯ (' + str(len(dir_without_files)) + ')\n', "red")
                        load_text.insert(END, '\n', 'bg_gray_1')
                        load_text.insert(END, ' Название папки, которая будет проигнорирована: ', "highlightline")
                        load_text.insert(END, '\n', 'bg_gray_1')
                    elif len(dir_without_files) == 0:
                        pass
                    else:
                        load_text.insert(END, 'ПУСТЫЕ ДИРЕКТОРИИ (' + str(len(dir_without_files)) + ')\n', "red")
                        load_text.insert(END, '\n', 'bg_gray_1')
                        load_text.insert(END, ' Названия папок, которые будут проигнорированы: ', "highlightline")
                        load_text.insert(END, '\n', 'bg_gray_1')

                    if len(dir_without_files) >= 1:
                        folder_counter = 0
                        for path in dir_without_files.values():
                            folder_counter += 1
                            path_name_reversed = str(path)[::-1]
                            if '\\' in path_name_reversed:
                                folder_name_reversed = path_name_reversed[:path_name_reversed.find('\\')]
                            else:
                                folder_name_reversed = path_name_reversed[:path_name_reversed.find('/')]
                            folder_name = folder_name_reversed[::-1]
                            load_text.insert(END, '\n' + str(folder_counter) + ') ' + str(folder_name),
                                             'bg_gray_1')
                        load_text.insert(END, '\n\n', 'bg_gray_1')
                choose_directory_btn['background'] = 'lightgreen'
            load_text['state'] = DISABLED

            #
            # ЗАПИСЫВАТЬ ИЗАНЧАЛЬНЫЙ ПУТЬ, КОТОРЫЙ ВЫБРАЛ ПОЛЬЗОВАТЕЛЬ И СОХРАНЯТЬ ЕГО В БД ДЛЯ ВОЗМОЖНОСТИ
            # АРХИВИРОВАНИЯ И ДР ВЗАИМОДЕЙСТВИЙ
            #

            #
            # ТУТ ПОЛЬЗОВАТЕЛЬ ВЫБИРАЕТ ТРЕБУЕМЫЕ ПАПКИ ДЛЯ ЗАГРУЗКИ В БАЗУ. ВЫБОР ПО ФАЙЛАМ, НАВЕРНОЕ, ДЕЛАТЬ НЕ СТОИТ.
            # ЭТО БУДЕТ ИЗБЫТОЧНО. ТЕМ БОЛЕЕ БАЗА ДАННЫХ БУДЕТ РАБОТАТЬ В ПЕРВУЮ ОЧЕРЕДЬ С ДИРЕКТОРИЯМИ ЦЕЛИКОМ
            #

            # ДО ЭТОГО МОМЕНТА ОПРЕДЕЛЯЮТСЯ СЛЕДУЮЩИЕ ПЕРЕМЕННЫЕ:
            # - translation_trigger
            # - transliteration_trigger
            # ПО ЭТОМУ ДАЛЬШЕ ПОКА ЧТО БУДУТ КОСТЫЛИ False/True. Дописать и заменить

            #
            # При выборе галочкой перевода через гугл, сразу проверять его работоспособность и выдавать сообщение в ГУИ
            #

            #
            # КОСТЫЛЬ. СЧИТАЕМ, ЧТО ПОЛЬЗОВАТЕЛЬ ВЫБРАЛ ВСЕ ДИРЕКТОРИИ
            #

            """
            processed_books = []
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
        self.db_generation_window["bg"] = 'gray90'

        # frame for the main interface
        frame_for_text_db_generation = LabelFrame(self.db_generation_window)
        frame_for_text_db_generation.pack(side=LEFT)

        frame_for_button_open_folder = LabelFrame(self.db_generation_window)
        frame_for_button_open_folder.pack(side=TOP, fill=X, pady=15)

        frame_for_translation = LabelFrame(self.db_generation_window)
        frame_for_translation.pack(side=TOP, fill=X, pady=8)

        frame_for_checkbox_translation = LabelFrame(frame_for_translation)
        frame_for_checkbox_translation.pack(side=TOP, fill=X)

        frame_for_checkbox_translation_text = LabelFrame(frame_for_translation)
        frame_for_checkbox_translation_text.pack(side=TOP, fill=X)

        frame_for_transliteration = LabelFrame(self.db_generation_window)
        frame_for_transliteration.pack(side=TOP, fill=X, pady=8)

        frame_for_checkbox_transliteration = LabelFrame(frame_for_transliteration)
        frame_for_checkbox_transliteration.pack(side=TOP, fill=X)

        frame_for_checkbox_transliteration_text = LabelFrame(frame_for_transliteration)
        frame_for_checkbox_transliteration_text.pack(side=TOP, fill=X)

        frame_for_db_name = LabelFrame(self.db_generation_window)
        frame_for_db_name.pack(side=TOP, fill=X, pady=8)

        frame_for_db_description = LabelFrame(self.db_generation_window)
        frame_for_db_description.pack(side=TOP, fill=X, pady=8)

        frame_for_start_btn = LabelFrame(self.db_generation_window)
        frame_for_start_btn.pack(side=TOP, fill=X)

        load_text = Text(frame_for_text_db_generation, width=70, height=30, cursor='arrow', background='ghost white',
                         wrap=WORD)
        load_text.pack(side=LEFT)
        load_text['state'] = DISABLED

        choose_directory_btn = Button(frame_for_button_open_folder, text="Выбрать папку", relief=GROOVE, width=30,
                                      command=check_directory)
        choose_directory_btn.pack(side=TOP)

        ## написать функции для проверки английского языка!!! Сделать подсветку зеленым после проверки
        ## сделать так, чтобы переменные були передавались в циклическую функцию
        ## прописать кнопку генерации данных в функции предобработки

        ## галочки транслита и перевода
        ##
        translation_variable = BooleanVar()
        transliteration_variable = BooleanVar()

        def check_translation():

            def status_check():
                self.googletrans_status = False
                translator = Translator()
                trans = translator.translate('check', dest='ru')
                translated_tag = trans.text
                print(translated_tag)

                if translated_tag:
                    self.googletrans_status = True
                    label_for_translation['text'] = 'подключено: 🗸'
                    label_for_translation['background'] = 'lightgreen'
                    frame_for_checkbox_translation_text['background'] = 'lightgreen'
                    frame_for_checkbox_translation['background'] = 'lightgreen'
                    checkbutton_translation['background'] = 'lightgreen'
                else:
                    label_for_translation['background'] = 'lightcoral'
                    label_for_translation['text'] = 'Проверьте Internet соединение!!!'
                    frame_for_checkbox_translation_text['background'] = 'lightcoral'
                    frame_for_checkbox_translation['background'] = 'gray95'
                    checkbutton_translation['background'] = 'gray95'
                    translation_variable.set(False)

                return translated_tag

            if translation_variable.get():
                label_for_translation['background'] = 'gray95'
                label_for_translation['text'] = 'проверка работы сервисов: ...'
                frame_for_checkbox_translation_text.after(400, status_check)
                frame_for_checkbox_translation_text['background'] = 'gray95'
                if self.googletrans_status == 'first_press':
                    pass
                if not self.googletrans_status:
                    print(self.googletrans_status)
                    label_for_translation['background'] = 'lightcoral'
                    label_for_translation['text'] = 'Проверьте Internet соединение!!!'
                    frame_for_checkbox_translation_text['background'] = 'lightcoral'
                    frame_for_checkbox_translation['background'] = 'gray95'
                    checkbutton_translation['background'] = 'gray95'
                    translation_variable.set(False)

            else:
                label_for_translation['background'] = 'gray95'
                label_for_translation['text'] = 'статус подключения модуля: ❎'
                checkbutton_translation['background'] = 'gray95'
                frame_for_checkbox_translation_text['background'] = 'gray95'
                frame_for_checkbox_translation['background'] = 'gray95'

        def check_transliteration():
            def status_change():
                label_for_transliteration['background'] = 'lightgreen'
                label_for_transliteration['text'] = 'подключено: 🗸'
                frame_for_checkbox_transliteration_text['background'] = 'lightgreen'

            if transliteration_variable.get():
                label_for_transliteration['background'] = 'gray95'
                label_for_transliteration['text'] = 'проверка работы сервисов: ...'
                label_for_transliteration.after(600, status_change)
                frame_for_checkbox_transliteration_text['background'] = 'gray95'

                checkbutton_transliteration['background'] = 'lightgreen'
                frame_for_checkbox_transliteration['background'] = 'lightgreen'
            else:
                label_for_transliteration['background'] = 'gray95'
                label_for_transliteration['text'] = 'статус подключения модуля: ❎'
                frame_for_checkbox_transliteration_text['background'] = 'gray95'
                checkbutton_transliteration['background'] = 'gray95'
                frame_for_checkbox_transliteration['background'] = 'gray95'

        checkbutton_translation = Checkbutton(frame_for_checkbox_translation, text='Перевод (сервисы google)',
                                              command=check_translation,
                                              variable=translation_variable, onvalue=True, offvalue=False)
        checkbutton_translation.pack(side=LEFT, pady=10)

        label_for_translation = Label(frame_for_checkbox_translation_text, text='статус подключения модуля: ❎')
        label_for_translation.pack(side=TOP, pady=2)

        checkbutton_transliteration = Checkbutton(frame_for_checkbox_transliteration, text='Транслитерация текста',
                                                  command=check_transliteration,
                                                  variable=transliteration_variable, onvalue=True, offvalue=False)
        checkbutton_transliteration.pack(side=LEFT, pady=10)

        label_for_transliteration = Label(frame_for_checkbox_transliteration_text,
                                          text='статус подключения модуля: ❎')
        label_for_transliteration.pack(side=TOP, pady=2)

        translation_variable.set(False)                    ####   переменные були, по которым нужно смотреть был ли выбор перевода/транслитерации
        transliteration_variable.set(False)
        ##
        ##

        ## меню ввода названия директории (((добавить переменную названия базы данных)))!
        ##
        def validate_dbname(dbname):
            if not dbname:
                self.entry['background'] = 'lightcoral'
            else:
                self.entry['background'] = 'lightgreen'
            return self.pattern.match(dbname) is not None

        def change_color_error():
            def change_back():
                if self.entry.get():
                    self.entry['background'] = 'lightgreen'
            self.entry['background'] = 'lightcoral'
            self.entry.after(400, change_back)

        self.pattern = re.compile("^\w{0,30}$")
        self.label = Label(frame_for_db_name, text="Введите название базы данных:")
        vcmd = (frame_for_db_name.register(validate_dbname), "%P")
        self.entry = Entry(frame_for_db_name, validate="key",
                           validatecommand=vcmd, invalidcommand=change_color_error, background='white')
        self.label.pack()
        self.entry.pack(side=TOP, padx=10, pady=10, fill=X)
        ##
        ##

        ##   текст описания базы данных!!
        ##
        label_for_description = Label(frame_for_db_description, text="Описание БД (опционально):")
        label_for_description.pack(side=TOP)
        text_of_description = Text(frame_for_db_description, background='white', width=25, height=2)
        text_of_description.pack(side=TOP, padx=10, pady=10)
        ##
        ##

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

    def ask_db_generation(self):
        """Запускает стартовое окно с запросом на генерацию баз данных"""
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
        open_db_generation_btn = Button(frame_for_buttons_start_window, text="Создать новую", relief=GROOVE, width=30,
                                        command=self.db_generation)
        open_db_generation_btn.pack(side=TOP)
        from_archive_btn = Button(frame_for_buttons_start_window, text="Разархивировать", relief=GROOVE, width=30,
                                  state=DISABLED)
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
        self.open_btn = Button(frame_for_buttons_start_window, text="Открыть", relief=GROOVE, width=30,
                               command=self.open_db, state=DISABLED)
        self.open_btn.pack(side=LEFT)
        self.new_db_btn = Button(frame_for_buttons_start_window, text="Создать новую", relief=GROOVE, width=30,
                                 command=self.ask_db_generation)
        self.new_db_btn.pack(side=LEFT)
        self.delete_db_btn = Button(frame_for_buttons_start_window, text="Удалить", relief=GROOVE, width=30,
                                    cursor='X_cursor', command=self.delete_db, state=DISABLED)
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
