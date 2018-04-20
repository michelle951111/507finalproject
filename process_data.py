import requests
import json
from bs4 import BeautifulSoup
import plotly.plotly as py
import plotly.graph_objs as go
import sqlite3

DBNAME = 'movie.db'

class Movie():
    def __init__(self, title):
        self.title = title

        try:
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()
        except Error as e:
            print(e)

        param=(title,)
        statement = '''
            SELECT *
            From Movies
            WHERE Movie =?;
        '''
        results = cur.execute(statement,param)
        result_list = results.fetchall()
        self.rating=result_list[0][2]
        self.year=result_list[0][3]
        self.director=result_list[0][4]
        self.usgross=result_list[0][5]
        self.globalgross=result_list[0][6]

    def __str__(self):
        intro = self.title + self.year + " directed by " + self.director + ' ('+str(self.rating)+')'
        return intro

def show_number():
    genre=[]
    number=[]
    result={}
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    statement = '''
        SELECT Genre,Count(*)
        From Movies_Genres
        JOIN Genres on Genres.Id = Movies_Genres.GenreId
        Group by Movies_Genres.GenreId;
    '''
    cur.execute(statement)

    print('Number of Movies in Each Genre:')
    for row in cur:
        genre.append(row[0])
        number.append(row[1])
        print('{:10}'.format(row[0]),end=" ")
        print('{:5}'.format(str(row[1])))
        #print(row[0],row[1])
        result[row[0]]=row[1]

    conn.commit()
    conn.close()

    trace0 = go.Bar(
    x=genre,
    y=number,
    marker=dict(
        color='rgb(26, 118, 255)',
        ),
        opacity=1
    )

    data = [trace0]
    layout = go.Layout(
        title='Number of Movies in Each Genre',
        xaxis=dict(
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
            )
        ),
        yaxis=dict(
            title='Number of Movies',
            titlefont=dict(
                size=16,
                color='rgb(107, 107, 107)'
            ),
            tickfont=dict(
                size=14,
                color='rgb(107, 107, 107)'
            )
        ),
        bargap=0.15,
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='number-genre')

    return result

def show_rating():
    genre=[]
    rating=[]
    result={}
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    statement = '''
        SELECT Genre,AVG(Rating)
        From Movies_Genres
        JOIN Genres on Genres.Id = Movies_Genres.GenreId
        JOIN Movies on Movies.Id = Movies_Genres.MovieId
        Group by Movies_Genres.GenreId;
    '''
    cur.execute(statement)

    print('Average Rating of Movies in Each Genre:')
    for row in cur:
        genre.append(row[0])
        rating.append(format(row[1]-8,'.2f'))
        print('{:10}'.format(row[0]),end=" ")
        print('{:5}'.format(str(format(row[1],'.2f'))))
        #print(row[0],format(row[1],'.2f'))
        result[row[0]]=format(row[1],'.2f')

    conn.commit()
    conn.close()

    trace0 = go.Bar(
    x=genre,
    y=rating,
    base = 8,
    marker=dict(
        color='#FFAC00',
        ),
        opacity=1
    )

    data = [trace0]
    layout = go.Layout(
        title='Average Ratings of Movies in Each Genre',
        xaxis=dict(
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
            )
        ),

        yaxis=dict(
            range=[8, 8.4],
            title='Average Rating',
            titlefont=dict(
                size=16,
                color='rgb(107, 107, 107)'
            ),
            tickfont=dict(
                size=14,
                color='rgb(107, 107, 107)'
            )
        ),
        bargap=0.15,
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='rating-genre')

    return result

