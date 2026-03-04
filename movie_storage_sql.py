import sqlalchemy
from sqlalchemy import create_engine, text

DB_URL = "sqlite:///movies.db"
engine = create_engine(DB_URL)


def init_db():
    """Initialize the database and create the table with a poster column."""
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                poster TEXT
            )
        """))
        connection.commit()

def add_movie(title, year, rating, poster_url):
    """Add a new movie including its poster URL."""
    with engine.connect() as connection:
        try:
            connection.execute(text("""
                INSERT INTO movies (title, year, rating, poster) 
                VALUES (:title, :year, :rating, :poster)
            """), {"title": title, "year": year, "rating": rating, "poster": poster_url})
            connection.commit()
        except Exception as error:
            print(f"Database error: {error}")

def list_movies():
    """Retrieve all movies including posters."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster FROM movies"))
        movies = result.fetchall()
    return {row[0]: {"year": row[1], "rating": row[2], "poster": row[3]} for row in movies}


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            # We use rowcount to check if a movie was actually found and deleted
            result = connection.execute(
                text("DELETE FROM movies WHERE title = :title"),
                {"title": title}
            )
            connection.commit()

            if result.rowcount > 0:
                print(f"Movie '{title}' deleted successfully.")
            else:
                print(f"Movie '{title}' not found.")
        except Exception as error:
            print(f"Error deleting movie: {error}")


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            result = connection.execute(
                text("UPDATE movies SET rating = :rating WHERE title = :title"),
                {"rating": rating, "title": title}
            )
            connection.commit()

            if result.rowcount > 0:
                print(f"Rating for '{title}' updated to {rating}.")
            else:
                print(f"Movie '{title}' not found.")
        except Exception as error:
            print(f"Error updating movie: {error}")
