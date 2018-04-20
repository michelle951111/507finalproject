import requests
import json
from bs4 import BeautifulSoup
import plotly.plotly as py
import sqlite3


# on startup, try to load the cache from file
CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

header = {'User-Agent': 'SI_CLASS'}
def make_request_using_cache(url):
    global header
    unique_ident = url

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url,headers=header)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

top250=[]

def get_top_250():
    global header
    baseurl = 'https://www.imdb.com'
    top_url = baseurl + "/chart/top?ref_=nv_mv_250_6"
    top_text = make_request_using_cache(top_url)
    top_page_soup = BeautifulSoup(top_text, 'html.parser')
    top_movie_list = top_page_soup.find(class_= 'lister-list')
    top_movies = top_movie_list.find_all('tr')
    for each_movie in top_movies:
        movie_title = each_movie.find(class_='titleColumn')
        movie_name = movie_title.find('a').string
        movie_year = movie_title.find('span').string
        movie_url = baseurl + movie_title.find('a')['href']
        movie_rating_data = each_movie.find(class_='ratingColumn imdbRating')
        movie_rating_raw = movie_rating_data.find('strong').string
        movie_rating = float(movie_rating_raw)
        movie_page_text = make_request_using_cache(movie_url)
        movie_page_soup = BeautifulSoup(movie_page_text, 'html.parser')
        movie_director_data = movie_page_soup.find(itemprop='director')
        movie_director = movie_director_data.find(itemprop='name').string
        movie_detail = movie_page_soup.select('.txt-block')
        # get gross
        for each in movie_detail:
            inline = each.select('.inline')
            if inline:
                if inline[0].get_text() == 'Gross USA:':
                    gross_usa = str(each.get_text())
                elif inline[0].get_text() == 'Cumulative Worldwide Gross:':
                    cumulative_worldwide_gross = str(each.get_text())
        #trans to int
        a = gross_usa.strip()
        b = a[a.index('$') + 1:].strip()
        movie_gross_usa = int(b.split(' ')[0].replace(',', ''))
        c = cumulative_worldwide_gross.strip()
        d = c[c.index('$') + 1:].strip()
        movie_gross_world = int(d.split(' ')[0].replace(',', ''))
        #get genre
        movie_genres=[]
        titleStoryLine = movie_page_soup.find(id='titleStoryLine')
        genres = titleStoryLine.find(itemprop='genre')
        genre_list = genres.find_all('a')
        for each in genre_list:
            movie_genres.append(each.string)
        top250.append({"title":movie_name,"rating":movie_rating,"year":movie_year,"director":movie_director,"us gross":movie_gross_usa,"global gross":movie_gross_world,"genres":movie_genres})
    return top250

if __name__=="__main__":
    get_top_250()

    directory_dict_cache = json.dumps(top250,indent=4)
    f = open("movies_dict.json","w")
    f.write(directory_dict_cache)
    f.close()