def show_gross():
    genre=[]
    us_gross=[]
    global_gross=[]
    result={}
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    statement = '''
        SELECT Genre,AVG(UsGross),AVG(GlobalGross)
        From Movies_Genres
        JOIN Genres on Genres.Id = Movies_Genres.GenreId
        JOIN Movies on Movies.Id = Movies_Genres.MovieId
        Group by Movies_Genres.GenreId;
    '''
    cur.execute(statement)

    print('Average Gross of Movies in Each Genre:')
    for row in cur:
        genre.append(row[0])
        us_gross.append(format(row[1]/1000000,'.2f'))
        global_gross.append(format(row[2]/1000000,'.2f'))
        #print(row[0],str(format(row[1],'.2f'))+'(USA)',str(format(row[2],'.2f'))+'(Global)')
        print('{:10}'.format(row[0]),end=" ")
        print('{:18}'.format(str(format(row[1],'.2f'))+'(USA)'),end=" ")
        print('{:18}'.format(str(format(row[2],'.2f'))+'(Gloabl)'))
        result[row[0]]={'US Gross':(format(row[1],'.2f')),'Global Gross':(format(row[2],'.2f'))}

    conn.commit()
    conn.close()

    trace1 = go.Bar(
    x=genre,
    y=us_gross,
    name='Gross in USA',
    marker=dict(
        color='#F05656'
        )
    )
    trace2 = go.Bar(
        x=genre,
        y=global_gross,
        name='Global Gross',
        marker=dict(
            color='rgb(26, 118, 255)'
        )
    )
    data = [trace1, trace2]
    layout = go.Layout(
        title='Average Gross of Movies in Each Genre',
        xaxis=dict(
            tickfont=dict(
                size=14,
                color='rgb(107, 107, 107)'
            )
        ),
        yaxis=dict(
            title='USD (millions)',
            titlefont=dict(
                size=16,
                color='rgb(107, 107, 107)'
            ),
            tickfont=dict(
                size=14,
                color='rgb(107, 107, 107)'
            )
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='gross-genre')
    return result

def gross_rating(genre):
    movie=[]
    rating=[]
    global_gross=[]
    result={}
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)
    param=(genre,)
    statement = '''
        SELECT Movie,Rating,GlobalGross
        From Movies
        JOIN Movies_Genres on Movies.Id = Movies_Genres.MovieId
            JOIN Genres on Genres.Id = Movies_Genres.GenreId
        WHERE Genre =?
        Group By Movie
        Order BY Rating desc
        LIMIT 50;
    '''
    cur.execute(statement,param)

    print('GlobalGross and Ratings of '+genre+' Movies:')

    i=1
    for row in cur:
        global_gross.append(format(row[2]/1000000,'.2f'))
        movie.append(row[0])
        rating.append(row[1])
        #print(str(i),row[0],str(row[2])+'(Gross)',str(row[1])+'(Rating)')
        print('{:3}'.format(str(i)),end=" ")
        if len(row[0])>20:
            output = row[0][0:19]+"..."
        else:
            output = row[0]
        print('{:25}'.format(output),end=" ")
        print('{:20}'.format(str(row[2])+'(Gross)'),end=" ")
        print('{:10}'.format(str(row[1])+'(Rating)'))
        result[i]={'Movie':row[0],'Gross':row[2],'Rating':row[1]}
        i=i+1

    conn.commit()
    conn.close()

    trace = go.Scatter(
        x = global_gross,
        y = rating,
        mode = 'markers',
        marker= dict(size= 14,
                    color= 'FFAC00',
                    opacity= 1
                   ),
        text = movie
        )

    data = [trace]
    layout = go.Layout(
        title='GlobalGross and Rating of '+ genre +' Movies',
        xaxis=dict(
            title='Global Gross (USD Millions)',
            titlefont=dict(
                size=16,
                color='rgb(107, 107, 107)'
            ),
            tickfont=dict(
                size=14,
                color='rgb(107, 107, 107)'
                )
        ),

        yaxis=dict(
            title='Rating',
            titlefont=dict(
                size=16,
                color='rgb(107, 107, 107)'
            ),
            tickfont=dict(
                size=14,
                color='rgb(107, 107, 107)'
            )
        ),

    )
    fig= go.Figure(data=data, layout=layout)
    py.plot(fig,filename='gross-rating')
    return result

def gross_share(movie):
    obj = Movie(title=movie)
    us_gross = obj.usgross
    global_gross = obj.globalgross
    other_gross = global_gross-us_gross
    result=(us_gross, global_gross)
    print('movie info:')
    print(obj)

    labels = ['Gross in USA','Gross in Other Regions']
    values = [us_gross,other_gross]
    colors = ['#F05656', 'rgb(26, 118, 255)']

    trace = go.Pie(labels=labels, values=values,
                   hoverinfo='label+percent+value', textinfo='percent',
                   textfont=dict(size=20),
                   marker=dict(colors=colors,
                               ))
    layout = go.Layout(
            title='Gross Share of '+ movie
            )

    fig= go.Figure(data=[trace], layout=layout)
    py.plot(fig,filename='gross_share')
    return result

def help_command():
        print("""
       valid command:

       number
           show number of movies in each genre among the 250 top rated movies
       rating
           show average of movies in each genre among the 250 top rated movies
       gross
           show average gross in both USA and the world of movies in each genre among the 250 top rated movies
       <genre name>
           available only if there is an active result set
           valid input: a genre listed in a result set
       <movie name>
           available after there is an active result set of <genre name> command
           valid input: a number listed in a result set of <genre name> command
       exit
           exits the program
       help
           lists available commands (these instructions)

        """)

def interactive_prompt():
    term=input('Enter number/rating/gross or help: ')
    while term != 'exit':
        if (term=='number')or(term=='rating')or(term=='gross'):
            term=main_command(term)
        elif term=="help":
            term=help_command()
        else:
            print('Invalid Command, Please input help to see instruction')

        if term!='exit':
            term=input('Enter number/rating/gross or help: ')
    return term

def main_command(term):
    result={}
    if term=='number':
        result=show_number()
    elif term=='rating':
        result=show_rating()
    elif term=='gross':
        result=show_gross()
    elif term=='exit':
        pass
    second_term=input('Enter number/rating/gross or a genre or help: ')

    if (second_term=='number')or(second_term=='rating')or(second_term=='gross'):
        second_term=main_command(second_term)
    elif second_term=='exit':
        pass
    else:
        second_term=genre_command(second_term,result)
    return second_term

def genre_command(term,last_result):
    movie_dict={}
    if term in last_result.keys():
        movie_dict=gross_rating(term)
    elif term=="help":
        help_command()
    elif term=='exit':
        pass
    else:
        print('Invalid Command, Please input help to see instruction')
    second_term=input('Enter a number in the movie list, or try another genre or help: ')

    if (second_term.isdigit()) and (int(second_term) <= len(movie_dict)) :
        second_term=movie_command(second_term,last_result,movie_dict)
    elif second_term=='exit':
        pass
    else:
        second_term=genre_command(second_term,last_result)
    return second_term

def movie_command(term,last_result,movie_dict):
    movie=movie_dict[int(term)]['Movie']
    gross_share(movie)
    second_term=input('Enter a number in the movie list, or try another genre or help: ')

    if (second_term.isdigit()) and (int(second_term) <= len(movie_dict)) :
        second_term=movie_command(second_term,last_result,movie_dict)
    elif second_term=='exit':
        pass
    else:
        second_term=genre_command(second_term,last_result)
    return second_term




if __name__=="__main__":
    print('Welcome to IMDB top 250 movies!')
    term=interactive_prompt()
    print("bye")
    #print(gross_rating('Crime'))
