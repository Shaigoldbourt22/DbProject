import mysql.connector

def query_1():
    connection = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="MovieDB"
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
        host="localhost",
        user="your_username",
        password="your_password",
        database="MovieDB"
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
        host="localhost",
        user="your_username",
        password="your_password",
        database="MovieDB"
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
        host="localhost",
        user="your_username",
        password="your_password",
        database="MovieDB"
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
        host="localhost",
        user="your_username",
        password="your_password",
        database="MovieDB"
    )
    cursor = connection.cursor()
    cursor.execute("""
    SELECT p.name, COUNT(mc.movie_id) as movie_count
    FROM persons p
    JOIN movie_cast mc ON p.person_id = mc.person_id
    GROUP BY p.name
    HAVING movie_count > 1
    ORDER BY movie_count DESC
    LIMIT 10
    """)
    result = cursor.fetchall()
    for row in result:
        print(row)
    cursor.close()
    connection.close()