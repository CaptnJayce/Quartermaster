import spotipy
import spotipy.util
import spotify_id
from spotipy.oauth2 import SpotifyOAuth
from spotify_id import playlist_uri

# Spotify credentials should be defined in spotify_id.py
# spotify_id.py contains:
# SPOTIFY_CLIENT_ID = "your-client-id"
# SPOTIFY_CLIENT_SECRET = "your-client-secret"
# SPOTIFY_REDIRECT_URI = "your-redirect-uri"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=spotify_id.SPOTIFY_CLIENT_ID,
    client_secret=spotify_id.SPOTIFY_CLIENT_SECRET,
    redirect_uri=spotify_id.SPOTIFY_REDIRECT_URI,
    scope="user-library-read user-read-playback-state user-modify-playback-state user-library-modify user-read-currently-playing"
))

# Get User's device
def get_device_id():
    devices = sp.devices()
    if not devices['devices']:
        print("No devices found")
        return None
    return devices['devices'][0]['id']

# Rewind song
def rewind_song():
    device_id = get_device_id()
    if device_id:
        sp.previous_track(device_id=device_id)

# Skip song
def skip_song():
    device_id = get_device_id()
    if device_id:
        sp.next_track(device_id=device_id)

# Pause song
def pause_song():
    device_id = get_device_id()
    if device_id:
        sp.pause_playback(device_id=device_id)

# Resume song
def resume_song():
    device_id = get_device_id()
    if device_id:
        current_playback = sp.current_playback()
        if current_playback and current_playback['is_playing']:
            sp.pause_playback(device_id=device_id)
        sp.start_playback(device_id=device_id)

# Like currently playing song
def like_song():
    device_id = get_device_id()
    if device_id:
        current_playback = sp.current_playback()
        if current_playback and current_playback['is_playing']:
            track_id = current_playback["item"]["id"]
            sp.current_user_saved_tracks_add([track_id])