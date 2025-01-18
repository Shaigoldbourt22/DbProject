import mysql.connector

def query_1():
    # Find the top 5 movies mentioning 'Leonardo DiCaprio' in their overview with the highest average rating, including genres
    connection = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="MovieDB"
    )
    cursor = connection.cursor()
    cursor.execute("""
    SELECT m.title, m.overview, m.release_date, m.vote_average, GROUP_CONCAT(DISTINCT g.name) AS genres
    FROM movies m
    LEFT JOIN movie_genres mg ON m.movie_id = mg.movie_id
    LEFT JOIN genres g ON mg.genre_id = g.genre_id
    WHERE MATCH(m.overview) AGAINST('Leonardo DiCaprio' IN NATURAL LANGUAGE MODE)
    GROUP BY m.movie_id
    ORDER BY m.vote_average DESC
    LIMIT 5
    """)
    result = cursor.fetchall()
    for row in result:
        print(row)
    cursor.close()
    connection.close()

def query_2():
    # Find the top 5 most popular movies mentioning 'Action' in their overview, along with their genres and the number of actors in each movie
    connection = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="MovieDB"
    )
    cursor = connection.cursor()
    cursor.execute("""
    SELECT m.title, m.overview, m.release_date, m.popularity, GROUP_CONCAT(DISTINCT g.name) AS genres, COUNT(DISTINCT mc.person_id) AS actor_count
    FROM movies m
    JOIN movie_genres mg ON m.movie_id = mg.movie_id
    JOIN genres g ON mg.genre_id = g.genre_id
    JOIN movie_cast mc ON m.movie_id = mc.movie_id
    WHERE MATCH(m.overview) AGAINST('Action' IN NATURAL LANGUAGE MODE) AND mc.role = 'Actor'
    GROUP BY m.movie_id
    ORDER BY m.popularity DESC
    LIMIT 5
    """)
    result = cursor.fetchall()
    for row in result:
        print(row)
    cursor.close()
    connection.close()

def query_3():
    # Find movies with the most diverse cast (actors from different genres)
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