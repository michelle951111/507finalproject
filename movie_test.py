import unittest
import get_imdb_data as gd
import store_data as sd
import process_data as pd
import sqlite3

DBNAME = 'movie.db'

class TestGetData(unittest.TestCase):

    def test_get_data(self):
        results=gd.get_top_250()
        self.assertIsInstance(results,list)
        self.assertIsInstance(results[1],dict)
        self.assertEqual(len(results), 250)

class TestDatabase(unittest.TestCase):

    def test_movie(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        statement = 'SELECT Movie FROM Movies'
        results = cur.execute(statement)
        result_list = results.fetchall()
        self.assertIn(('Pulp Fiction',), result_list)
        self.assertEqual(len(result_list), 250)

        statement = '''
                SELECT * FROM Movies
                WHERE Movie='Pulp Fiction';
                '''
        cur.execute(statement)
        for row in cur:
            self.assertEqual(row[2], 8.9)
            self.assertEqual(row[3], '(1994)')
            self.assertEqual(row[4], 'Quentin Tarantino')
            self.assertEqual(row[5], 107928762)
            self.assertEqual(row[6], 213928762)
        conn.close()

    def test_genre(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        statement = '''
                SELECT Genre FROM Genres;
                '''
        results = cur.execute(statement)
        result_list = results.fetchall()
        self.assertIn(('Adventure',), result_list)
        self.assertEqual(len(result_list), 21)


    def test_join(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        statement = '''
            SELECT Genre
            From Movies_Genres
            JOIN Genres on Genres.Id = Movies_Genres.GenreId
            JOIN Movies on Movies.Id = Movies_Genres.MovieId
            WHERE Movie='Inception';
        '''
        results = cur.execute(statement)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 4)
        self.assertIn(('Action',), result_list)
        self.assertIn(('Adventure',), result_list)
        self.assertIn(('Sci-Fi',), result_list)
        self.assertIn(('Thriller',), result_list)
        conn.close()

class TestProcessData(unittest.TestCase):

    def test_show_number(self):
        result=pd.show_number()
        self.assertEqual(len(result),21)
        self.assertEqual(result['Crime'],55)

    def test_show_rating(self):
        result=pd.show_rating()
        self.assertEqual(len(result),21)
        self.assertEqual(result['Crime'],'8.32')

    def test_show_gross(self):
        result=pd.show_gross()
        self.assertEqual(len(result),21)
        self.assertEqual(result['Crime']['US Gross'],'85501162.35')
        self.assertEqual(result['Crime']['Global Gross'],'206184429.56')


    def test_gross_rating(self):
        result=pd.gross_rating('Crime')
        self.assertEqual(len(result),50)
        self.assertEqual(result[1]['Movie'],'The Godfather')
        self.assertEqual(result[1]['Gross'],245066411)
        self.assertEqual(result[1]['Rating'],9.2)

    def test_gross_share(self):
        self.assertEqual(pd.gross_share('The Godfather'),(134966411, 245066411))

if __name__ == '__main__':
    unittest.main()
