from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox, scrolledtext
import download_methods
import sys


class YouTubeDownloader: 

    def __init__(self, window):
        # Create window
        self.window = window
        window.geometry("500x400")
        window.title("YouTube Downloader")
        window.resizable(False, False)


        # Variables
        self.ytlink = StringVar(window)
        self.resolution = StringVar(window)
        self.fileFormat = StringVar(window)
        fileOptions = ("MP4", "WVM", "MP3", "WAV")
        qualityOptions = ("720p", "1080p")


        # Input_link label and entry
        url_label = Label(window, text="Link")
        url_label.grid(row = 0, column = 0, sticky = "e", padx = 10, pady = 10)
        self.url_entry = Entry(width = 60, textvariable = self.ytlink)
        self.url_entry.grid(row = 0, column = 1)


        # Create download_type label and menu
        downloadTypeLabel = Label(window, text = "Download Type")
        downloadTypeLabel.grid(row = 1, column = 0, sticky = "e", padx = 10, pady = 10)

        self.downloadTypeMenuButton = Menubutton(text = "Select download type")
        self.downloadTypeMenu = Menu(self.downloadTypeMenuButton, tearoff = False)
        self.downloadTypeMenuButton.config(menu = self.downloadTypeMenu)
        self.downloadTypeMenuButton.grid(row = 1, column = 1, sticky = "w")

        # Add options to the menu. Assigned callback to uptade text when option is selected
        for fileType in fileOptions:
            self.downloadTypeMenu.add_radiobutton(label = fileType, variable = self.fileFormat, value = fileType, command = self.update_menu_text)


        # Create quality label and menu
        qualityLabel = Label(window, text = "Quality")
        qualityLabel.grid(row = 2, column = 0, sticky = "e", padx = 10, pady = 10)

        self.qualityMenuButton = Menubutton(text = "Select quality")
        self.qualityMenu = Menu(self.qualityMenuButton, tearoff = False)
        self.qualityMenuButton.config(menu = self.qualityMenu)
        self.qualityMenuButton.grid(row = 2, column = 1, sticky = "w")

        # Add options to the menu. Assigned callback to uptade text when option is selected
        for quality in qualityOptions:
            self.qualityMenu.add_radiobutton(label = quality, variable = self.resolution, value = quality, command = self.update_menu_text)
        

        # Create download button. Assigned callback function download_content for when the button is clicked
        self.download_button = Button(window, text="Download Video", command = self.download_content)
        self.download_button.grid(row = 4, column = 1, sticky = "w", pady = 10)


        # Create text box to print information to the user
        self.window.downloaded_text = scrolledtext.ScrolledText(width = 55, height = 10)
        self.window.downloaded_text.grid(column = 0, row = 5, sticky = "e", padx = 20, columnspan = 2)
        

    def download_content(self):
        answer = False
        status = False
        self.window.downloaded_text.delete(1.0, END) # Clear printed text

        # If the video is from a playlist, ask if user wants to download whole playlist or just video
        if 'list' in self.ytlink.get():
            answer = messagebox.askyesnocancel(title="Download whole playlist", message="This link is from a YouTube playlist, do you want to download it all?")

        # If user didn't select cancel, download link input.
        # download method returns a boolean with the completion status of the downloads
        if answer is not None:
            status = download_methods.download(self.window, self.ytlink.get(), self.fileFormat.get(), self.resolution.get(), answer)

        if status == True:
            self.window.downloaded_text.insert("1.0", "Your videos are now downloaded")
        else:
            self.window.downloaded_text.insert("1.0", "Unable to download files correctly")


    def update_menu_text(self):
        if len(self.fileFormat.get()) != 0:
            self.downloadTypeMenuButton.config(text = self.fileFormat.get())

        if len(self.resolution.get()) != 0:
            self.qualityMenuButton.config(text = self.resolution.get())


if __name__ == "__main__":
    root = Tk()
    yt_gui = YouTubeDownloader(root)
    root.mainloop()