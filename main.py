import os
import json
import time
import schedule
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import re
from libs.ytdlp import get_playlist_info, filter_playlist, download_songs

interval = int(os.environ.get('Interval') or 1440)  # in minutes

def parse_playlists(playlists_str):
    if not playlists_str:
        return {}
    
    try:
        return json.loads(playlists_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing playlists JSON: {e}")
        return {}
  
playlists = parse_playlists(os.environ.get('Playlists'))
playlist_states = {}

def update_downloads():
  for url, path in playlists.items():
    playlist_entries = get_playlist_info(url)
    current_ids = set(entry.get('id') for entry in playlist_entries if entry.get('id'))
    
    # Check if playlist has changed
    if url in playlist_states and playlist_states[url] == current_ids:
      print(f"No changes detected in playlist {url}")
      continue
    
    # Update stored state
    playlist_states[url] = current_ids
    
    # Read existing songs from files
    songs = {}
    if os.path.exists(path):
      files = os.listdir(path)
      for file in files:
        if file.endswith('.mp3'):
          filepath = os.path.join(path, file)
          try:
            audio = MP3(filepath, ID3=ID3)
            # Get URL from purl
            if audio.tags:
              for tag in audio.tags.values():
                if hasattr(tag, 'desc') and tag.desc == 'purl':
                  purl = str(tag.text[0]) if tag.text else None
                  break
            
            if purl:
              # Extract video ID from URL (after ?v=)
              match = re.search(r'[?&]v=([^&]+)', purl)
              if match:
                id = match.group(1)
                songs[id] = None
          except Exception as e:
            print(f"Error reading metadata from {file}: {e}")
    else:
      os.makedirs(path, exist_ok=True)

    to_download = filter_playlist(playlist_entries, songs)
    print(f"Downloading {len(to_download)} new songs to {path}...")
    download_songs(to_download, path)


if(playlists):
  update_downloads() 

  schedule.every(2).minutes.do(update_downloads)

  while True:
    schedule.run_pending()
    time.sleep(60)
else:
  print("No playlists found in environment variable 'Playlists'")

