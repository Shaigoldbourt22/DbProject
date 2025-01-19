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

    # Create index on the popularity column
    create_index_if_not_exists("idx_popularity", "movies", "CREATE INDEX idx_popularity ON movies(popularity)")

    # Movies table indexes
    create_index_if_not_exists("idx_movie_vote", "movies", "CREATE INDEX idx_movie_vote ON movies(movie_id, vote_average)")
    create_index_if_not_exists("idx_movie_popularity", "movies", "CREATE INDEX idx_movie_popularity ON movies(movie_id, popularity)")

    # Movie genres table indexes
    create_index_if_not_exists("idx_movie_vote", "movies", "CREATE INDEX idx_movie_vote ON movies(movie_id, vote_average)")
    create_index_if_not_exists("idx_movie_popularity", "movies", "CREATE INDEX idx_movie_popularity ON movies(movie_id, popularity)")

    # Movie cast table indexes
    create_index_if_not_exists("idx_cast_movie", "movie_cast", "CREATE INDEX idx_cast_movie ON movie_cast(movie_id, person_id)")
    create_index_if_not_exists("idx_cast_role", "movie_cast", "CREATE INDEX idx_cast_role ON movie_cast(person_id, role)")
    create_index_if_not_exists("idx_role", "movie_cast", "CREATE INDEX idx_role ON movie_cast(role)")

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
