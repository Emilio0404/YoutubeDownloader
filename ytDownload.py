import sys
import os
from pytube import YouTube
from pytube import Playlist
from tkinter.filedialog import askdirectory
from tempfile import TemporaryDirectory
from re import sub
import ffmpeg


RESOLUTIONS = ['2160p', '1440p', '1080p', '720p', '480p', '360p', '240p', '144p']


def main(downloadFormat, link):

    # Get directory to save videos
    print('Choose a folder to download link')
    directory = askdirectory(title="Select folder")

    # Check if link is a video or a playlist
    whole_list = False

    # If the link is from a playlist, ask wether to download it all or not
    if 'list' in link:
        whole_list = ask_for_whole_playlist()

    # Download videos
    if whole_list:
        playlist = Playlist(link)
        for pLink in playlist.video_urls:
            download(pLink, downloadFormat, directory)
    else:
        # If true, video was from a playlist so we remove that data
        if link.find('&') != -1:
            link = link[0:link.find('&')]
        download(link, downloadFormat, directory)
    
    print('Files downloaded succesfully. Have a good day!')

    
def download(link, downloadFormat, directory):
    """ Handles download logic for both video and audio parts of the received link """
    """ Joins them if download format is a video, converts to mp3 if it is audio """

    yt = YouTube(link)
    print(f'Now downloading {yt.title}')

    # Create temporary directory to save temp files
    temp_dir = TemporaryDirectory()

    # Download audio data and get its path
    audioDirectory = download_audio(yt.streams, temp_dir.name)

    # Clean up output name of downloaded video
    outputName = safe_filename(yt.title)
    
    if downloadFormat == 'video':

        # Download video data and get its path
        videoDirectory = download_video(yt.streams, temp_dir.name)

        # Create download path for mp4
        outputPath = os.path.join(directory, outputName + '.mp4')
        outputPath = os.path.normpath(outputPath)

        # Join audio and video files
        try:
            ffmpegVideoStream = ffmpeg.input(audioDirectory)
            ffmpegAudioStream = ffmpeg.input(videoDirectory)
            ffmpeg.output(ffmpegAudioStream, ffmpegVideoStream, outputPath, loglevel="quiet").run()
        except (ffmpeg.Error, OSError) as E:
            print('UNABLE TO DOWNLOAD VIDEO ' + outputName)
            print(E)

        # Delete temporary video files
        os.remove(videoDirectory)

    else:
        # Create download path for mp3
        outputPath = os.path.join(directory, outputName + '.mp3')
        outputPath = os.path.normpath(outputPath)

        # Convert to mp3
        try:
            ffmpegAudioStream = ffmpeg.input(audioDirectory)
            ffmpeg.output(ffmpegAudioStream, outputPath, loglevel="quiet").run()
        except (ffmpeg.Error, OSError) as E:
            print('UNABLE TO DOWNLOAD VIDEO ' + outputName)
            print(E)

    # Remove temporary files
    os.remove(audioDirectory)
    temp_dir.cleanup()


def download_audio(yt_streams, tmp_dir):
    """Downloads audio part of the YT video and returns the path where it was downloaded"""
    
    # Declare file name so we can delete it later with that name
    audioFileName = 'yt_download_tmp_audio'

    # Get audio stream
    audioStream = yt_streams.get_audio_only()
    audioStream.download(output_path=tmp_dir, filename=audioFileName)

    # Get directory of temporary audio file
    return os.path.join(tmp_dir, audioFileName)


def download_video(yt_streams, tmp_dir):
    """Downloads video part of the YT video and returns the path where it was downloaded"""

    # Declare file name so we can delete it later with that name
    videoFileName = 'yt_download_tmp_video'

    # Get video stream and download it
    videoStream = yt_streams.get_by_itag(get_video_tag(yt_streams))
    videoStream.download(output_path=tmp_dir, filename=videoFileName)

    # Get directory of temporary video file
    return os.path.join(tmp_dir, videoFileName)


def get_video_tag(video_streams):
    """ Get highest resolution tag of a video stream """

    stream_tag = -1
    res_index = 0
    found_tag = False

    while not found_tag:
        available_streams = video_streams.filter(adaptive=True, file_extension='mp4', resolution=RESOLUTIONS[res_index], only_video=True)
        
        # No streams were found with set parameters. Select a tag manually
        if len(available_streams) > 8:
            print('\nCould not find a valid tag. Please type in a tag from the list.')
            for stream in available_streams:
                print(stream)
            stream_tag = int(input('Tag: '))

        # No stream was found with current resolution.
        elif len(available_streams) == 0:
            res_index += 1

        # A stream was found. Break loop
        else:
            stream_tag = available_streams[0].itag
            found_tag = True

    return stream_tag


def safe_filename(name):
    """ Returns a safe filename to store in PC"""

    return sub(r'[\\/*?:"<>|]',"", name)


def ask_for_whole_playlist():
    """Ask whether to download whole playlist or not if video link is a playlist"""

    answer = ''
    while answer != 'y' and answer != 'n':
        answer = input('This link is from a playlist. Do you want to download the whole playlist? (Y/N) ')[0].lower()
        if answer == 'y':
            return True
        elif answer =='n':
            return False
        else:
            print('I dare you to give me a valid answer!')


if __name__ == '__main__':

    # Ensure file format and link has been provided
    if len(sys.argv) != 3:
        print('ERROR. Usage: python -m ytDownload [video | audio] "[link]"')
        sys.exit()

    # Ensure format is audio or video
    elif sys.argv[1] != 'audio' and sys.argv[1] != 'video':
        print('ERROR. Usage: python -m ytDownload [video | audio] "[link]"')
        sys.exit()

    # Ensure the link provided is valid

    main(sys.argv[1], sys.argv[2])