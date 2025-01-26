from utils import create_database_connection


# Query 1: Find the top 5 movies mentioning 'gangster' in their overview with the highest average rating, including genres
def query_1():
    connection = create_database_connection()
    cursor = connection.cursor()
    cursor.execute("""
    SELECT m.title, m.overview, m.release_date, m.vote_average, GROUP_CONCAT(DISTINCT g.name) AS genres
    FROM movies m
    LEFT JOIN movie_genres mg ON m.movie_id = mg.movie_id
    LEFT JOIN genres g ON mg.genre_id = g.genre_id
    WHERE MATCH(m.overview) AGAINST('gangster' IN NATURAL LANGUAGE MODE)
    GROUP BY m.movie_id
    ORDER BY m.vote_average DESC
    LIMIT 5
    """)
    result = cursor.fetchall()
    for row in result:
        print(row)
    cursor.close()
    connection.close()


# Query 2: Find the top 5 most popular movies mentioning 'Action' in their overview, along with their genres and the number of actors in each movie
def query_2():
    connection = create_database_connection()
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


# Query 3: Find movies with the most diverse cast (actors from different genres)
def query_3():
    connection = create_database_connection()
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


# Query 4: Find the highest-rated movie in each genre, along with its rating, genre name, and popularity.
def query_4():
    connection = create_database_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT 
            g.name AS genre_name,
            m.title AS top_movie,
            m.vote_average AS rating,
            m.popularity
        FROM genres g
        JOIN movie_genres mg ON g.genre_id = mg.genre_id
        JOIN movies m ON mg.movie_id = m.movie_id
        WHERE m.vote_average = (
                SELECT MAX(m2.vote_average)
                FROM movie_genres mg2
                JOIN movies m2 ON mg2.movie_id = m2.movie_id
                WHERE mg2.genre_id = g.genre_id
            )
        ORDER BY g.name
    """)
    result = cursor.fetchall()
    for row in result:
        print(row)
    cursor.close()
    connection.close()


# Query 5: Find top 5 directors by average vote_average of the movies they directed.
def query_5():
    connection = create_database_connection()
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
