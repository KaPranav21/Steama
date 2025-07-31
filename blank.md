# Steam DB Systems Project
## Goal:
Build a backend system that connects to the Steam Web API to fetch user and game data and stores it in an SQL database.

## Stack:

(prone to change)
| Tool / Concept            | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| **Python**               | Main programming language for logic and automation.                        |
| **requests**             | Python library for making HTTP requests to Steam API.                      |
| **.env + python-dotenv** | Manages your API key securely using environment variables.                 |
| **SQL**                  | Query language for interacting with your database.                         |
| **MySQL / SQLite**       | Relational database to store user and game data.                           |
| **mysql-connector / sqlite3** | Python libraries to connect to your database.                         |
| **SQL Schema**           | Design of your tables and relationships (users, games, ownership).         |
| **Terminal + Git**       | (Optional) Tools for running scripts and version control.      

## Tasks 1:
- Connect to the Steam Web API using an API key
- Fetch user profile data and owned games list
- Design a simple database schema with tables for users, games, and ownership
- Insert the fetched data into the SQL database
- Verify the data insertion with basic SELECT queries and tests

## Tasks 2:
- Fetch more detailed game information from Steam API
- Enhance database schema to include detailed game info
- Calculate and store user playtime statistics
- Develop SQL queries for insights
- Implement a command-line interface (CLI)



