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
    cursor.execute("SELECT * FROM Movies WHERE title = %s", (title,))
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
    cursor.execute("SELECT * FROM Actors WHERE name = %s", (name,))
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
    cursor.execute("SELECT * FROM Movies WHERE release_year > %s AND genre = %s", (year, genre))
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
    cursor.execute("SELECT genre, COUNT(*) FROM Movies GROUP BY genre")
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
    SELECT a.name, COUNT(ma.movie_id) as movie_count
    FROM Actors a
    JOIN MovieActors ma ON a.actor_id = ma.actor_id
    GROUP BY a.name
    HAVING movie_count > 1
    """)
    result = cursor.fetchall()
    for row in result:
        print(row)
    cursor.close()
    connection.close()
