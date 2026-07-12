import streamlit as st
import pickle


# -----------------------
# Load files
# -----------------------

movies = pickle.load(
    open("anime_list.pkl","rb")
)

recommendations = pickle.load(
open("recommendations.pkl","rb")
)


# -----------------------
# Recommendation function
# -----------------------

def recommend(anime):

    # Find selected anime MAL_ID

    anime_id = movies[
        movies['title']==anime
    ]['MAL_ID'].values[0]


    recommended_names = []
    recommended_posters = []
    recommended_studios = []
    scores = []


    # Get stored recommendations

    for item in recommendations[anime_id]:


        recommended_id = item['MAL_ID']

        score = item['score']


        # Find anime details

        anime_info = movies[
            movies['MAL_ID']==recommended_id
        ].iloc[0]


        recommended_names.append(
            anime_info['title']
        )


        recommended_posters.append(
            anime_info['image_jpg_large_url']
        )


        recommended_studios.append(
            anime_info['studios']
        )


        scores.append(
            round(score*100,2)
        )


    return (
        recommended_names,
        recommended_posters,
        recommended_studios,
        scores
    )


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
