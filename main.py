from auth.auth import get_spotify_client
from mood.mood_analysis import retry_analyze_mood
from spotify.spotify_client import fetch_top_tracks, create_playlist, add_tracks_to_playlist

sp = get_spotify_client()

user_text = input("How are you feeling? Sad, Happy or Hyped: ")

mood = retry_analyze_mood(user_text)

print(f"Analyzed Mood: {mood}")  

if 'happy' in mood.lower():
    results = sp.search(q='genre:pop', type='track', limit=10)
elif 'sad' in mood.lower():
    results = sp.search(q='genre:acoustic', type='track', limit=10)
elif 'hyped' in mood.lower():
    results = sp.search(q='genre:hip-hop', type='track', limit=10)
else:
    print("Mood not recognized. Please enter Sad, Happy or Hyped.")
    results = {"tracks": {"items": []}}

print(f"Search Results: {results}")

# Extract track URIs
tracks = [track['uri'] for track in results['tracks']['items']]
if tracks:
    playlist_id = create_playlist('Mood Playlist')
    add_tracks_to_playlist(playlist_id, tracks)
    print(f"Created playlist with ID: {playlist_id} and added {len(tracks)} tracks.")
else:
    print("No tracks found for the specified mood.")
