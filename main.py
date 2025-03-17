import json
import streamlit as st

# File to store library data
LIBRARY_FILE = "library.json"

def load_library():
    """Load library data from a file."""
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_library(library):
    """Save library data to a file."""
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

def add_book(library, title, author, year, genre, read):
    """Add a new book to the library."""
    book = {
        "Title": title,
        "Author": author,
        "Year": int(year),
        "Genre": genre,
        "Read": read
    }
    library.append(book)
    save_library(library)

def remove_book(library, title):
    """Remove a book from the library by title."""
    for book in library:
        if book["Title"].lower() == title.lower():
            library.remove(book)
            save_library(library)
            return True
    return False

def search_books(library, keyword):
    """Search for books by title or author."""
    return [book for book in library if keyword.lower() in book["Title"].lower() or keyword.lower() in book["Author"].lower()]

def display_statistics(library):
    """Display total books and percentage read."""
    total_books = len(library)
    read_books = sum(1 for book in library if book['Read'])
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
    return total_books, percentage_read

# Streamlit UI
st.title("📚 Personal Library Manager")

library = load_library()

menu = st.sidebar.selectbox("Menu", ["Add Book", "Remove Book", "Search Book", "View Library", "Statistics"])

if menu == "Add Book":
    st.header("Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1000, max_value=2100, step=1)
    genre = st.text_input("Genre")
    read = st.checkbox("Have you read this book?")
    if st.button("Add Book"):
        add_book(library, title, author, year, genre, read)
        st.success("Book added successfully!")

elif menu == "Remove Book":
    st.header("Remove a Book")
    title = st.text_input("Enter the title of the book to remove")
    if st.button("Remove Book"):
        if remove_book(library, title):
            st.success("Book removed successfully!")
        else:
            st.error("Book not found.")

elif menu == "Search Book":
    st.header("Search for a Book")
    keyword = st.text_input("Enter title or author name")
    if st.button("Search"):
        results = search_books(library, keyword)
        if results:
            for book in results:
                st.write(f"**{book['Title']}** by {book['Author']} ({book['Year']}) - {book['Genre']} - {'Read' if book['Read'] else 'Unread'}")
        else:
            st.warning("No matching books found.")

elif menu == "View Library":
    st.header("Your Library")
    if not library:
        st.write("Your library is empty.")
    else:
        for book in library:
            st.write(f"**{book['Title']}** by {book['Author']} ({book['Year']}) - {book['Genre']} - {'Read' if book['Read'] else 'Unread'}")

elif menu == "Statistics":
    st.header("Library Statistics")
    total_books, percentage_read = display_statistics(library)
    st.write(f"Total books: {total_books}")
    st.write(f"Percentage read: {percentage_read:.2f}%")
