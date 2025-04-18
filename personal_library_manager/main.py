# library_manager_streamlit.py
import streamlit as st
import json
from datetime import datetime
from os import path

class LibraryManager:
    def __init__(self):
        self.books = []
        self.load_library()
        self.setup_page()

    def setup_page(self):
        st.set_page_config(page_title="Personal Library Manager", layout="wide")
        st.title("📚 Personal Library Manager")
        st.write(f"Current date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        st.write(f"Total books loaded: {len(self.books)}")

    def load_library(self):
        try:
            if path.exists("library.json"):
                with open("library.json", "r") as file:
                    self.books = json.load(file)
        except Exception as e:
            st.error(f"Error loading library: {str(e)}")
            self.books = []

    def save_library(self):
        try:
            with open("library.json", "w") as file:
                json.dump(self.books, file, indent=4)
            return True
        except Exception as e:
            st.error(f"Error saving library: {str(e)}")
            return False

    def add_book(self):
        with st.form("add_book_form"):
            st.subheader("📖 Add New Book")
            title = st.text_input("Title")
            author = st.text_input("Author")
            year = st.number_input("Publication Year", min_value=1800, max_value=datetime.now().year)
            genre = st.text_input("Genre")
            read = st.checkbox("Have you read this book?")
            
            if st.form_submit_button("Add Book"):
                if title and author and genre:
                    self.books.append({
                        "title": title,
                        "author": author,
                        "year": int(year),
                        "genre": genre,
                        "read": read,
                        "added_date": datetime.now().strftime("%Y-%m-%d")
                    })
                    self.save_library()
                    st.success(f"✅ '{title}' added successfully!")
                else:
                    st.warning("Please fill all required fields")

    def remove_book(self):
        st.subheader("🗑️ Remove Book")
        if not self.books:
            st.warning("Your library is empty!")
            return
            
        title_to_remove = st.selectbox(
            "Select book to remove",
            [book["title"] for book in self.books]
        )
        
        if st.button("Remove Book"):
            self.books = [book for book in self.books if book["title"] != title_to_remove]
            self.save_library()
            st.success(f"✅ '{title_to_remove}' removed successfully!")

    def search_books(self):
        st.subheader("🔍 Search Books")
        search_type = st.radio("Search by:", ["Title", "Author", "Genre", "Year"])
        search_term = st.text_input("Search term")
        
        if search_term:
            results = []
            if search_type == "Title":
                results = [b for b in self.books if search_term.lower() in b["title"].lower()]
            elif search_type == "Author":
                results = [b for b in self.books if search_term.lower() in b["author"].lower()]
            elif search_type == "Genre":
                results = [b for b in self.books if search_term.lower() in b["genre"].lower()]
            elif search_type == "Year":
                try:
                    year = int(search_term)
                    results = [b for b in self.books if b["year"] == year]
                except ValueError:
                    st.error("Please enter a valid year")
            
            self.display_books(results, "Search Results")

    def display_books(self, books=None, title="Your Library"):
        if books is None:
            books = self.books
            
        st.subheader(title)
        if not books:
            st.warning("No books found!")
            return
            
        for book in books:
            with st.expander(f"{book['title']} by {book['author']}"):
                st.write(f"**Year:** {book['year']}")
                st.write(f"**Genre:** {book['genre']}")
                st.write(f"**Read:** {'✓' if book['read'] else '✗'}")
                st.write(f"**Added:** {book.get('added_date', 'N/A')}")

    def show_stats(self):
        st.subheader("📊 Library Statistics")
        if not self.books:
            st.warning("Your library is empty!")
            return
            
        total = len(self.books)
        read = sum(1 for b in self.books if b["read"])
        genres = {b["genre"] for b in self.books}
        oldest = min(b["year"] for b in self.books)
        newest = max(b["year"] for b in self.books)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Books", total)
        col2.metric("Books Read", f"{read} ({read/total:.0%})")
        col3.metric("Genres", len(genres))
        
        st.write(f"**Publication years:** {oldest} to {newest}")
        st.write("**Genres:** " + ", ".join(genres))

    def run(self):
        menu = ["Home", "Add Book", "Remove Book", "Search Books", "View All Books", "Statistics"]
        choice = st.sidebar.selectbox("Menu", menu)
        
        if choice == "Home":
            st.write("Welcome to your personal library manager!")
            self.display_books()
        elif choice == "Add Book":
            self.add_book()
        elif choice == "Remove Book":
            self.remove_book()
        elif choice == "Search Books":
            self.search_books()
        elif choice == "View All Books":
            self.display_books()
        elif choice == "Statistics":
            self.show_stats()

if __name__ == "__main__":
    manager = LibraryManager()
    manager.run()

    # Footer branding
st.markdown("<div class='footer'>Created by <b>Ubaid Raza</b></div>", unsafe_allow_html=True)
