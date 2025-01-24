from queries_db_script import query_1, query_2, query_3, query_4, query_5


def main():
    print("Executing Query 1: Find the Top 5 Movies Mentioning 'Leonardo DiCaprio' in Their Overview with the Highest Average Rating, Including Genres")    
    query_1()
    print("\n")

    print("Executing Query 2: Find the top 5 most popular movies mentioning 'Action' in their overview, along with their genres and the number of actors in each movie")
    query_2()
    print("\n")

    print("Executing Query 3: Find Movies with the Most Diverse Cast (Actors from Different Genres)")    
    query_3()
    print("\n")

    print("Executing Query 4: Find the highest-rated movie in each genre, along with its rating, genre name, and popularity.")
    query_4()
    print("\n")

    print("Executing Query 5: Find top 5 directors by average vote_average of the movies they directed")
    query_5()
    print("\n")


if __name__ == "__main__":
    main()
