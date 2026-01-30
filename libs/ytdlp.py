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
            'key': 'FFmpegMetadata', # adds title/artist tags
        }
    ],
    
    # 'quiet': True,
    # 'extract_flat': True,
  }

  if include_thumbnail:
    ydl_opts['writethumbnail'] = True  # Required for EmbedThumbnail
  

  return ydl_opts

def filter_playlist(url, songs):
  ydl_opts = gen_opts("./downloads", include_thumbnail=False)
  missing = []

  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    playlist_info = ydl.extract_info(url, download=False)
    if 'entries' in playlist_info:
      for entry in playlist_info['entries']:
        song_url = entry.get('original_url')
        song_name = entry.get('title')
        song_artist = entry.get('artist')

        name = f"{song_name} - {song_artist}"
        sanitized_name = yt_dlp.utils.sanitize_filename(name, restricted=False)

        if sanitized_name in songs:
          continue
            
        print(f"Missing: {sanitized_name}")
        missing.append(song_url)
      
  return missing

def download_songs(songs, path):
  ydl_opts = gen_opts(path)

  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(songs)