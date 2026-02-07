import yt_dlp

def gen_opts(output_path='./downloads', include_thumbnail=True):
  ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': f'{output_path}/%(title)s - %(artist)s.%(ext)s',
    'js_runtimes': {
        'deno': {
            'path': '/usr/bin/deno'
        }
    },
    'remote_components': ['ejs:github'],
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0',
        },
        {
            'key': 'EmbedThumbnail', # adds album art to the file
        },
        {
            'key': 'FFmpegMetadata',
            'add_metadata': True,
        },
    ],
    'ignoreerrors': True,
    
    # 'quiet': True,
    'extract_flat': True,
  }

  if include_thumbnail:
    ydl_opts['writethumbnail'] = True  # Required for EmbedThumbnail
  

  return ydl_opts

def get_playlist_info(url):
  ydl_opts = gen_opts("./downloads", include_thumbnail=False)
  
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    playlist_info = ydl.extract_info(url, download=False)
    return playlist_info.get('entries', [])

def filter_playlist(playlist_entries, songs):
  missing = []
  
  for entry in playlist_entries:
    song_url = entry.get('url')
    song_name = entry.get('title')
    song_id = entry.get('id')

    if song_id in songs:
      continue
        
    print(f"Missing: {song_name}")
    missing.append(song_url)
  
  return missing

def download_songs(songs, path):
  ydl_opts = gen_opts(path)

  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(songs)