import mysql.connector

def query_1():
    connection = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="MovieDB"
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
        host="localhost",
        user="your_username",
        password="your_password",
        database="MovieDB"
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
        host="localhost",
        user="your_username",
        password="your_password",
        database="MovieDB"
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
    """)
    result = cursor.fetchall()
    for row in result:
        print(row)
    cursor.close()
    connection.close()