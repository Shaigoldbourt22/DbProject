from queries_db_script import query_1, query_2, query_3, query_4, query_5


def main():
    print("Executing Query 1: Search for Movies by Title")
    query_1()
    print("\n")

    print("Executing Query 2: Search for Actors by Name")
    query_2()
    print("\n")

    print("Executing Query 3: Find Movies Released After a Certain Year with a Specific Genre")
    query_3()
    print("\n")

    print("Executing Query 4: Count the Number of Movies per Genre")
    query_4()
    print("\n")

    print("Executing Query 5: Find top 5 directors by average vote_average of the movies they directed")
    query_5()
    print("\n")


if __name__ == "__main__":
    main()
