import os
import sqlite3
from tkinter import filedialog as fd

folder_name = fd.askdirectory() # запрашивает директорию

db = sqlite3.connect('something.db')  # создает базу данных
sql = db.cursor()  # переменная для взаимодействия с базой

sql.execute("""CREATE TABLE IF NOT EXISTS something (
    name TEXT
)""")  # создает таблицу

sql.execute("DELETE FROM something") # зачищает данные из таблицы

# for root, dirs, files in os.walk("."):  # считывает всё в корневой папке!!!!!

for root, dirs, files in os.walk(folder_name):
    for filename in files:

        # добавление данных
        sql.execute("INSERT INTO something VALUES(?)", (filename, ))
        db.commit()

        # вывод данных

sql.execute("SELECT rowid, * FROM something")

for timer in range(0, 48):
    print(sql.fetchone())

db.commit()  # сохраняет изменения
db.close()
