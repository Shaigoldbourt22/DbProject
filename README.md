# Movie Database Management System

<p align="center">
    <img alt="Issues" src="https://img.shields.io/github/issues-raw/Shaigoldbourt22/DbProject"/>
    <img alt="pull request" src="https://img.shields.io/github/issues-pr-closed/Shaigoldbourt22/DbProject"/>
    <img alt="stars" src="https://img.shields.io/github/stars/Shaigoldbourt22/DbProject?style=social">
    <img alt="updated" src="https://img.shields.io/github/last-commit/Shaigoldbourt22/DbProject">
    <img alt="size" src="https://img.shields.io/github/repo-size/Shaigoldbourt22/DbProject" >
</p>

## Overview

This project involves the creation of a movie-centered database management system (DBMS) using MySQL and Python. The system fetches data from The Movie Database (TMDB) API and stores it in a well-structured MySQL database. Additionally, the project includes five distinct database queries to analyze the stored data, focusing on specific aspects of the movie industry.

## Features

1. **Database Schema**: The database includes five tables: `movies`, `genres`, `persons`, `movie_genres`, and `movie_cast`. These tables store detailed information about movies, their genres, and cast/crew members.

2. **Data Population**:

   - The system uses the TMDB API to retrieve movie data, genres, and credits.
   - Over 5,000 records are populated across the tables.

3. **Queries**:

   - Two full-text search queries.
   - Three complex queries involving nested subqueries, aggregations, and the `EXISTS` clause.

4. **Database Optimizations**:
   - Proper indexing and foreign key constraints for efficient query execution.

## Prerequisites

- Python 3.11.4
- MySQL server (hosted on `mysqlsrv1.cs.tau.ac.il`)
- Required Python libraries (see `requirements.txt`)

## File Structure

```
project-root/
│
├── src/
│   ├── create_db_script.py       # Script to create the database schema
│   ├── api_data_retrieve.py      # Script to fetch and insert data from TMDB API
│   ├── queries_db_script.py      # Contains the SQL query functions
│   └── queries_execution.py      # Query executions
│
├── documentation/
│   ├── user_manual.pdf           # Application functionality and design
│   ├── system_docs.pdf           # Database schema and design 
│   └── mysql_and_user_password.txt # MySQL credentials
│
├── requirements.txt              # Required Python packages
└── name_and_id.txt               # Team member names and IDs
```

## Database Design

The database consists of the following tables:

1. **movies**:

   - Stores basic movie details.
   - Indexed by `movie_id` for fast lookups.

2. **genres**:

   - Stores genre information.
   - Linked to movies via the `movie_genres` table.

3. **persons**:

   - Stores details of cast and crew members.

4. **movie_genres**:

   - Links movies to their respective genres.

5. **movie_cast**:
   - Links movies to cast and crew, specifying roles and character names.

## Queries Implemented

1. **Query 1**: Find the top 5 movies mentioning 'gangster' in their overview with the highest average rating, including genres
2. **Query 2**: Find the top 5 most popular movies mentioning 'Action' in their overview, along with their genres and the number of actors in each movie
3. **Query 3**: Find movies with the most diverse cast (actors from different genres)
4. **Query 4**: Find the highest-rated movie in each genre, along with its rating, genre name, and popularity.
5. **Query 5**: Find top 5 directors by average vote_average of the movies they directed

# Index Strategy

This project uses a set of carefully selected indexes to optimize query performance. Below is a summary of the indexes added to each table, their purpose, and justification:

| Table              | Index Name                        | Columns                    | Purpose                                                                                              | Justification                                                                                       |
| ------------------ | --------------------------------- | -------------------------- | ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| **`movies`**       | `idx_overview`                   | `overview`                 | Full-text search for queries like `MATCH ... AGAINST` on movie descriptions.                         | Improves performance for text searches involving keywords (e.g., "gangster").                       |
|                    | `idx_popularity`                 | `popularity`               | Filtering and sorting movies by popularity.                                                          | Optimizes queries that rank movies by popularity, often used in user-facing applications.           |
|                    | `idx_vote_average`               | `vote_average`             | Filtering and sorting movies by average vote.                                                        | Improves performance for queries ranking movies by ratings.                                         |
|                    | `idx_movies_vote_movie`          | `vote_average`, `movie_id` | Efficient sorting and grouping for queries involving ratings and movie ID.                           | Supports queries like finding the top-rated movies or aggregating results by movie ID.              |
| **`movie_genres`** | `idx_movie_genres_genre_movie`   | `genre_id`, `movie_id`     | Efficient joins between movies and genres.                                                           | Essential for queries combining movie and genre information (e.g., highest-rated movies per genre). |
| **`movie_cast`**   | `idx_cast_movie`                 | `movie_id`, `person_id`    | Optimizes joins with `persons` and grouping for queries about actors and directors.                  | Critical for queries fetching details about cast members or filtering by cast roles.                |
|                    | `idx_cast_role`                  | `person_id`, `role`        | Efficient filtering for queries involving roles (e.g., actors or directors).                         | Improves performance of role-specific queries like finding directors or actors for a movie.         |
| **`genres`**       | `idx_genre_id`                   | `genre_id`                 | Efficient joins with `movie_genres` for genre-specific queries.                                      | Ensures fast joins between genres and movie genres for filtering or aggregating by genre.           |
| **`persons`**      | `idx_person_id`                  | `person_id`                | Optimizes joins with `movie_cast` for queries involving directors and cast members.                  | Supports fast lookups of directors or actors and their associated movies.                           |

### Key Points

- **Read Optimization:** These indexes are designed to enhance the performance of read-heavy operations such as `SELECT`, `JOIN`, `WHERE`, and `GROUP BY`.
- **Write Performance Impact:** While indexes slightly slow down write operations (`INSERT`, `UPDATE`, `DELETE`), the tradeoff is acceptable given the read-heavy nature of the workload.

### Notes

- The `idx_overview` index is a full-text index and is crucial for queries that involve searching for specific text in the movie descriptions.
- Composite indexes (e.g., `idx_movie_genres_genre_movie` and `idx_movies_vote_movie`) are used for optimizing queries that involve multiple columns for filtering, grouping, or sorting.

## Setup and Usage

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create the Database

Run the following script to create the database schema:

```bash
python src/create_db_script.py
```

### 3. Populate the Database

Fetch and insert data from TMDB API:

```bash
python src/api_data_retrieve.py
```

### 4. Execute Queries

Run queries to interact with the database:

```bash
python src/queries_execution.py
```

## System Documentation

Detailed descriptions of the database schema, design rationale, and optimizations are available in `system_docs.pdf`.

## Error Handling

The scripts include robust error handling to manage API failures, database connection issues, and data insertion conflicts.

## License

This project is developed for educational purposes and follows the academic guidelines set by the institution.

---

## Creators / Maintainers

- Shai Goldbourt([Shaigoldbourt22](https://github.com/Shaigoldbourt22))
- Dor Liberman ([dorlib](https://github.com/dorlib))

If you have any questions or feedback, I would be glad if you will contact us via mail.

<p align="left">
  <a href="dorlibrm@gmail.com"> 
    <img alt="Connect via Email" src="https://img.shields.io/badge/Gmail-c14438?style=flat&logo=Gmail&logoColor=white" />
  </a>
</p>

This project was created for educational purposes, for personal and open-source use.

---
