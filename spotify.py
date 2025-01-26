import spotipy
import spotipy.util as util
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