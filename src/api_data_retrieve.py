import requests
import mysql.connector
import time

API_KEY = '733e89cf8650182d336cd0a0d5ad71d0'

def fetch_movies(page):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&page={page}"
    response = requests.get(url)
    return response.json()

def fetch_genres():
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}"
    response = requests.get(url)
    return response.json()

def insert_data():
    connection = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="MovieDB"
    )
    cursor = connection.cursor()
    
    genres = fetch_genres()
    genre_dict = {genre['id']: genre['name'] for genre in genres['genres']}
    
    for page in range(1, 251):  # Fetching 5000 movies (20 movies per page)
        movie_data = fetch_movies(page)
        for movie in movie_data['results']:
            genre_names = ', '.join([genre_dict[genre_id] for genre_id in movie['genre_ids']])
            cursor.execute("""
            INSERT INTO Movies (title, release_year, genre)
            VALUES (%s, %s, %s)
            """, (movie['title'], movie['release_date'][:4], genre_names))
            
            # Assuming you have a way to fetch actor data and insert into Actors and MovieActors tables
            
        # Sleep to avoid hitting the rate limit
        time.sleep(1)
        print(f"Inserted movies from page {page}")
    
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    insert_data()