from pytube import YouTube
from pytube import Playlist
from tkinter.filedialog import askdirectory
from main import YouTubeDownloader
import os


"""
Receives tkinter window, link (string), file format to download (string), 
resolution (string), and a boolean to see if a playlist should be downloaded.
Returns a boolean with the download status code. True if download was succesfull.
"""
def download(window, link, format, resolution, whole_list):
    directory = askdirectory(title = "Select folder")
    
    if whole_list == True:
        p = Playlist(link)
        
        # If the playlist is empty, return False code
        if len(p.video_urls) == 0:
            return False

        for video in p.video_urls:
            getVideo(window, video, format, resolution, directory)

    else:
        #link = formatLink(link) #Remove playlist info from url
        getVideo(window, link, format, resolution, directory)

    return True


def getVideo(window, link, format, resolution, directory):
    yt = YouTube(link)
    
    # Assign download type to stream object
    if format == "MP4" or format == "WVM":
        stream = yt.streams.get_highest_resolution();
    else:
        stream = yt.streams.get_audio_only()

    window.downloaded_text.insert(1.0, f"Now downloading {(yt.title if len(yt.title) < 30 else yt.title[0:30])}...") # Update current video
    window.update()
    stream.download(directory) # Download video with pytube


def formatLink(link):
    position = link.find('&')
    return link[0:position]