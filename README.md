# What is this
Every 24 hours this will scan your youtube music playlists and download any music that has been added

# How do I install
```
# pull the image from github container repository

docker pull ghcr.io/alivehamster/ytm-playlist-monitor:main

# start the image with the config in the Playlist env variable
docker run -e Playlists='config' -v /path/on/host:/path/in/container ghcr.io/alivehamster/ytm-playlist-monitor:main
```

### What's goes in the config section:
```
{
  "Youtube_Playlist_URL": "directory_inside_container",
  "Youtube_Playlist_URL": "directory_inside_container"
  // As many playlists as you want
}
```