import sys
import os
from pytube import YouTube
from pytube import Playlist
from tkinter.filedialog import askdirectory
sys.path.insert(0, 'C:\Python39\Lib\site-packages\ffmpeg')
import ffmpeg

failedRenames = 0


def main(downloadFormat, link):

    # Get directory to save videos
    print('Choose a folder to download link')
    directory = askdirectory(title = "Select folder")
    if directory == os.getcwd():
        print('Please input a valid directory.')
        return

    # Check if link is a video or a playlist and handle both cases
    whole_list = False
    if 'list' in link:
        answer = input('This link is from a playlist. Do you want to download the whole playlist? Y/N ')[0].lower()
        if answer == 'y':
            if link.find('&') == -1:
                print('If you don\'t want to download the whole playlist, please give me a valid video link!')
                return
            whole_list = True
        elif answer == 'n':
            link = link[0:link.find('&')]
        else:
            print('I couldn\'t understand you.')
            return

    if whole_list:
        playlist = Playlist(link)
        for pLink in playlist.video_urls:
            download(pLink, downloadFormat, directory)

    else:
        download(link, downloadFormat, directory)

    
def download(link, downloadFormat, directory):

    yt = YouTube(link)
    print(f'Now downloading {yt.title}')

    # Declare file name so we can delete it later with that name
    audioFileName = 'ytDownload_tempAudio'

    # Get audio stream
    audioStream = yt.streams.get_audio_only()
    audioStream.download(output_path=directory, filename=audioFileName)

    # Get the directory of the new tempprary downloaded audio file
    audioDirectory = os.path.join(directory, audioFileName)

    if downloadFormat == 'video':

        # Declare file name so we can delete it later with that name
        videoFileName = 'ytDownload_videoAudio'

        # Get video stream and download it
        videoStream = yt.streams.get_by_itag(get_video_tag(yt))
        videoStream.download(output_path=directory, filename=videoFileName)

        # Get directory of video file
        videoDirectory = os.path.join(directory, videoFileName)

        # Join audio and video files
        ffmpegVideoStream = ffmpeg.input(audioDirectory)
        ffmpegAudioStream = ffmpeg.input(videoDirectory)
        ffmpeg.output(ffmpegAudioStream, ffmpegVideoStream, 'out.mp4').run()

        # Delete individual video file
        os.remove(videoDirectory)

    else:
        # Convert to mp3
        ffmpegAudioStream = ffmpeg.input(audioDirectory)
        outputName = os.path.normpath(os.path.join(directory, 'ytdwnldoutput.mp3'))
        ffmpeg.output(ffmpegAudioStream, outputName).run(capture_stderr=True)

        try:
            os.rename(outputName, os.path.join(directory, f'{yt.title}.mp3'))
        except OSError:
            global failedRenames
            print(f'This video\'s title is not permitted as a filename. Named as: invalidNameAudio{str(failedRenames)}.mp3')
            os.rename(outputName, os.path.join(directory, f'invalidNameAudio{str(failedRenames)}.mp3'))
            failedRenames += 1

    # Remove old audio files
    os.remove(audioDirectory)
    
    print('Files downloaded succesfully. Have a good day!')


def get_video_tag(videoObject):
    """ Get highest resolution tag of a video stream """

    """
    while not found:
        for stream in videoObject.streams.filter():

            
                streamTag = stream.itag
                found = True
                break
    """

    return streamTag


if __name__ == '__main__':

    """
    print(yt.streams.filter(fps=30, res="1080p", mime_type="video/mp4"))
    """

    if len(sys.argv) != 3:
        print('ERROR. Usage: python -m ytDownload [video | audio] [link]')
        sys.exit()
    elif sys.argv[1] != 'audio' and sys.argv[1] != 'video':
        print('ERROR. Usage: python -m ytDownload [video | audio] [link]')
        sys.exit()
    #elif check valid link

    main(sys.argv[1], sys.argv[2])


# Get directory

# If it is a list
    # Ask for list of only video
    # If only video
        #create yt  object 
    # If playlist
        #create playlist object
        #for loop in all links of that playlist object

# Create yt object
# Get stream with highest audio resolution

# If it is a video
    # get highest video resolution
    # Download both stream parts
    # join both parts
# If it is an audio
    # Download stream