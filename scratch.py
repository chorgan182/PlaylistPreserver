# -*- coding: utf-8 -*-
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# set ids and secrets
os.environ["SPOTIPY_CLIENT_ID"] = "490a0db12cc04207bdc1719f40132717"
os.environ["SPOTIPY_CLIENT_SECRET"] = "21466d35e131432dbe3214377696d04e"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://127.0.0.1:9090"

### come back to this, investigate scopes
scope = "user-modify-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# test connection - it works!!!
results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])

# more testing
sp.current_user()


