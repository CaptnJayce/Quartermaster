import spotipy
import spotipy.util
from spotipy.oauth2 import SpotifyOAuth
import spotify_id

# Spotify credentials should be defined in spotify_id.py
# spotify_id.py contains:
# SPOTIFY_CLIENT_ID = "your-client-id"
# SPOTIFY_CLIENT_SECRET = "your-client-secret"
# SPOTIFY_REDIRECT_URI = "your-redirect-uri"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=spotify_id.SPOTIFY_CLIENT_ID,
    client_secret=spotify_id.SPOTIFY_CLIENT_SECRET,
    redirect_uri=spotify_id.SPOTIFY_REDIRECT_URI,
    scope="user-library-read user-read-playback-state user-modify-playback-state"
))

# Get User's device
devices = sp.devices()
if not devices['devices']:
    print("No devices found")
    exit()

device_id = devices['devices'][0]['id']

# Rewind song
def rewind_song():
    sp.previous_track(device_id=device_id)

# Skip song
def skip_song():
    sp.next_track(device_id=device_id)

# Pause song
def pause_song():
    sp.pause_playback(device_id=device_id)

# Resume song
def resume_song():
    current_playback = sp.current_playback()
    
    # This check prevents a crash when playing my playlist with already active playback
    # I have no idea why.
    if current_playback and current_playback['is_playing']:
        sp.pause_playback(device_id=device_id)
    sp.start_playback(device_id=device_id)

# Play playlist
def play_playlist(playlist_uri, device_id=None):
    sp.start_playback(device_id=device_id, context_uri=playlist_uri)