# YoutubeDownloader

Command line utility to download YouTube videos.

## How to use:

Usage: python -m ytDownload [video | audio] "[link]"

**IMPORTANT NOTE:** Playlists have to be public to be downloaded, PyTube doesn't handle private playlists. 

## Dependencies

PyTube
ffmpeg-python
tkinter.filedialog

## TODO

- Video tag
- Catch errors. Invalid link, other OS errors
    - Playlists must be public. Warn user
    - Pytube two different type of playlist links