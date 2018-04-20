
# Data sources:
  * Use BeautifulSoup Module to scrape and crawl the pages of IMDB website. Start form the list of 250 top rated movies on https://www.imdb.com/chart/top?ref_=nv_mv_250_6 and crawl each page of movie from the link in this page, such as https://www.imdb.com/title/tt0111161/ to get rating, box office and genre, and other related information( released year, director)

# Getting started info for plotly:
  * Plotly https://plot.ly/ is a graphing service that you can work with from Python.
  Look at start instruction https://plot.ly/python/getting-started/ , Follow the instructions, install the package, create an account and import plotly in your local enviroment.

# Brief description of how my code is structured:


# Brief user guide:
  1. Run get_imdb_data.py to get cache.json and movies_dict.json_data
  2. Run store_data.py to build a database movie.db
  3. Run process_data.py to interact with this program and see some interesting insights of relationships of genre, rating, gross of movies. Please input valid command in your commandline.
      * valid commands:
         * number
             * show number of movies in each genre among the 250 top rated movies
         * rating
             * show average of movies in each genre among the 250 top rated movies
         * gross
             * show average gross in both USA and the world of movies in each genre among the 250 top rated movies
         * <'a genre name'>
             * available only if there is an active result set
             * valid input: a genre listed in a result set
         * <'a movie name'>
             * available after there is an active result set of <genre name> command
             * valid input: a number listed in a result set of <genre name> command
         * exit
             * exits the program
         * help
             * lists available commands (these instructions)
