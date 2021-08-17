import spotipy
from spotipy.oauth2 import SpotifyOAuth


def add_top_songs():
    """Check if top songs are saved, and adds non-saved songs to a playlist for review."""
    scope = "user-top-read user-library-read playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    top_tracks = []
    review_tracks = []
    not_saved = []

    # Get top songs
    results = sp.current_user_top_tracks(limit=50, offset=0, time_range='short_term')
    for item in results['items']:
        top_tracks.append(item['uri'])

    # Get songs in review playlist
    results = sp.playlist_tracks("https://open.spotify.com/playlist/6YCqhbHvopQBA6XxyNSSIf?si=e0118e63e546474c")
    for item in results['items']:
        review_tracks.append(item['track']['uri'])

    # Check if top songs are saved
    results = sp.current_user_saved_tracks_contains(top_tracks)
    for i, track in enumerate(top_tracks):

        # If song not saved and song not in review playlist, add to review playlist
        if not results[i] and track not in review_tracks:
            not_saved.append(track)

    # If there are songs to be added to the review playlist, add them
    if len(not_saved) > 0:
        sp.playlist_add_items("https://open.spotify.com/playlist/6YCqhbHvopQBA6XxyNSSIf?si=e0118e63e546474c", not_saved)


if __name__ == '__main__':
    add_top_songs()
