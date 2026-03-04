# 🎬 My Movies Database (CLI & Web)

My Movies Database is a Python-based application designed to manage personal movie collections. It allows users to store their favorite films in a local database, with data automatically enriched via the OMDb API.

---

## 🚀 Features

* **API Integration:** Fetches movie details (Poster, Year, Rating) automatically using the OMDb API.
* **SQL Storage:** Persistent data management using SQLAlchemy and SQLite.
- **CLI Interface:** User-friendly menu to list, add, delete, search, and view statistics.
* **Web Generation:** Export your movie collection into a beautiful, responsive HTML dashboard.
* **Reliability:** Built-in error handling for API connections and database integrity.

---

## 🛠️ Installation & Setup

To run the project locally, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone [<your-repository-url>](https://github.com/84edu/Movie-Project---SQL-HTML-API.git)
    cd Movie-Project---SQL-HTML-API
    ```

2.  **Install Dependencies:**
    Make sure you have Python installed, then run:
    ```bash
    pip install sqlalchemy requests python-dotenv
    ```

3.  **Environment Variables:**
    Create a `.env` file in the root directory and add your OMDb API key:
    ```env
    API_KEY=your_omdb_api_key_here
    ```

4.  **Run the Application:**
    ```bash
    python movies.py
    ```

---

## 🗃️ Database & Web Export

The project uses **SQLite** with **SQLAlchemy** for data persistence.

* **Automatic Setup:** The database table is automatically initialized upon the first run of the application.
* **Website Generation:** Use option **9** in the menu to generate a professional `index.html`.
* **Viewing the Dashboard:** To view your collection, simply open the generated `index.html` file in your favorite web browser.
* **Git Notice:** The `movies.db` file, the `.env` file, and the generated `index.html` are excluded from the repository to ensure privacy and clean version control.

---

## 📂 Project Structure

- `movies.py`: The main entry point containing the CLI logic.
- `movie_storage_sql.py`: Handles all database operations.
- `_static/`: Contains the `index_template.html` and `style.css` required for the web export.

---

## 📝 License
This project was created for educational purposes.
