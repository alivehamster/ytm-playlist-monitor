import os
import json
import time
import schedule
from libs.ytdlp import filter_playlist, download_songs

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

def update_downloads():
  for url, path in playlists.items():
    songs = {}
    if os.path.exists(path):
        files = os.listdir(path)
        for file in files:
            songs[os.path.splitext(file)[0]] = None
    else:
        os.makedirs(path, exist_ok=True)
    to_download = filter_playlist(url, songs)

    print(f"Downloading {len(to_download)} new songs to {path}...")
    download_songs(to_download, path)


if(playlists):
  update_downloads() 

  schedule.every(interval).minutes.do(update_downloads)

  while True:
    schedule.run_pending()
    time.sleep(60)
else:
  print("No playlists found in environment variable 'Playlists'")

