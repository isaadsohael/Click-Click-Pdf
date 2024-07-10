import sqlite3
import os
import sys


# https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


database = resource_path("resources/app_data.db")


def create_app_data():
    db = sqlite3.connect(database)

    cursor = db.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS static_data(last_opened_dir text, is_separated_folder, theme_style text)""")
    db.commit()
    cursor.execute("SELECT * FROM static_data")
    data = cursor.fetchall()
    if data:
        pass
    else:
        cursor.execute("INSERT INTO static_data VALUES ('', 'NO', 'White')")
        db.commit()
    db.close()


def query_app_data(query):
    db = sqlite3.connect(database)

    cursor = db.cursor()
    cursor.execute(f"SELECT {query} FROM static_data")
    data = cursor.fetchall()
    return data


def update_directory(directory):
    db = sqlite3.connect(database)

    cursor = db.cursor()
    cursor.execute("UPDATE static_data SET last_opened_dir = (?)", (directory,))
    db.commit()
    db.close()


def update_checkbox(is_separated):
    db = sqlite3.connect(database)

    cursor = db.cursor()
    cursor.execute("UPDATE static_data SET is_separated_folder = (?)", (is_separated,))
    db.commit()
    db.close()


def change_theme_style(theme):
    db = sqlite3.connect(database)
    cursor = db.cursor()
    cursor.execute("UPDATE static_data SET theme_style = (?)", (theme,))
    db.commit()
    db.close()
