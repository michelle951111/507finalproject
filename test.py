import unittest
import get_imdb_data
import movie
import sqlite3

DBNAME = 'movie.db'

conn = sqlite3.connect(DBNAME)
cur = conn.cursor()

statement = 'SELECT Movie FROM Movies'
results = cur.execute(statement)
result_list = results.fetchall()
#self.assertIn(('Pulp Fiction',), result_list)
#self.assertEqual(len(result_list), 250)

statement = '''
        SELECT * FROM Movies
        WHERE Movie='Pulp Fiction';
        '''
cur.execute(statement)
for row in cur:
    print(row[1],row[2])
conn.close()
