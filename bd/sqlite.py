import os
import sqlite3
import uuid
from pathlib import Path

from tools import showMessageBox, count_words

current_dir = Path(__file__).parent
db_path = current_dir.parent / "bd" / "essay_bd"

connect = sqlite3.connect(db_path, check_same_thread=False)


def get_essays_by_genre(genre):
    genre_id = get_genre_id(genre)
    try:
        with connect:
            cursor = connect.cursor()
            request = """SELECT essay_id, title, filename 
                        FROM Essay_genre JOIN Genres ON genre_id = genres.id JOIN Essays ON essays.id = essay_id
                        WHERE genre_id = ? """
            cursor.execute(request, (genre_id,))
            essay_list = [i for i in cursor.fetchall()]
            return essay_list
    except sqlite3.Error as e:
        print(f"Database error in all_genres_on_essay: {e}")
        return


def get_essay_data_by_id(essay_id):
    try:
        with connect:
            cursor = connect.cursor()
            request = """SELECT DISTINCT essay_id, title, filename 
                        FROM Essay_genre JOIN Genres ON genre_id = genres.id JOIN Essays ON essays.id = essay_id
                        WHERE essay_id = ?"""
            cursor.execute(request, (essay_id,))
            essay_data = cursor.fetchall()[0]
            return essay_data
    except sqlite3.Error as e:
        print(f"Database error in all_genres_on_essay: {e}")
        return


def all_genres_on_essay(essay_id):
    try:
        with connect:
            cursor = connect.cursor()
            request = """SELECT name FROM Essay_genre JOIN Genres ON genre_id = id
                        WHERE essay_id = ? """
            cursor.execute(request, (essay_id,))
            genre_list = [i[0] for i in cursor.fetchall()]
            return genre_list
    except sqlite3.Error as e:
        print(f"Database error in all_genres_on_essay: {e}")
        return


def all_literature_on_essay(essay_id):
    try:
        with connect:
            cursor = connect.cursor()
            request = """SELECT title FROM Essay_literature JOIN Literatures ON literature_id = id
                        WHERE essay_id = ? """
            cursor.execute(request, (essay_id,))
            genre_list = [i[0] for i in cursor.fetchall()]
            return genre_list
    except sqlite3.Error as e:
        print(f"Database error in all_genres_on_essay: {e}")
        return


def get_all_genres():
    try:
        with connect:
            cursor = connect.cursor()
            cursor.execute('''SELECT name FROM Genres''')
            genres = [i[0].capitalize() for i in cursor.fetchall()]
        return sorted(set(genres))
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []


def get_genre_id(genre):
    genre = genre.lower()
    with connect:
        cursor = connect.cursor()
        genre_id = cursor.execute('''SELECT id FROM Genres WHERE name = ?''', (genre,)).fetchone()
    return genre_id[0] if genre_id else genre


def genre_exists(genre: str):
    return genre.capitalize() in get_all_genres()


def add_genre(genre):
    genre = genre.lower()
    try:
        with connect:
            cursor = connect.cursor()
            cursor.execute('''INSERT INTO Genres (name) VALUES (?)''', (genre,))
        return get_genre_id(genre)
    except sqlite3.Error as e:
        print(f"Database error in add genre: {e}")
        return


def get_literature_id(literature):
    with connect:
        cursor = connect.cursor()
        literature_id = cursor.execute('''SELECT id FROM Literatures WHERE title = ?''', (literature,)).fetchone()
    return literature_id[0] if literature_id else literature


def literature_exists(literature: str):
    all_literature = get_all_literature()
    return literature in all_literature


def get_all_literature():
    try:
        with connect:
            cursor = connect.cursor()
            cursor.execute('''SELECT title FROM Literatures''')
            literature = [i[0] for i in cursor.fetchall()]
        return sorted(set(literature))
    except sqlite3.Error as e:
        print(f"Database error in get_all_literature: {e}")
        return []


def add_literature(literature, author):
    try:
        with connect:
            if author_exists(author):
                cursor = connect.cursor()
                cursor.execute('''INSERT INTO Literatures (title, author_id) VALUES (?, ?)''',
                               (literature, get_author_id(author)))
            else:
                add_author(author)
                add_literature(literature, author)
            return get_literature_id(literature)
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return


def get_essay_id(filename):
    with connect:
        cursor = connect.cursor()
        essay_id = cursor.execute('''SELECT id FROM Essays WHERE filename = ?''', (filename,)).fetchone()
        return essay_id[0] if essay_id else None


