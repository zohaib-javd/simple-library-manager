import streamlit as st
import sqlite3
from datetime import datetime

# Set page configuration with title and icon
st.set_page_config(page_title="Simple Library Manager", page_icon="📚")

# ------------------------------
# Database Setup and Functions
# ------------------------------
def init_db():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT UNIQUE,
            author TEXT,
            year INTEGER,
            genre TEXT,
            rating INTEGER,
            date_added TEXT,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_book(title, author, year, genre, rating, notes):
    try:
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        date_added = datetime.now().strftime("%Y-%m-%d")
        c.execute('''
            INSERT INTO books 
            (title, author, year, genre, rating, date_added, notes)
            VALUES (?,?,?,?,?,?,?)
        ''', (title, author, year, genre, rating, date_added, notes))
        conn.commit()
        st.success("Book added successfully!")
    except sqlite3.IntegrityError:
        st.error("This book already exists in the library!")
    finally:
        conn.close()

def get_books():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM books ORDER BY title')
    books = c.fetchall()
    conn.close()
    return books

def delete_book(book_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    st.success("Book deleted successfully!")

# Initialize the database
init_db()

# ------------------------------
# Sidebar: Contact and Special Thanks Toggle
# ------------------------------
with st.sidebar.expander("📲 Connect with me", expanded=False):
    st.markdown("""
**🔗 LinkedIn:** [Zohaib Javed](https://www.linkedin.com/in/zohaib-javd)  
**👨‍💻 GitHub:** [zohaib-javd](https://www.github.com/zohaib-javd)  
**📧 Email:** [zohaibjaved@gmail.com](mailto:zohaibjaved@gmail.com)  
**❎ X:** [zohaibjaved](https://x.com/zohaibjaved)
    """)
    st.markdown("---")
    st.markdown("### 🧑‍🏫 Special thanks to all my teachers:")
    st.markdown("""
- Sir Zia Khan  
- Sir Daniyal Nagori  
- Sir Muhammad Qasim  
- Sir Ameen Alam  
- Sir Aneeq Khatri  
- Sir Okasha Aijaz  
- Sir Muhammad Osama  
- Sir Mubashir Ali  
- Sir Amjad Ali  
- Sir Naeem Hussain  
- Sir Fahad Ghouri  
- Sir Saleem Raza  
- Sir Shaikh Abdul Sami  
- Sir Abdullah Arain
    """)

# ------------------------------
# Main Streamlit UI
# ------------------------------
st.title("📚 Simple Library Manager")

# Sidebar menu for navigating between functions
menu = st.sidebar.radio("Menu", ["Add Book", "View Books", "Search Books"])

if menu == "Add Book":
    st.header("Add New Book")
    # Form for adding a new book
    with st.form("add_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Year", min_value=1800, max_value=datetime.now().year, step=1)
        genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science Fiction", "Mystery", "Other"])
        rating = st.slider("Rating", 1, 5)
        notes = st.text_area("Notes")
        
        submit = st.form_submit_button("Add Book")
        
    if submit:
        if title and author:
            add_book(title, author, year, genre, rating, notes)
        else:
            st.warning("Please fill in at least the Title and Author fields.")

elif menu == "View Books":
    st.header("Your Library")
    books = get_books()
    
    if books:
        for book in books:
            with st.expander(f"{book['title']} by {book['author']}"):
                st.write(f"**Year:** {book['year']}")
                st.write(f"**Genre:** {book['genre']}")
                st.write(f"**Rating:** {'⭐' * book['rating']}")
                st.write(f"**Added on:** {book['date_added']}")
                st.write(f"**Notes:** {book['notes']}")
                if st.button("Delete Book", key=f"del_{book['id']}"):
                    delete_book(book['id'])
                    st.rerun()
    else:
        st.info("No books in the library yet!")

elif menu == "Search Books":
    st.header("Search Books")
    search_term = st.text_input("Search by title, author, or genre")
    
    if search_term:
        books = get_books()
        results = [
            b for b in books
            if search_term.lower() in b['title'].lower() or
               search_term.lower() in b['author'].lower() or
               search_term.lower() in b['genre'].lower()
        ]
        
        if results:
            st.subheader(f"Found {len(results)} result(s):")
            for book in results:
                st.write(f"- **{book['title']}** by {book['author']} ({book['year']})")
        else:
            st.info("No matching books found.")

# Footer
st.markdown("---")
st.caption("Developed by Zohaib Javed | Simple Library Manager v1.0")
