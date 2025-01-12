from dotenv import load_dotenv
import os
import requests
import mysql.connector
import time

load_dotenv()

TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = os.getenv('TMDB_BASE_URL')

db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")

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
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
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
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = connection.cursor()

    genres = fetch_genres()
    genre_dict = {genre['id']: genre['name'] for genre in genres['genres']}

    for page in range(1, 3):  # Fetching 5000 movies (20 movies per page)
        movie_data = fetch_movies(page)
        for movie in movie_data['results']:
            movie_id = movie['id']
            title = movie['title']
            release_date = movie['release_date']
            vote_average = movie['vote_average']
            overview = movie['overview']
            popularity = movie['popularity']

            cursor.execute(insert_movie, (movie_id, title, release_date, vote_average, overview, popularity))

            for genre_id in movie['genre_ids']:
                genre_name = genre_dict[genre_id]
                cursor.execute(insert_genre, (genre_id, genre_name))
                cursor.execute(link_movie_genre, (movie_id, genre_id))

            movie_credits = fetch_credits(movie_id)
            cast_list = movie_credits.get("cast", [])
            crew_list = movie_credits.get("crew", [])

            # Insert cast (actors)
            for c in cast_list:
                person_id = c["id"]
                name = c["name"]
                character_name = c.get("character", "")
                cursor.execute(insert_person, (person_id, name))
                cursor.execute(link_movie_cast, (movie_id, person_id, "Actor", character_name))

            # Insert crew
            for crew_member in crew_list:
                person_id = crew_member["id"]
                name = crew_member["name"]
                cursor.execute(insert_person, (person_id, name))
                cursor.execute(link_movie_cast, (movie_id, person_id, crew_member.get("job"), ""))

        # Sleep to avoid hitting the rate limit
        time.sleep(1)
        print(f"Inserted movies from page {page}")

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    clean_database()
    insert_data()
