import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotify_id

# declare variables in spotify_id.py 
# client_id=""
# client_secret=""
# redirect_uri=""
# scope=""

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(spotify_id.client_id, spotify_id.client_secret, spotify_id.redirect_uri, spotify_id.scope))

# uri for Denzel Curry
test_url = 'spotify:artist:6fxyWrfmjcbj5d12gXeiNV'

results = sp.artist_albums(test_url, album_type='album')
albums = results['items']
while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])
    
