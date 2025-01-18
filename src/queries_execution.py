from queries_db_script import query_1, query_2, query_3, query_4, query_5

def main():
    print("Executing Complex Query 1: Find the Top 5 Actors with the Highest Average Movie Rating")
    query_1()
    print("\n")

    print("Executing Complex Query 2: Find the Top 5 Genres with the Highest Average Movie Rating")
    query_2()
    print("\n")

    print("Executing Complex Query 3: Find Movies with the Most Diverse Cast (Actors from Different Genres)")
    query_3()
    print("\n")

    print("Executing Query 4: Count the Number of Movies per Genre")
    query_4()
    print("\n")

    print("Executing Query 5: Find 10 Actors Who Have Acted in More Than One Movie")
    query_5()
    print("\n")

if __name__ == "__main__":
    main()