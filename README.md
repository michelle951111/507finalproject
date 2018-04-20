# Brief user guide:
  1. The first step: Run get_imdb_data.py to get cache.json and movies_dict.json_data
  2. The second step: Run store_data.py to build a database movie.db
  3. Then you can run process_data.py to interact with this program and see some interesting insights of relationships of genre, rating, gross of movies. Please input valid command in your commandline.
      * valid commands:
         * number
             * show number of movies in each genre among the 250 top rated movies
         * rating
             * show average rating of movies in each genre among the 250 top rated movies
         * gross
             * show average gross in both USA and the world of movies in each genre among the 250 top rated movies
         * <'a genre'>
             * show the rating and global gross of movies in the genre
             * available only if there is an active result set
             * valid input: a genre listed in a result set
         * <'a movie'>
             * show the gross in USA and the gross in other regions of the movie
             * available after there is an active result set of <genre name> command
             * valid input: a number listed in a result set of <genre name> command
         * exit
             * exits the program
         * help
             * lists available commands (these instructions)

# Data sources:
  * Use BeautifulSoup Module to scrape and crawl the pages of IMDB website. Start form the list of 250 top rated movies on https://www.imdb.com/chart/top?ref_=nv_mv_250_6 and crawl each page of movie from the link in this page, such as https://www.imdb.com/title/tt0111161/ to get rating, box office and genre, and other related information( released year, director)

# Getting started info for plotly:
  * Plotly https://plot.ly/ is a graphing service that you can work with from Python.
  Look at start instruction https://plot.ly/python/getting-started/ , Follow the instructions, install the package, create an account and import plotly in your local enviroment.

# Brief description of how my code is structured:
  * My code is composed of three parts:
  1. get_imdb_data.py is for requesting and getting movie data from IMDB website. The webpage data is cached in cache.json, which I can get data from this file later. And the data I need of movies is cached in movies_dict.json, including the movie name, genre, released year, director, gross in USA, and gross in the world.
  2. store_data.py is for building a database and inserting data to it. The movie.db database includes three table: Movies, Genres and Movies_Genres. movies and genres are in many-to-many relationship and the Movies_Genres is the bridge table.
  3. process_data.py is the main part that process data and show visualization as well as enable users to interact with the program. There are five functions and one class to process data and generate plotly graphs:
       * Class Movie(): define the movie object, which has attributes of title, rating, director, year, usgross and global gross. It will be printed as a brief intro of this movie.
       * show_number(): show the number of movies in each genre among the 250 top movies.
       * show_rating(): show average rating of movies in each genre among the 250 top rated movies
       * show_gross(): show average gross in both USA and the world of movies in each genre among the 250 top rated movies
       * gross_rating(genre): show the rating and global gross of movies in the genre
       * gross_share(movie): show the gross in USA and the gross in other regions of the movie
