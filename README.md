# Movie Database Management System

<p align="center">
    <img alt="Issues" src="https://img.shields.io/github/issues-raw/Shaigoldbourt22/DbProject"/>
    <img alt="pull request" src="https://img.shields.io/github/issues-pr-closed/Shaigoldbourt22/DbProject"/>
    <img alt="stars" src="https://img.shields.io/github/stars/Shaigoldbourt22/DbProject?style=social">
    <img alt="updated" src="https://img.shields.io/github/last-commit/Shaigoldbourt22/DbProject">
    <img alt="size" src="https://img.shields.io/github/repo-size/Shaigoldbourt22/DbProject" >
</p>

## Overview
This project involves the creation of a movie-centered database management system (DBMS) using MySQL and Python. The system fetches data from The Movie Database (TMDB) API and stores it in a well-structured MySQL database. Additionally, the project includes five distinct database queries to analyze the stored data, focusing on specific aspects of the movie industry. While the project emphasizes backend development, a frontend design is documented to illustrate the intended application interface.

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
│   └── queries_execution.py      # Demonstrates query executions
│
├── documentation/
│   ├── user_manual.pdf           # Application functionality and design
│   ├── system_docs.pdf           # Database schema and design rationale
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
1. **Query 1**: 
2. **Query 2**: 
3. **Query 3**: 
4. **Query 4**: 
5. **Query 5**: Find top 5 directors by average vote_average of the movies they directed

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
Run example queries to interact with the database:
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

If you like my content or find my code useful, give it a :star: 


---
