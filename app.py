import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests

# Load secrets
CLIENT_ID = st.secrets["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = st.secrets["SPOTIFY_CLIENT_SECRET"]
YOUR_GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def get_embed_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        embed_url = track["external_urls"]["spotify"].replace("open.spotify.com", "open.spotify.com/embed")
        return embed_url
    else:
        return None

def recommend(song):
    song_name, artist_name = song.split(" - ")
    index = music[(music['song'] == song_name) & (music['artist'] == artist_name)].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music = []
    for i in distances[1:6]:
        recommended_song = music.iloc[i[0]]
        recommended_music.append({
            'song': recommended_song['song'],
            'artist': recommended_song['artist'],
            'album_cover_url': get_song_album_cover_url(recommended_song['song'], recommended_song['artist']),
            'embed_url': get_embed_url(recommended_song['song'], recommended_song['artist'])
        })
    return recommended_music

def get_chatbot_response(query):
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={YOUR_GEMINI_API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {"text": query}
                ]
            }
        ]
    }
    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
        candidates = response_data.get("candidates", [])
        if candidates:
            return candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "Sorry, I couldn't process your request.")
        return "Sorry, I couldn't process your request."
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return "Sorry, I couldn't process your request due to a network error."
    except ValueError:
        return "Sorry, I received an invalid response from the server."

# Initialize session state
if 'recommended_music' not in st.session_state:
    st.session_state['recommended_music'] = []

# Sidebar for chatbot
st.sidebar.header('Ask Me Anything!')
user_query = st.sidebar.text_input("Type your question here...")
if st.sidebar.button('Ask'):
    bot_response = get_chatbot_response(user_query)
    st.sidebar.write(bot_response)

st.header('Music Recommender System')
music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Create a unique list of "song - artist" combinations for the dropdown
music['song_artist'] = music['song'] + " - " + music['artist']
music_list = music['song_artist'].unique()
selected_song = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

if st.button('Show Recommendation'):
    st.session_state['recommended_music'] = recommend(selected_song)
    song_name, artist_name = selected_song.split(" - ")
    st.session_state['selected_song_embed_url'] = get_embed_url(song_name, artist_name)

# Display the selected song's player
if 'selected_song_embed_url' in st.session_state and st.session_state['selected_song_embed_url']:
    st.write(f"### Now Playing: {selected_song}")
    st.components.v1.iframe(st.session_state['selected_song_embed_url'], height=80)

# Display recommendations if available in session state
if st.session_state['recommended_music']:
    recommended_music = st.session_state['recommended_music']
    cols = st.columns(5)
    
    for idx, col in enumerate(cols):
        with col:
            st.text(f"{recommended_music[idx]['song']} - {recommended_music[idx]['artist']}")
            st.image(recommended_music[idx]['album_cover_url'])
    
    for rec in recommended_music:
        st.write(f"**{rec['song']} - {rec['artist']}**")
        if rec['embed_url']:
            st.components.v1.iframe(rec['embed_url'], height=80)

    st.subheader("Feedback")
    feedback_text = st.text_area("What do you think of these recommendations?")
    rating = st.selectbox("Rate the recommendations out of 5", [1, 2, 3, 4, 5])
    if st.button("Submit Feedback"):
        st.write("Thank you for your feedback!")
        print(f"Feedback: {feedback_text}, Rating: {rating}")
