import sqlite3

db = sqlite3.connect('books.db')  # создает базу данных
sql = db.cursor()  # переменная для взаимодействия с базой

sql.execute("""CREATE TABLE IF NOT EXISTS books (
    id INTEGER,
    name TEXT,
    extension TEXT,
    year INTEGER,
    tags TEXT,
    transliterated_tags TEXT,
    user_tags TEXT,
    import_year INTEGER,
    import_month INTEGER,
    import_day INTEGER,
    import_hour INTEGER,
    import_minute INTEGER,
    last_open_year INTEGER,
    last_open_month INTEGER,
    last_open_day INTEGER,
    score INTEGER
)""")  # создает таблицу


# добавление данных
sql.execute("INSERT INTO books VALUES (2, 'doesnt matter', 'pdf', '2018', 'qqq nvc pls wow', 'ыьер тщту зды цщц', 'number two book', 2022, 6, 11, 13, 59, 2022, 7, 18, 3)")

# вывод данных
sql.execute("SELECT rowid, * FROM books")
print(sql.fetchall()) # вывести всё полученное от предыдущей команды


db.commit()  # сохраняет изменения
db.close()
