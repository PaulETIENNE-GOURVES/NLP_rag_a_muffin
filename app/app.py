import streamlit as st
from utils import (
    retrieve_best_recipes,
    prompt_mistral,
    client,
)
import base64

# Fonction pour lire un fichier MP3 local
def play_local_mp3(file_path):
    with open(file_path, "rb") as f:
        mp3_bytes = f.read()
    mp3_base64 = base64.b64encode(mp3_bytes).decode("utf-8")

    # HTML pour lire le MP3 en fond
    audio_html = f"""
    <audio id="music" controls autoplay loop style="display:none;">
        <source src="data:audio/mp3;base64,{mp3_base64}" type="audio/mpeg">
    </audio>
    <script>
        document.getElementById('music').volume = 0.6; 
    </script>
    """
    st.components.v1.html(audio_html, height=0)


# Configuration de la page
st.set_page_config(page_title="Recettes RAG", layout="wide")

# Titre
st.title("🧁 Rasta Muffin, ton assistant culinaire et musical !🧁")

st.header("Rechercher des recettes")
query = st.text_input(
    "Quel type de muffin souhaites-tu cuisiner et avec quels ingrédients ?",
    "Exemple : Je veux un délicieux muffin au chocolat"
    )
if st.button("Rechercher"):
    if query:

        # Loading screen & music
        loading_placeholder = st.empty()
        loading_placeholder.image("./app/loading/loading.gif", caption="Recherche en cours (🔊 sound on ! 🔊)...", width=300)
        play_local_mp3("./app/loading/loading_music.mp3")


        best_recipes = retrieve_best_recipes(query)
        print(best_recipes)
        
        response = prompt_mistral(best_recipes, query)

        # remove loading gif
        loading_placeholder.empty()

        st.markdown("### Rasta Muffin te répond :")
        st.markdown(response)

    else:
        st.warning("Veuillez entrer des ingrédients.")

