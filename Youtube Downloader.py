'''

Youtube Downloader using PyTube

IMPORTANT NOTE: To download a playlist it has to be a public.
Private playlists can't be downlaoded.

'''

from pytube import YouTube
from pytube import Playlist
import sys
import os


def main():
    
    print('Welcome to Youtube Downloader.')
    running = True
    
    while running == True:
    
        link = input('Please input a link for me to download:\n').strip()

        # If the link is a playlist, ask to download the playlist or only the video.
        # If not a playlist, just download the video
        
        if 'list' in link:
            print('This link is from a YouTube playlist. Do you want to download the whole playlist?')
            print('1. Only the video\n2. The whole playlist\n3. Exit')
            # Keep running while the input is invalid
            userOption = True
            while userOption == True:
                user = input()
                if user == '1' or user == '2' or user == '3':
                    userOption = False
                else:
                    print('Please insert a valid number.')
            # Runs an option according to the input
            if user == '1':
                link = trimLink(link)
                downloadVideo(link)
            elif user == '2':
                downloadPlaylist(link)
            elif user == '3':
                print('Have a nice day!')
                sys.exit()
        else:
            downloadVideo(link)
        
        # If user does not want to download another video, exit the program
        print("I\'m done! Do you want to download another video? Y/N")
        user = input().lower()
        if user == 'n':
            running = False

    print('Have a nice day!')
    
    
    
# Creates Youtube object from link and calls getStream to download video
def downloadVideo(_link):
    yt = YouTube(_link)
    getStream(yt)
    

# Iterates over Playlist to download all videos
# 'video' contains the Youtube link from the iteration
def downloadPlaylist(_link):
    p = Playlist(_link) # Creates playlist object
    # Checks if the playlist is empty or not.
    if len(p.video_urls) == 0:
        print('This playlist is empty. Check if the playlist you\'re trying to download is public.')
    else:
        for video in p.video_urls:
            downloadVideo(video)


# Gets the highest resolution from a viedo and downloads it in a new folder
def getStream(yt):
    directory = os.path.join(os.getcwd(), 'Video Download')
    print('Now downloading', yt.title)
    stream = yt.streams.get_highest_resolution()
    stream.download(directory)


# Returns a string containing only the characters corresponding to the 
# current video from a Youtube playlist link
def trimLink(_link):
    position = _link.find('&')
    _link = _link[0:position]
    return _link

main()