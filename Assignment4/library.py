import streamlit as st

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .stTextInput input, .stNumberInput input, .stTextArea textarea {
        border-radius: 5px;
        border: 1px solid #ccc;
        padding: 10px;
    }
    .stHeader {
        color: #4CAF50;
    }
    .stDataFrame {
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize the library in session state
if "library" not in st.session_state:
    st.session_state.library = []

# Title of the app
st.markdown("<h1 class='stHeader'>📚 Personal Library Manager</h1>", unsafe_allow_html=True)

# Sidebar for navigation
with st.sidebar:
    st.markdown("<h2 class='stHeader'>🔍 Navigation</h2>", unsafe_allow_html=True)
    option = st.radio(
        "Choose an option:",
        ["🏠 Home", "➕ Add Book", "✏️ Edit Book", "🗑️ Remove Book", "🔎 Search Book", "📊 Statistics"],
    )

# Home Page
if option == "🏠 Home":
    st.markdown("<h2 class='stHeader'>🏠 Home</h2>", unsafe_allow_html=True)
    st.write("Welcome to your Personal Library Manager! Here's your current library:")

    # Display the library on the Home page
    if st.session_state.library:
        for i, book in enumerate(st.session_state.library):
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 2, 2])
                with col1:
                    st.markdown(f"**Title:** {book['title']}")
                with col2:
                    st.markdown(f"**Author:** {book['author']}")
                with col3:
                    st.markdown(f"**Year:** {book['year']}")
                with col4:
                    st.markdown(f"**Genre:** {book['genre']}")
                with col5:
                    st.markdown(f"**Read:** {'✅ Yes' if book['read'] else '❌ No'}")
            st.markdown("---")
    else:
        st.info("Your library is empty. Add some books to get started!")

# Add Book Page
elif option == "➕ Add Book":
    st.markdown("<h2 class='stHeader'>➕ Add a Book</h2>", unsafe_allow_html=True)
    title = st.text_input("Title", placeholder="Enter the book title")
    author = st.text_input("Author", placeholder="Enter the author's name")
    year = st.number_input("Publication Year", min_value=600, max_value=2100, step=1, value=2023)
    genre = st.text_input("Genre", placeholder="Enter the genre")
    read_status = st.checkbox("Have you read this book?")
    if st.button("Add Book", key="add_book"):
        if title and author and year and genre:
            book = {
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "read": read_status
            }
            st.session_state.library.append(book)
            st.success("Book added successfully!")  # Success message
            st.rerun()  # Refresh the page to show the updated library
        else:
            st.error("Please fill in all fields.")

# Edit Book Page
elif option == "✏️ Edit Book":
    st.markdown("<h2 class='stHeader'>✏️ Edit a Book</h2>", unsafe_allow_html=True)
    if st.session_state.library:
        # Dropdown to select a book to edit
        book_titles = [book["title"] for book in st.session_state.library]
        selected_title = st.selectbox("Select a book to edit:", book_titles)
        selected_book = next(book for book in st.session_state.library if book["title"] == selected_title)

        # Form to edit the selected book
        with st.form("edit_book_form"):
            new_title = st.text_input("Title", value=selected_book["title"])
            new_author = st.text_input("Author", value=selected_book["author"])
            new_year = st.number_input("Publication Year", value=selected_book["year"], min_value=1800, max_value=2100, step=1)
            new_genre = st.text_input("Genre", value=selected_book["genre"])
            new_read_status = st.checkbox("Have you read this book?", value=selected_book["read"])
            if st.form_submit_button("Save Changes"):
                selected_book["title"] = new_title
                selected_book["author"] = new_author
                selected_book["year"] = new_year
                selected_book["genre"] = new_genre
                selected_book["read"] = new_read_status
                st.success("Book updated successfully!")
                st.rerun()
    else:
        st.info("Your library is empty. Add some books to get started!")

# Remove Book Page
elif option == "🗑️ Remove Book":
    st.markdown("<h2 class='stHeader'>🗑️ Remove a Book</h2>", unsafe_allow_html=True)
    if st.session_state.library:
        # Dropdown to select a book to remove
        book_titles = [book["title"] for book in st.session_state.library]
        selected_title = st.selectbox("Select a book to remove:", book_titles)
        if st.button("Remove Book"):
            st.session_state.library = [book for book in st.session_state.library if book["title"] != selected_title]
            st.success("Book removed successfully!")
            st.rerun()
    else:
        st.info("Your library is empty. Add some books to get started!")

# Search Book Page
elif option == "🔎 Search Book":
    st.markdown("<h2 class='stHeader'>🔎 Search for a Book</h2>", unsafe_allow_html=True)
    search_query = st.text_input("Enter the title or author to search:")
    if search_query:
        results = [
            book for book in st.session_state.library
            if search_query.lower() in book["title"].lower() or search_query.lower() in book["author"].lower()
        ]
        if results:
            st.write("Matching Books:")
            for i, book in enumerate(results):
                st.markdown(f"""
                **Title:** {book['title']}  
                **Author:** {book['author']}  
                **Year:** {book['year']}  
                **Genre:** {book['genre']}  
                **Read:** {'✅ Yes' if book['read'] else '❌ No'}  
                ---
                """)
        else:
            st.info("No matching books found.")

# Statistics Page
elif option == "📊 Statistics":
    st.markdown("<h2 class='stHeader'>📊 Statistics</h2>", unsafe_allow_html=True)
    total_books = len(st.session_state.library)
    read_books = sum(book["read"] for book in st.session_state.library)
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Books", total_books)
    with col2:
        st.metric("Percentage Read", f"{percentage_read:.1f}%")