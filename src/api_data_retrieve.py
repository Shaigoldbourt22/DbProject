import requests
import mysql.connector
import time

API_KEY = '733e89cf8650182d336cd0a0d5ad71d0'
BASE_URL = "https://api.themoviedb.org/3"

def fetch_movies(page):
    url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&page={page}"
    response = requests.get(url)
    return response.json()

def fetch_genres():
    url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}"
    response = requests.get(url)
    return response.json()

def fetch_actors(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}"
    response = requests.get(url)
    return response.json()

def clean_database():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nrerc247!",
        database="MovieDB"
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
        host="localhost",
        user="root",
        password="Nrerc247!",
        database="MovieDB"
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
            
            cursor.execute("""
            INSERT INTO movies (movie_id, title, release_date, vote_average, overview, popularity)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (movie_id, title, release_date, vote_average, overview, popularity))
            
            for genre_id in movie['genre_ids']:
                genre_name = genre_dict[genre_id]
                cursor.execute("INSERT INTO genres (genre_id, name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE name=name", (genre_id, genre_name))
                cursor.execute("INSERT INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)", (movie_id, genre_id))
            
            actor_data = fetch_actors(movie_id)
            for actor in actor_data['cast']:
                person_id = actor['id']
                name = actor['name']
                character_name = actor.get('character', '')
                cursor.execute("INSERT INTO persons (person_id, name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE name=name", (person_id, name))
                cursor.execute("INSERT IGNORE INTO movie_cast (movie_id, person_id, role, character_name) VALUES (%s, %s, %s, %s)", (movie_id, person_id, 'Actor', character_name))
            
        # Sleep to avoid hitting the rate limit
        time.sleep(1)
        print(f"Inserted movies from page {page}")
    
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    clean_database()
    insert_data()