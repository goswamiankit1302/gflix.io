import streamlit as st
import pandas as pd
import numpy as np
import math
import random

st.set_page_config(page_title="Gflix", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for Netflix-like styling
st.markdown("""
<style>
    .main {
        background-color: #141414;
        color: white;
    }
    .stButton>button {
        background-color: #e50914;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #f40612;
    }
    .movie-card {
        background-color: #333;
        border-radius: 10px;
        padding: 10px;
        margin: 5px;
        text-align: center;
    }
    .hero {
        background: linear-gradient(to right, rgba(0,0,0,0.8), rgba(0,0,0,0.2)), url('https://image.tmdb.org/t/p/original/9cqNxx0GxF0bflZmeSMuL5tnGzr.jpg');
        background-size: cover;
        color: white;
        padding: 100px 50px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .recommendation-glance {
        background-color: #333;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        display: flex;
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

# Movie data with posters and IMDb ratings
movies = [
    {"title": "The Shawshank Redemption", "genre": "Drama", "poster": "https://image.tmdb.org/t/p/w500/9cqNxx0GxF0bflZmeSMuL5tnGzr.jpg", "year": 1994, "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.", "imdb_rating": 9.3, "trailer": "https://www.youtube.com/watch?v=6hB3S9bIaco"},
    {"title": "The Godfather", "genre": "Crime", "poster": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg", "year": 1972, "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.", "imdb_rating": 9.2, "trailer": "https://www.youtube.com/watch?v=sY1S34973zA"},
    {"title": "The Dark Knight", "genre": "Action", "poster": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg", "year": 2008, "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests.", "imdb_rating": 9.0, "trailer": "https://www.youtube.com/watch?v=EXeTwQWrcwY"},
    {"title": "Pulp Fiction", "genre": "Crime", "poster": "https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg", "year": 1994, "description": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.", "imdb_rating": 8.9, "trailer": "https://www.youtube.com/watch?v=s7EdQ4FqbhY"},
    {"title": "Forrest Gump", "genre": "Drama", "poster": "https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg", "year": 1994, "description": "The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate, and other historical events unfold through the perspective of an Alabama man.", "imdb_rating": 8.8, "trailer": "https://www.youtube.com/watch?v=bLvqoHBptjg"},
    {"title": "Inception", "genre": "Sci-Fi", "poster": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg", "year": 2010, "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.", "imdb_rating": 8.8, "trailer": "https://www.youtube.com/watch?v=YoHD9XEInc0"},
    {"title": "The Matrix", "genre": "Sci-Fi", "poster": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg", "year": 1999, "description": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.", "imdb_rating": 8.7, "trailer": "https://www.youtube.com/watch?v=vKQi3bBA1y8"},
    {"title": "Titanic", "genre": "Romance", "poster": "https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg", "year": 1997, "description": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.", "imdb_rating": 7.9, "trailer": "https://www.youtube.com/watch?v=kVrqfYjkTdQ"},
    {"title": "Avatar", "genre": "Sci-Fi", "poster": "https://image.tmdb.org/t/p/w500/kyeqWdyUXW608qlYkRqosgbbJyK.jpg", "year": 2009, "description": "A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.", "imdb_rating": 7.9, "trailer": "https://www.youtube.com/watch?v=5PSNL1qE6VY"},
    {"title": "The Avengers", "genre": "Action", "poster": "https://image.tmdb.org/t/p/w500/RYMX2wcKCBAr24UyPD7xwmjaTn.jpg", "year": 2012, "description": "Earth's mightiest heroes must come together and learn to fight as a team if they are going to stop the mischievous Loki and his alien army from enslaving humanity.", "imdb_rating": 8.0, "trailer": "https://www.youtube.com/watch?v=eOrNdBpGMv8"},
    {"title": "Interstellar", "genre": "Sci-Fi", "poster": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg", "year": 2014, "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.", "imdb_rating": 8.6, "trailer": "https://www.youtube.com/watch?v=zSWdZVtXT7E"},
    {"title": "The Lord of the Rings: The Fellowship of the Ring", "genre": "Fantasy", "poster": "https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg", "year": 2001, "description": "A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring.", "imdb_rating": 8.8, "trailer": "https://www.youtube.com/watch?v=V75dMMIW2B4"},
    {"title": "Fight Club", "genre": "Drama", "poster": "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg", "year": 1999, "description": "An insomniac office worker and a devil-may-care soapmaker form an underground fight club.", "imdb_rating": 8.8, "trailer": "https://www.youtube.com/watch?v=SUXWAEX2jlg"},
    {"title": "The Silence of the Lambs", "genre": "Thriller", "poster": "https://image.tmdb.org/t/p/w500/uS9m8OBk1A8eM9I042bx8XXpqAq.jpg", "year": 1991, "description": "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer.", "imdb_rating": 8.6, "trailer": "https://www.youtube.com/watch?v=W6Mm8Sbe__o"},
    {"title": "Schindler's List", "genre": "Drama", "poster": "https://image.tmdb.org/t/p/w500/sF1U4EUQS8YHUYjNl3pMGNIQyr0.jpg", "year": 1993, "description": "In German-occupied Poland during World War II, Oskar Schindler gradually becomes concerned for his Jewish workforce.", "imdb_rating": 8.9, "trailer": "https://www.youtube.com/watch?v=JdRGC-w9syA"}
]

# Initialize session state for recommendations
if "recommendations" not in st.session_state:
    st.session_state.recommendations = {movie["title"]: 0 for movie in movies}
if "last_recommended" not in st.session_state:
    st.session_state.last_recommended = None
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Home", "Trending", "My List", "Search", "Statistics"])

with tab1:
    # Hero Section
    featured = random.choice(movies)
    st.markdown(f"""
    <div class="hero">
        <h1>{featured['title']} ({featured['year']})</h1>
        <p>A great movie in the {featured['genre']} genre.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Watch Now", key="hero_watch"):
        st.session_state.selected_movie = featured
        st.rerun()

    # Sidebar for search and filters
    st.sidebar.title("Gflix")
    search_query = st.sidebar.text_input("Search Movies")
    genre_filter = st.sidebar.multiselect("Genres", options=list(set(m["genre"] for m in movies)))

    # Filter movies
    filtered_movies = movies
    if search_query:
        filtered_movies = [m for m in movies if search_query.lower() in m["title"].lower()]
    if genre_filter:
        filtered_movies = [m for m in filtered_movies if m["genre"] in genre_filter]

    # Recommendation Section
    st.subheader("Get a Recommendation")
    if st.button("Recommend Me a Movie"):
        if filtered_movies:
            recommended = random.choice(filtered_movies)
            st.session_state.recommendations[recommended["title"]] += 1
            st.session_state.last_recommended = recommended
            st.rerun()
        else:
            st.write("No movies match your filters.")

    # Show glance of last recommended
    if st.session_state.last_recommended:
        rec = st.session_state.last_recommended
        st.markdown(f"""
        <div class="recommendation-glance">
            <img src="{rec['poster']}" width="150" style="margin-right: 20px;">
            <div>
                <h2>{rec['title']} ({rec['year']})</h2>
                <p><strong>Genre:</strong> {rec['genre']}</p>
                <p><strong>IMDb Rating:</strong> {rec['imdb_rating']}/10</p>
                <p>{rec['description']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    if st.button("Clear Recommendation", key="clear_rec"):
        st.session_state.last_recommended = None
        st.rerun()

    # Group by genre
    genres = list(set(m["genre"] for m in filtered_movies))
    for genre in genres:
        genre_movies = [m for m in filtered_movies if m["genre"] == genre]
        if genre_movies:
            st.subheader(genre)
            cols = st.columns(5)
            for i, movie in enumerate(genre_movies[:5]):
                with cols[i % 5]:
                    st.image(movie["poster"], width=150, caption=movie["title"])
                    if st.button("Details", key=f"{movie['title']}_details_home"):
                        st.session_state.selected_movie = movie
                        st.rerun()

# Details modal (shared across tabs)
if "selected_movie" in st.session_state:
    movie = st.session_state.selected_movie
    with st.expander(f"Details for {movie['title']}", expanded=True):
        st.image(movie["poster"], width=300)
        st.write(f"**Genre:** {movie['genre']}")
        st.write(f"**Year:** {movie['year']}")
        st.write(f"**IMDb Rating:** {movie['imdb_rating']}/10")
        st.write(movie["description"])
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Add to My List"):
                if movie["title"] not in st.session_state.watchlist:
                    st.session_state.watchlist.append(movie["title"])
                    st.success("Added to My List!")
                else:
                    st.info("Already in My List.")
        with col2:
            if st.button(f"Watch Trailer"):
                st.markdown(f"[Watch Trailer]({movie['trailer']})", unsafe_allow_html=True)
        if st.button("Close"):
            del st.session_state.selected_movie
            st.rerun()

with tab2:
    st.header("Trending Now")
    # Sort by rating descending
    trending = sorted(movies, key=lambda x: x["imdb_rating"], reverse=True)[:10]
    cols = st.columns(5)
    for i, movie in enumerate(trending):
        with cols[i % 5]:
            st.image(movie["poster"], width=150, caption=f"{movie['title']} ({movie['imdb_rating']})")
            if st.button("Details", key=f"{movie['title']}_trending"):
                st.session_state.selected_movie = movie
                st.rerun()

with tab3:
    st.header("My List")
    if st.session_state.watchlist:
        watchlist_movies = [m for m in movies if m["title"] in st.session_state.watchlist]
        cols = st.columns(5)
        for i, movie in enumerate(watchlist_movies):
            with cols[i % 5]:
                st.image(movie["poster"], width=150, caption=movie["title"])
                if st.button("Details", key=f"{movie['title']}_list"):
                    st.session_state.selected_movie = movie
                    st.rerun()
                if st.button("Remove", key=f"{movie['title']}_remove"):
                    st.session_state.watchlist.remove(movie["title"])
                    st.rerun()
    else:
        st.write("Your list is empty. Add movies from the details view.")

with tab4:
    st.header("Advanced Search")
    col1, col2, col3 = st.columns(3)
    with col1:
        search_title = st.text_input("Movie Title")
    with col2:
        search_genre = st.selectbox("Genre", ["All"] + list(set(m["genre"] for m in movies)))
    with col3:
        min_rating = st.slider("Min IMDb Rating", 0.0, 10.0, 0.0)
    
    search_results = movies
    if search_title:
        search_results = [m for m in search_results if search_title.lower() in m["title"].lower()]
    if search_genre != "All":
        search_results = [m for m in search_results if m["genre"] == search_genre]
    search_results = [m for m in search_results if m["imdb_rating"] >= min_rating]
    
    if search_results:
        cols = st.columns(5)
        for i, movie in enumerate(search_results):
            with cols[i % 5]:
                st.image(movie["poster"], width=150, caption=movie["title"])
                if st.button("Details", key=f"{movie['title']}_search"):
                    st.session_state.selected_movie = movie
                    st.rerun()
    else:
        st.write("No movies found matching your criteria.")

with tab5:
    st.header("Statistics")
    
    # Total recommendations
    total_rec = sum(st.session_state.recommendations.values())
    st.write(f"Total Recommendations: {total_rec}")
    
    # Bar chart of recommendations per movie
    rec_df = pd.DataFrame(list(st.session_state.recommendations.items()), columns=["Movie", "Count"])
    rec_df = rec_df[rec_df["Count"] > 0].sort_values("Count", ascending=False)
    if not rec_df.empty:
        st.subheader("Recommendations by Movie")
        st.bar_chart(rec_df.set_index("Movie"))
    else:
        st.write("No recommendations yet.")
    
    # Genre stats
    genre_counts = {}
    for movie in movies:
        genre = movie["genre"]
        count = st.session_state.recommendations[movie["title"]]
        genre_counts[genre] = genre_counts.get(genre, 0) + count
    
    genre_df = pd.DataFrame(list(genre_counts.items()), columns=["Genre", "Count"])
    genre_df = genre_df[genre_df["Count"] > 0]
    if not genre_df.empty:
        st.subheader("Recommendations by Genre")
        st.bar_chart(genre_df.set_index("Genre"))
    
    # Most recommended movie
    if rec_df.empty:
        st.write("No data available.")
    else:
        top_movie = rec_df.iloc[0]["Movie"]
        st.write(f"Most Recommended Movie: {top_movie} ({rec_df.iloc[0]['Count']} times)")
    
    # IMDb Ratings Stats
    st.header("IMDb Ratings Statistics")
    
    # Top rated movies
    rating_df = pd.DataFrame([(m["title"], m["imdb_rating"]) for m in movies], columns=["Movie", "Rating"]).sort_values("Rating", ascending=False)
    st.subheader("Top Rated Movies")
    st.bar_chart(rating_df.set_index("Movie"))
    
    # Average rating by genre
    genre_ratings = {}
    genre_counts_rating = {}
    for movie in movies:
        genre = movie["genre"]
        rating = movie["imdb_rating"]
        if genre not in genre_ratings:
            genre_ratings[genre] = 0
            genre_counts_rating[genre] = 0
        genre_ratings[genre] += rating
        genre_counts_rating[genre] += 1
    
    avg_genre_df = pd.DataFrame([(g, genre_ratings[g] / genre_counts_rating[g]) for g in genre_ratings], columns=["Genre", "Average Rating"]).sort_values("Average Rating", ascending=False)
    st.subheader("Average IMDb Rating by Genre")
    st.bar_chart(avg_genre_df.set_index("Genre"))
