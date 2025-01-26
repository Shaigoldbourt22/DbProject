from dotenv import load_dotenv
from utils import create_database_connection
import os
import requests
import time

load_dotenv()

TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = os.getenv('TMDB_BASE_URL')


insert_movie = """INSERT INTO movies (movie_id, title, release_date, vote_average, overview, popularity)
            VALUES (%s, %s, %s, %s, %s, %s)"""
insert_genre = """INSERT INTO genres (genre_id, name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE name=name"""
insert_person = """INSERT INTO persons (person_id, name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE name=name"""
link_movie_genre = """INSERT INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)"""
link_movie_cast = """INSERT IGNORE INTO movie_cast (movie_id, person_id, role, character_name) VALUES (%s, %s, %s, %s)"""


def fetch_movies(page):
    url = f"{TMDB_BASE_URL}/movie/popular?api_key={TMDB_API_KEY}&page={page}"
    response = requests.get(url)
    return response.json()


def fetch_genres():
    url = f"{TMDB_BASE_URL}/genre/movie/list?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    return response.json()


def fetch_credits(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    return response.json()


def clean_database():
    connection = create_database_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM movie_cast")
    cursor.execute("DELETE FROM movie_genres")
    cursor.execute("DELETE FROM genres")
    cursor.execute("DELETE FROM persons")
    cursor.execute("DELETE FROM movies")
    connection.commit()
    cursor.close()
    connection.close()


def insert_data():
    connection = create_database_connection()
    cursor = connection.cursor()

    genres = fetch_genres()
    genre_dict = {genre['id']: genre['name'] for genre in genres['genres']}
    movie_ids_visited = set()

    # Batches for bulk inserts
    movies_batch = []
    genres_batch = []
    movie_genres_batch = []
    persons_batch = []
    movie_cast_batch = []

    for page in range(1, 250):  # Fetching 5000 movies (20 movies per page)
        movie_data = fetch_movies(page)
        for movie in movie_data['results']:
            movie_id = movie['id']
            title = movie['title']
            release_date = movie['release_date']
            vote_average = movie['vote_average']
            overview = movie['overview']
            popularity = movie['popularity']

            if movie_id in movie_ids_visited or not release_date:
                continue

            # Add movie to the batch
            movies_batch.append((movie_id, title, release_date, vote_average, overview, popularity))

            # Add genres to the batch
            for genre_id in movie['genre_ids']:
                genres_batch.append((genre_id, genre_dict[genre_id]))
                movie_genres_batch.append((movie_id, genre_id))

            # Fetch credits
            movie_credits = fetch_credits(movie_id)
            cast_list = movie_credits.get("cast", [])
            crew_list = movie_credits.get("crew", [])

            # Add cast (actors) to the batch
            for c in cast_list:
                person_id = c["id"]
                name = c["name"]
                character_name = c.get("character", "")
                persons_batch.append((person_id, name))
                movie_cast_batch.append((movie_id, person_id, "Actor", character_name))

            # Add crew to the batch
            for crew_member in crew_list:
                if (crew_member.get("job") == "Director"):
                    person_id = crew_member["id"]
                    name = crew_member["name"]
                    role = crew_member.get("job", "")
                    persons_batch.append((person_id, name))
                    movie_cast_batch.append((movie_id, person_id, role, ""))

            movie_ids_visited.add(movie_id)

        # Insert batches into the database
        if movies_batch:
            cursor.executemany(insert_movie, movies_batch)
            movies_batch = []

        if genres_batch:
            cursor.executemany(insert_genre, genres_batch)
            genres_batch = []

        if movie_genres_batch:
            cursor.executemany(link_movie_genre, movie_genres_batch)
            movie_genres_batch = []

        if persons_batch:
            cursor.executemany(insert_person, persons_batch)
            persons_batch = []

        if movie_cast_batch:
            cursor.executemany(link_movie_cast, movie_cast_batch)
            movie_cast_batch = []

        connection.commit()
        print(f"Inserted movies from page {page}")

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    clean_database()
    insert_data()
