from utils import create_database_connection

from dotenv import load_dotenv
import os

load_dotenv()

db_name=os.getenv('DB_NAME')


def create_database():
    connection = create_database_connection()
    cursor = connection.cursor()
    cursor.execute(f"""CREATE DATABASE IF NOT EXISTS {db_name}""")
    cursor.close()
    connection.close()


def create_tables():
    connection = create_database_connection()
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

    # Check if indexes already exist before creating them
    def create_index_if_not_exists(index_name, table_name, index_sql):
        cursor.execute(f"""
        SELECT COUNT(*)
        FROM information_schema.statistics
        WHERE table_schema = '{db_name}' AND table_name = '{table_name}' AND index_name = '{index_name}'
        """)
        if cursor.fetchone()[0] == 0:
            cursor.execute(index_sql)

    # Create full-text index on the overview column
    create_index_if_not_exists("idx_overview", "movies", "CREATE FULLTEXT INDEX idx_overview ON movies(overview)")

    # Indexes for Query Optimization
    create_index_if_not_exists("idx_popularity", "movies", "CREATE INDEX idx_popularity ON movies(popularity)")
    create_index_if_not_exists("idx_vote_average", "movies", "CREATE INDEX idx_vote_average ON movies(vote_average)")

    # Composite index for Query 4 (movie_genres with genre_id and movie_id)
    create_index_if_not_exists("idx_movie_genres_genre_movie", "movie_genres", "CREATE INDEX idx_movie_genres_genre_movie ON movie_genres(genre_id, movie_id)")

    # Composite index for Query 4 (movies with vote_average and movie_id)
    create_index_if_not_exists("idx_movies_vote_movie", "movies", "CREATE INDEX idx_movies_vote_movie ON movies(vote_average, movie_id)")

    # Movie cast table indexes
    create_index_if_not_exists("idx_cast_movie", "movie_cast", "CREATE INDEX idx_cast_movie ON movie_cast(movie_id, person_id)")
    create_index_if_not_exists("idx_cast_role", "movie_cast", "CREATE INDEX idx_cast_role ON movie_cast(person_id, role)")

    # Genres table index
    create_index_if_not_exists("idx_genre_id", "genres", "CREATE INDEX idx_genre_id ON genres(genre_id)")

    # Persons table index
    create_index_if_not_exists("idx_person_id", "persons", "CREATE INDEX idx_person_id ON persons(person_id)")

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    create_database()
    create_tables()
