import requests
import mysql.connector
import time

API_KEY = 'your_tmdb_api_key'

def fetch_movies(page):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&page={page}"
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
    
    for page in range(1, 251):  # Fetching 5000 movies (20 movies per page)
        movie_data = fetch_movies(page)
        for movie in movie_data['results']:
            cursor.execute("""
            INSERT INTO Movies (title, release_year, genre)
            VALUES (%s, %s, %s)
            """, (movie['title'], movie['release_date'][:4], ', '.join([genre['name'] for genre in movie['genre_ids']])))
            
            # Assuming you have a way to fetch actor data and insert into Actors and MovieActors tables
            
        # Sleep to avoid hitting the rate limit
        time.sleep(1)
    
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    insert_data()