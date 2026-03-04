import random, requests, statistics, os
import movie_storage_sql as storage
from dotenv import load_dotenv

load_dotenv()

OMDB_API_KEY = os.getenv('API_KEY')
BASE_URL = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t="

if not OMDB_API_KEY:
    raise ValueError("No API_KEY found in environment variables!")

def list_movies():
    """Retrieve and display all movies including the poster data."""
    movies = storage.list_movies()
    print(f"\n{len(movies)} movies in total:")
    for title, data in movies.items():
        year = data.get("year")
        rating = data.get("rating")
        poster = data.get("poster")
        print(f"- {title} ({year}): {rating} | Poster: {poster}")


def add_movie():
    """Fetch movie data from OMDb API and save it to the database."""
    movie_title = input("Enter the movie name: ").strip()
    if not movie_title:
        print("The movie name cannot be empty!")
        return

    movies = storage.list_movies()
    if movie_title.lower() in [title.lower() for title in movies.keys()]:
        print(f"Movie '{movie_title}' already exists in the database.")
        return

    try:
        response = requests.get(BASE_URL + movie_title, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "False":
            print(f"Error: {data.get('Error', 'Movie not found in OMDb!')}")
            return

        title = data.get("Title")
        year_str = data.get("Year", "0")
        year = int(year_str[:4]) if year_str != "N/A" else 0

        try:
            rating = float(data.get("imdbRating", 0.0))
        except ValueError:
            rating = 0.0

        poster = data.get("Poster", "N/A")

        storage.add_movie(title, year, rating, poster)
        print(f"Successfully added '{title}' ({year}) with Rating {rating}.")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Check your internet connection.")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


def delete_movie():
    """Delete a movie from the database."""
    movies = storage.list_movies()
    movie_name = input("Enter the movie name you want to delete: ").strip()

    original_key = None
    for title in movies.keys():
        if title.lower() == movie_name.lower():
            original_key = title
            break

    if original_key is None:
        print(f"Error: The movie '{movie_name}' does not exist in the database!")
    else:
        storage.delete_movie(original_key)
        print(f"Movie '{movie_name}' was deleted successfully.")


def update_movie():
    """Update a movie in the database."""
    movies = storage.list_movies()
    movie_name = input("Enter the movie name you want to update: ").strip()

    original_key = None
    for title in movies.keys():
        if title.lower() == movie_name.lower():
            original_key = title
            break

    if original_key is None:
        print(f"Error: The movie '{movie_name}' does not exist in the database!")
    else:
        while True:
            try:
                movie_rating = float(input(f"Enter the new Rating for {original_key} (1-10): "))
                if 1 <= movie_rating <= 10:
                    break
                print("Please enter a rating between 1 and 10.")
            except ValueError:
                print("Invalid input! Please enter a number for the rating.")

        storage.update_movie(original_key, movie_rating)
        print(f"Movie '{original_key}' updated successfully!")


def stats():
    """Display statistics of movies from the database."""
    movies = storage.list_movies()
    if not movies:
        print("Database is empty!")
        return

    ratings = [data["rating"] for data in movies.values()]

    average_rating = statistics.mean(ratings)
    print(f"Average rating of filmes: {average_rating:.1f}")

    median = statistics.median(ratings)

    print(f"Median of ratings: {median:.1f}")

    best_rating = max(ratings)
    worst_rating = min(ratings)

    best_movies = [title for title, data in movies.items()
                   if (data["rating"]) == best_rating]
    worst_movies = [title for title, data in movies.items()
                    if (data["rating"]) == worst_rating]

    print(f"Best movie(s): {', '.join(best_movies)}, Rating: {best_rating}")
    print(f"Worst movie(s): {', '.join(worst_movies)}, Rating: {worst_rating}")


def random_movie():
    """Select and display a random movie from the database."""
    movies = storage.list_movies()
    title = random.choice(list(movies.keys()))
    data = movies[title]
    print(f"Here is your random movie with its rating: {title} ({data['year']}), {data['rating']}")


def search_movie():
    """Search among all movies in the database."""
    movies = storage.list_movies()
    search_term = input("Enter part of the movie name: ").strip().lower()
    found = False

    for title, data in movies.items():
        if search_term in title.lower():
            print(f"{title} ({data['year']}), {data['rating']}")
            found = True

    if not found:
        print(f"No movies found containing '{search_term}'.")


def sorted_movies():
    """Display a sorted list of all movies from the database."""
    movies = storage.list_movies()
    sorted_list = sorted(movies.items(), key=lambda item: item[1]['rating'], reverse=True)

    print("\nMovies sorted by rating:")
    for title, data in sorted_list:
        year = data['year']
        rating = data['rating']
        print(f"{title} ({year}): {rating}")


def main():
    storage.init_db()
    print("\n********** My Movies Database **********")

    while True:
        print(
            "\nMenu:\n"
            "0. Exit\n"
            "1. List movies\n"
            "2. Add movie\n"
            "3. Delete movie\n"
            "4. Update movie\n"
            "5. Stats\n"
            "6. Random movie\n"
            "7. Search movie\n"
            "8. Movies sorted by rating"
        )

        choice = input("\nEnter choice (0-8): ")

        if choice == "0":
            print("Bye!")
            break

        if choice == "1":
            list_movies()

        elif choice == "2":
            add_movie()

        elif choice == "3":
            delete_movie()

        elif choice == "4":
            update_movie()

        elif choice == "5":
            stats()

        elif choice == "6":
            random_movie()

        elif choice == "7":
            search_movie()

        elif choice == "8":
            sorted_movies()

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
