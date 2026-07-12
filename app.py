import streamlit as st
import pickle


# -----------------------
# Load files
# -----------------------

movies = pickle.load(
    open("anime_list.pkl","rb")
)

similarity = pickle.load(
    open("similarity.pkl","rb")
)



# -----------------------
# Recommendation function
# -----------------------

def recommend(anime):

    index = movies[
        movies['title']==anime
    ].index[0]


    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x:x[1]
    )

    names = []
    posters = []
    studios = []
    scores = []

    for i in distances[1:6]:
        row = movies.iloc[i[0]]

        names.append(row['title'])

        posters.append(row['image_jpg_large_url'])

        studios.append(row['studios'])

        scores.append(round(i[1] * 100, 2))


    return names,posters,studios,scores



# -----------------------
# Streamlit UI
# -----------------------

st.set_page_config(
    page_title="Anime Recommendation System",
    layout="wide"
)

st.markdown(
    """
    <style>

    .anime-poster img {
        width: 200px;
        height: 280px;
        object-fit: cover;
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎌 Anime Recommendation System")


anime_list = movies['title'].values


selected_anime = st.selectbox(
    "Choose an anime",
    anime_list
)



if st.button("Recommend"):


    names, posters, studios, scores = recommend(selected_anime)


    st.subheader(
        "Recommended Anime"
    )


    cols = st.columns(5)

    for col, name, poster, studio, score in zip(
            cols,
            names,
            posters,
            studios,
            scores
    ):

        with col:
            st.markdown(
                f"""
                <div class="anime-poster">
                    <img src="{poster}">
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write(
                "**"+name+"**"
            )

            st.caption(
                studio
            )

            st.success(
                f"Similarity: {score}%"
            )