def get_all_essays():
    try:
        with connect:
            cursor = connect.cursor()
            cursor.execute('''SELECT * FROM Essays''')
            essays = cursor.fetchall()
        return sorted(essays)
    except sqlite3.Error as e:
        print(f"Database error in get_all_essays: {e}")
        return []


def add_essay(title, text, selected_genres, selected_literature, unknown_literature='', author=''):
    selected_genres = [i.lower() for i in selected_genres]
    print(title, text, selected_genres, selected_literature, unknown_literature, author)
    try:
        with connect:
            cursor = connect.cursor()
            file_name = f"essay_{uuid.uuid4().hex}"  # essay_1a2b3c4d5e6f7890
            file_path = f'./essays/{file_name}.txt'

            try:
                with open(file_path, 'w', encoding='utf-8') as essay_file:
                    essay_file.write(text)
            except Exception as e:
                print(f'Error while saving text: {e}')
                showMessageBox(text='Ошибка сохранения', info=f"Не удалось сохранить файл: {e}")
                return

            into_essay_request = f"""INSERT INTO Essays (title, filename) VALUES (?, ?)"""
            cursor.execute(into_essay_request, (title, file_name))

            essay_id = get_essay_id(file_name)
            if not essay_id:
                os.remove(file_path)
                showMessageBox(text='Ошибка при сохранении!', info="Не удалось сохранить текст")
                return
            literature_ids = [get_literature_id(i) for i in selected_literature]

            if len(list(filter(lambda x: isinstance(x, int), literature_ids))) != len(literature_ids):
                # если в списке есть неизвестная литература
                if not author:
                    print('Не указан автор неизвестного произведения')
                    showMessageBox(f'Укажите автора "{unknown_literature}"')
                    cursor.execute('''DELETE FROM Essays WHERE id = ?''', (essay_id,))
                    return
                literature_id = add_literature(unknown_literature, author)
                print(f'Добавлена литература: {unknown_literature}, ее айди - {literature_id}')
                if literature_id:
                    literature_ids = list(filter(lambda x: isinstance(x, int), literature_ids))
                    literature_ids.append(literature_id)
            essay_literature_req = f"""INSERT INTO Essay_literature 
                        VALUES {', '.join(f'({essay_id}, {i})' for i in literature_ids)}"""
            cursor.execute(essay_literature_req)
            print("Сочинение и литература")
            genre_ids = [get_genre_id(i) for i in selected_genres]
            if filter(lambda x: not genre_exists(x), selected_genres):
                # если в списке есть неизвестные темы
                new_genres = [genre for genre in selected_genres if not genre_exists(genre)]
                for genre in new_genres:
                    genre_ids.append(add_genre(genre))
            genre_ids = list(filter(lambda x: isinstance(x, int), genre_ids))
            essay_genre_req = f"""INSERT INTO Essay_genre 
            VALUES {', '.join(f'({essay_id}, {i})' for i in genre_ids)}"""
            cursor.execute(essay_genre_req)
            print("Жанры и сочинение")
            return 1

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return


def load_essay_data(genre=None):
    essay_data = []

    if not genre:  # если не задали какой-то темы
        data = get_all_essays()
    else:
        data = get_essays_by_genre(genre)
    for essay in data:
        essay_id, title, filename = essay
        word_count = count_words(filename)
        genre_list = all_genres_on_essay(essay_id)
        essay_data.append((essay_id, title, genre_list, word_count))
    return essay_data


def get_all_authors():
    try:
        with connect:
            cursor = connect.cursor()
            cursor.execute('''SELECT name FROM Authors''')
            authors = [i[0] for i in cursor.fetchall()]
        return sorted(set(authors))
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []


def get_author_id(author):
    with connect:
        cursor = connect.cursor()
        author_id = cursor.execute('''SELECT id FROM Authors WHERE name = ?''', (author,)).fetchone()
        return author_id[0] if author_id else None


def author_exists(author):
    return author in get_all_authors()


def add_author(author):
    try:
        with connect:
            cursor = connect.cursor()
            cursor.execute('''INSERT INTO Authors (name) VALUES (?)''', (author,))
        return get_author_id(author)
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None


def all_data(essay_id):
    _, title, filename = get_essay_data_by_id(essay_id)
    filename += '.txt'
    file_path = current_dir.parent / "essays" / filename
    try:
        with open(file_path, encoding='utf8') as file:
            text = file.read()
        genres_list = all_genres_on_essay(essay_id)
        literatures_list = all_literature_on_essay(essay_id)
        result = {'title': title, 'text': text, 'genres': genres_list, 'literature_list': literatures_list}
        return result
    except FileNotFoundError:
        print(f'Файл {file_path} не найден')
        return
