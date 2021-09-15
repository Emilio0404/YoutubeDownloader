from pytube import YouTube

yt = YouTube('https://www.youtube.com/watch?v=QJq3r1ceR64')
print(yt.title)
print(yt.streams)

#https://www.youtube.com/watch?v=QJq3r1ceR64&list=PLcWZElfOFTrbsO2yLpX8t0hSERSUSg-jd&index=3
#messagebox.showwarning(title="Invalid YT Playlist", message="Please input a valid link")
#img = PhotoImage(file = r"C:\\Users\\emili\\Desktop\\Projects\\Coding Projects\\Yotube Downloader\\YoutubeDownloader\\res\\sddefault.png)
#img1 = img.subsample(2,2)
#Label(window, image = img1).grid(row = 5, column = 1)