import requests
import json
from bs4 import BeautifulSoup
import plotly.plotly as py
import plotly.graph_objs as go
import sqlite3

DBNAME = 'movie.db'
MOVIEJSON = 'movies_dict.json'

def init_database(DBNAME):
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    statement = '''
        DROP TABLE IF EXISTS 'Movies';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Genres';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Movies_Genres';
    '''
    cur.execute(statement)


    statement = '''
        CREATE TABLE IF NOT EXISTS 'Movies' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Movie' TEXT,
            'Rating' REAL,
            'Year' TEXT,
            'Director' TEXT,
            'UsGross' INT,
            'GlobalGross' INT
        );
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE IF NOT EXISTS 'Genres' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Genre' TEXT
        );
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE IF NOT EXISTS 'Movies_Genres' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'MovieId' INT,
            'GenreId' INT
        );
    '''
    cur.execute(statement)

    conn.commit()
    conn.close()

def insert_data(MOVIEJSON):
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    with open(MOVIEJSON) as json_data:
        movies_data = json.load(json_data)
        all_genres=[]
        for movie in movies_data:
            insert_data = (movie['title'],movie['rating'],movie['year'],movie['director'],movie['us gross'],movie['global gross'])
            statement = 'INSERT INTO "Movies" (Movie,Rating,Year,Director,UsGross,GlobalGross)'
            statement += 'VALUES (?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insert_data)
            for genre in movie['genres']:
                genre_f = genre.replace(' ','')
                if genre_f not in all_genres:
                    all_genres.append(genre_f)

        for genre in all_genres:
            insert_data = (genre,)
            statement = 'INSERT INTO "Genres" (Genre)'
            statement += 'VALUES (?)'
            cur.execute(statement, insert_data)

        for movie in movies_data:
            for genre in movie['genres']:
                genre_f = genre.replace(' ','')
                insert_data = (movie['title'],genre_f)
                statement = 'INSERT INTO "Movies_Genres" (MovieId,GenreId)'
                statement += 'VALUES ((SELECT Id from "Movies" WHERE Movie=?),(SELECT Id from "Genres" WHERE Genre=?))'
                cur.execute(statement, insert_data)

    conn.commit()
    conn.close()

if __name__=="__main__":
    init_database(DBNAME)
    insert_data(MOVIEJSON)
