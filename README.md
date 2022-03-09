# PlaylistPreserver
Personal project to extend Spotify playlist capabilities, with the goal of learning Python, API principles, the Spotify Developer hub, and Streamlit.

## What does it do?

Have you ever...
- been listening to a long playlist and want to continue where you left off the next day, without re-listening to songs?
- clicked on a song recommendation and messed up your 47-hour playlist shuffle, with no recourse to return? 
- been confused about hearing the same song multiple times in that 47-hour playlist, even with shuffle enabled?

This app solves those problems by creating a new playlist with recently played songs removed. Given a time cutoff, you can select a playlist in your account, name the new playlist, and enable/disable a true shuffle.

## Known Issues

- The Spotify Developer hub was recently changed to limit client traffic to 25 _named_ users.
  - Unfortunately, this was discovered later. 
  - If you would like access, please reach out via the button on the landing page of the app _with the email registered with your Spotify account_.
  - You may authenticate any way you like (Facebook, Apple, Google, or username/password), but the email supplied must be the one you used to sign up for Spotify.
- Spotify's API endpoint for "recently played" songs is currently broken.
  - It only returns the 50 most recently played, which defeats the purpose of this app.
  - Documented on the Spotify for Developers Community forum [here](https://community.spotify.com/t5/Spotify-for-Developers/Now-that-users-can-view-their-recently-played-tracks-in-the-apps/m-p/5181981/thread-id/2278) and [here](https://community.spotify.com/t5/Spotify-for-Developers/quot-Current-User-s-Recently-Played-Tracks-quot-before-param-not/td-p/5133179).
- Authentication happens in a new tab.
  - Custom HTML options for hyperlinks are not supported in the version of Streamlit used for Streamlit Cloud.
  - This has already been addressed in a development release, so it should be implemented in Streamlit Cloud soon.
  - More in [merged PR](https://github.com/streamlit/streamlit/pull/4364) here.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/chorgan182/playlistpreserver/qry-param-method/playlist_preserver_app.py)
