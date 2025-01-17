from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_port = os.getenv("DB_PORT")


def create_database():
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        port=db_port,
        database=db_name
    )
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS MovieDB")
    cursor.close()
    connection.close()


def create_tables():
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        movie_id INT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        release_date DATE NOT NULL,
        vote_average FLOAT,
        overview TEXT,
        popularity FLOAT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS persons (
        person_id INT PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS genres (
        genre_id INT PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movie_genres (
        movie_id INT,
        genre_id INT,
        PRIMARY KEY (movie_id, genre_id),
        FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
        FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movie_cast (
        movie_id INT,
        person_id INT,
        role VARCHAR(255),
        character_name VARCHAR(255),
        PRIMARY KEY (movie_id, person_id),
        FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
        FOREIGN KEY (person_id) REFERENCES persons(person_id)
    )
    """)

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    create_database()
    create_tables()
