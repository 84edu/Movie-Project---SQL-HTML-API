import random
import statistics
import movie_storage_sql as storage


def list_movies():
    """Retrieve and display all movies from the database."""
    movies = storage.list_movies()
    print(f"{len(movies)} movies in total")
    for title, data in movies.items():
        rating = data.get("rating")
        year = data.get("year")
        print(f"{title} ({year}): {rating}")


def add_movie():
    """Add a new movie to the database."""
    movies = storage.list_movies()
    while True:
        movie_name = input("Enter the movie name: ").strip()
        if not movie_name:
            print("The movie name cannot be empty!")
            continue
        existing_movies = [title.lower() for title in movies.keys()]
        if movie_name.lower() in existing_movies:
            print(f"The movie {movie_name} is on our database. Please enter another movie.")
            continue
        break

    while True:
        try:
            movie_rating = float(input("Enter the movie Rating (1-10): "))
            if 1 <= movie_rating <= 10:
                break
            print("Please enter a rating between 1 and 10.")
        except ValueError:
            print("Invalid input! Please enter a number for the rating.")

    while True:
        try:
            movie_year = int(input("Enter the year of release (yyyy): "))
            if 1888 <= movie_year <= 2026:
                break
            print("Please enter a realistic year between 1888 and 2026 (e.g., 1994).")
        except ValueError:
            print("Invalid input! Please enter a valid year.")

    storage.add_movie(movie_name, movie_year, movie_rating)
    print(f"Movie '{movie_name}' added successfully!")


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
