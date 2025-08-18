

# import streamlit as st
# import pickle
# import pandas as pd
# import requests
# import os

# # Merge split similarity file
# def merge_similarity_file(output_file="similarity.pkl"):
#     parts = [f"similarity.pkl_part{i}" for i in range(8)]
#     with open(output_file, 'wb') as outfile:
#         for part in parts:
#             with open(part, 'rb') as infile:
#                 outfile.write(infile.read())


# # Merge onli if not already merged
# if not os.path.exists("similarity.pkl"):
#     merge_similarity_file()

# # load data 
# movies_dict = pickle.load(open('movie_dict.pkl' , 'rb'))
# movies = pd.DataFrame(movies_dict)
# similarity  = pickle.load(open('similarity.pkl', 'rb'))

# def fetch_poster(movie_id):
#     response = requests.get(
#         f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=94ec7a68ad87a416fc8517d3c47eb45f&language=en-US'
#     )
#     data = response.json()
#     # st.text(data)  # Optional: for debugging only
#     return "https://image.tmdb.org/t/p/w500" + data['poster_path']  # ✅ Fixed space

# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

#     recommended_movies = []
#     recommended_movies_posters = []
#     for i in movies_list:
#         movie_id = movies.iloc[i[0]]['id']
#         recommended_movies.append(movies.iloc[i[0]].title)
#         recommended_movies_posters.append(fetch_poster(movie_id))
#     return recommended_movies, recommended_movies_posters

# # Load data
# movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)
# similarity = pickle.load(open('similarity.pkl', 'rb'))

# # Streamlit UI
# st.title("Movie Recommender System")

# selected_movie_name = st.selectbox(
#     'Select a movie to get recommendations:',
#     movies['title'].values
# )

# if st.button('Recommend'):
#     names, posters = recommend(selected_movie_name)

#     col1, col2, col3, col4, col5 = st.columns(5)

#     with col1:
#         st.text(names[0])
#         st.image(posters[0])

#     with col2:
#         st.text(names[1])
#         st.image(posters[1])

#     with col3:
#         st.text(names[2])
#         st.image(posters[2])

#     with col4:
#         st.text(names[3])
#         st.image(posters[3])

#     with col5:
#         st.text(names[4])
#         st.image(posters[4])





import streamlit as st
import pickle
import pandas as pd
import requests
import io

# -------------------------------
# Function to rejoin similarity.pkl parts
# -------------------------------
def load_similarity():
    buffer = io.BytesIO()
    for i in range(8):  # Change this if you have more/less parts
        with open(f'similarity.pkl_part{i}', 'rb') as f:
            buffer.write(f.read())
    buffer.seek(0)
    return pickle.load(buffer)

# -------------------------------
# Function to fetch movie poster
# -------------------------------
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=94ec7a68ad87a416fc8517d3c47eb45f&language=en-US'
        )
        data = response.json()
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    except:
        return "https://via.placeholder.com/500x750.png?text=No+Poster"

# -------------------------------
# Recommendation Logic
# -------------------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_posters

# -------------------------------
# Load Data
# -------------------------------
st.title("🎬 Movie Recommender System")

# Load movie dictionary
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load similarity data from split files
similarity = load_similarity()

# -------------------------------
# UI
# -------------------------------
selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
