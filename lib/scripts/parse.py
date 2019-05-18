import  urllib3.exceptions
import sys, traceback
import config
import tmdbsimple as tmdb
import psycopg2
import datetime
import argparse
import urllib3.request
import socket


def database():
    """ connect to the database """
    # Define our connection string
    conn_string = "host='localhost' dbname='{}' user='{}' password = '{}'".format(config.DB_NAME, config.USER, config.PASSWORD)
    # print the connection string we will use to connect
    print("Connecting to database\n ->%s" % (conn_string))

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    # cursor = conn.cursor()
    print("Connected!\n")
    return conn


def insert_movie(conn, cur, movie, dt):
    """ Insert new movie into database """
    # dt = datetime.now()
    cur.execute("INSERT INTO movies(id, title, poster_path, release_date, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING", (movie['id'], movie['title'],  movie['poster_path'], movie['release_date'], dt, dt))
    print("Inserted: " + movie['title'])
    conn.commit()
    return True

def get_movies_now_playing(conn, cursor):
    counter = 0
    now = datetime.datetime.now()
    # datetime = time.strftime('%Y-%m-%d %H:%M:%S')
    movies = tmdb.Movies()
    for page_number in range(1, 10):
        tmdb.API_KEY = config.API_KEY
        dict_of_movies = movies.now_playing(**{'page':  page_number})
        for movie in dict_of_movies['results']:
            if(insert_movie(conn, cursor, movie, now)):
                counter+=1
    print('Inserted: ' + str(counter))

def main():
    try:
        # Open a connection to the database
        conn = database()
        # Open a cursor to perform database operations
        cursor = conn.cursor()
        get_movies_now_playing(conn, cursor)

    finally:
        print('Closing connection to database')
        # Close communication with the database
        cursor.close()
        conn.close()

if __name__ == '__main__':
    main()
