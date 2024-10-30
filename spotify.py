import spotipy
import logging
import time
import threading
import pwnagotchi.plugins as plugins
import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
from spotipy.oauth2 import SpotifyOAuth

class Song(plugins.Plugin):
    __author__ = 'Roli0810'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'Displays the current song and artist from Spotify'

    def on_loaded(self):
        logging.info("Spotify plugin loaded.")
        self.last_update = 0  # Track the last update time
        # Initialize Spotify client
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id="your own client id",
            client_secret="your own client secret",
            redirect_uri="http://localhost:8887/callback",
            cache_path="/usr/local/share/pwnagotchi/custom-plugins/.cache",
            scope="user-read-playback-state user-read-currently-playing"
        ))

        # Start the thread to update song information
        self.update_thread = threading.Thread(target=self.update_song_info)
        self.update_thread.daemon = True  # This will ensure the thread will exit when the main program does
        self.update_thread.start()

    def on_ui_setup(self, ui):
        # Position the text based on your screen type or set custom position
        ui.add_element(
            'song_playing',
            LabeledValue(
                color=BLACK,
                label='Song:',
                value='Loading...',
                position=(10, 80),  # Adjust x, y for your screen layout
                label_font=fonts.Small,
                text_font=fonts.Small,
            )
        )
        ui.add_element(
            'artist_playing',
            LabeledValue(
                color=BLACK,
                label='Artist:',
                value='Loading...',
                position=(10, 90),  # Adjust y position to avoid overlap
                label_font=fonts.Small,
                text_font=fonts.Small,
            )
        )

    def update_song_info(self):
        while True:
            current_time = time.time()
            # Fetch current Spotify song from Spotify API
            try:
                current_playback = self.sp.current_playback()
                if current_playback and current_playback.get('is_playing'):
                    track = current_playback['item']
                    song_name = track['name']
                    artist_name = track['artists'][0]['name']
                    # Update the UI elements with the song and artist info
                    self.set_ui(song_name, artist_name)
                else:
                    # No song is currently playing
                    self.set_ui("No song playing", "")
            except Exception as e:
                logging.error(f"Error fetching Spotify playback: {e}")

            time.sleep(10)  # Sleep for 10 seconds

    def set_ui(self, song_name, artist_name):
        # Method to safely update the UI from the thread
        # Assuming 'ui' is accessible globally or pass it appropriately
        if hasattr(self, 'ui'):
            self.ui.set('song_playing', song_name)
            self.ui.set('artist_playing', artist_name)

    def on_ui_update(self, ui):
        # Store the ui reference for updating in the thread
        self.ui = ui
