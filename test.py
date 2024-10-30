import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="your own client id",
    client_secret="your own client secret",
    redirect_uri="http://localhost:8888/callback",
    scope="user-read-playback-state user-read-currently-playing"
    
))

# Attempt to fetch the current playback as a test
current_playback = sp.current_playback()
print(current_playback)