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
    cursor.execute("""
    SELECT p.name AS actor, AVG(m.vote_average) AS avg_rating
    FROM persons p
    JOIN movie_cast mc ON p.person_id = mc.person_id
    JOIN movies m ON mc.movie_id = m.movie_id
    WHERE mc.role = 'Actor'
    GROUP BY p.name
    ORDER BY avg_rating DESC
    LIMIT 5
    """)
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
    cursor.execute("""
    SELECT g.name AS genre, AVG(m.vote_average) AS avg_rating
    FROM genres g
    JOIN movie_genres mg ON g.genre_id = mg.genre_id
    JOIN movies m ON mg.movie_id = m.movie_id
    GROUP BY g.name
    ORDER BY avg_rating DESC
    LIMIT 5
    """)
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
    cursor.execute("""
    SELECT m.title, COUNT(DISTINCT g.genre_id) AS genre_count
    FROM movies m
    JOIN movie_cast mc ON m.movie_id = mc.movie_id
    JOIN movie_genres mg ON m.movie_id = mg.movie_id
    JOIN genres g ON mg.genre_id = g.genre_id
    WHERE mc.role = 'Actor'
    GROUP BY m.title
    ORDER BY genre_count DESC
    LIMIT 5
    """)
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


# Query 5: Find top 5 directors by average vote_average of the movies they directed.
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
            p.name AS director_name,
            AVG(m.vote_average) AS avg_rating,
            COUNT(*) as num_movies
        FROM movie_cast mc
        JOIN persons p ON mc.person_id = p.person_id
        JOIN movies m ON mc.movie_id = m.movie_id
        WHERE mc.role = 'Director'
        GROUP BY p.person_id
        HAVING COUNT(*) >= 1
        ORDER BY avg_rating DESC
        LIMIT 5;
    """)
    result = cursor.fetchall()
    for row in result:
        print(row)
    cursor.close()
    connection.close()
