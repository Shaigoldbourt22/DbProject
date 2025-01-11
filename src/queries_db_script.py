from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")


def query_1():
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = connection.cursor()
    title = input("Enter movie title to search: ")
    cursor.execute("SELECT * FROM movies WHERE title = %s", (title,))
    result = cursor.fetchall()
    for row in result:
        print(row)
    cursor.close()
    connection.close()


def query_2():
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = connection.cursor()
    name = input("Enter actor name to search: ")
    cursor.execute("SELECT * FROM persons WHERE name = %s", (name,))
    result = cursor.fetchall()
    for row in result:
        print(row)
    cursor.close()
    connection.close()


def query_3():
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = connection.cursor()
    year = input("Enter release year: ")
    genre = input("Enter genre: ")
    cursor.execute("""
    SELECT m.*
    FROM movies m
    JOIN movie_genres mg ON m.movie_id = mg.movie_id
    JOIN genres g ON mg.genre_id = g.genre_id
    WHERE YEAR(m.release_date) > %s AND g.name = %s
    """, (year, genre))
    result = cursor.fetchall()
    for row in result:
        print(row)
    cursor.close()
    connection.close()


def query_4():
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = connection.cursor()
    cursor.execute("""
    SELECT g.name, COUNT(mg.movie_id) as movie_count
    FROM genres g
    JOIN movie_genres mg ON g.genre_id = mg.genre_id
    GROUP BY g.name
    """)
    result = cursor.fetchall()
    for row in result:
        print(row)
    cursor.close()
    connection.close()


def query_5():
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = connection.cursor()
    cursor.execute("""
        SELECT 
            m.title,
            p.name
        FROM movies m
        JOIN movie_cast mc_actor ON (m.movie_id = mc_actor.movie_id)
        JOIN persons p ON mc_actor.person_id = p.person_id
        WHERE mc_actor.role = 'Actor'
          AND EXISTS (
              SELECT 1
              FROM movie_cast mc_director
              WHERE mc_director.movie_id = m.movie_id
                AND mc_director.person_id = p.person_id
                AND mc_director.role = 'Director'
          );
      """)
    result = cursor.fetchall()
    for row in result:
        print(row)
    cursor.close()
    connection.close()
