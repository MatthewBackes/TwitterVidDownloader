#Author: Matthew Backes
#Simple program to download twitter videos. Requires working twitter link, meta-data in URL is ignored automatically.

import tweepy
import config
import urllib.request
from urllib.parse import urlparse
import tkinter as tk
from tkinter.filedialog import asksaveasfilename

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

api = tweepy.API(auth)
url = ""
#Function that saves the video. Allows for filepath selection.
#'asksaveasfilename' opens directory. urllib actually does the saving.
def save_as(vid):
    filepath = asksaveasfilename(
        defaultextension=".mp4",
        filetypes=[("Media Files", "*.mp4*")]
    )
    if not filepath:
        return
    urllib.request.urlretrieve(vid, filepath)

#GUI class acts as the screen that first appears when running the program.
#Intending to add all screens to this class to simplify code.
class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        #Code for using frames gathered from https://pythonprogramming.net/change-show-new-frame-tkinter/
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for x in (Start, Fail1, Fail2, Success, Done):
            frame = x(container, self)
            self.frames[x] = frame
            frame.grid(row = 0, column = 0, sticky="nsew")
        self.show_frame(Start)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class Start(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.ID = 0
        self.header = tk.Label(self,
            text= "Please enter tweet Link:",
            fg="white",
            bg = "black",
            width=60,
            height=20)
        self.header.pack()
        self.entry = tk.Entry(self)
        self.entry.pack()
        self.button = tk.Button(self, text="Enter", command=lambda: self.check_link(controller))
        self.button.pack()

    def check_link(self, controller):
        self.ID = self.entry.get()
        self.vidToGet = urlparse(self.entry.get()).path.split('/')[-1]
        #Try and except block to catch a fail if user provides something other than a tweet.
        try:
            self.tweet = api.get_status(self.vidToGet, tweet_mode="extended")
            self.vidCheck = ''
            self.bitrate = 0
            global url
            #Another try and except block. Except catches tweets that have no media.
            try:
                for tweetType in self.tweet.extended_entities['media']:
                    self.vidCheck = tweetType['type']
                #If check to make sure the tweet media is actually a video and not a picture, gif, etc.
                if self.vidCheck == "video":
                    for vid in self.tweet.extended_entities['media']:
                        vidin = vid.get('video_info')
                        for i in vidin.get('variants'):
                            if i.get('content_type') == 'video/mp4':
                                if i.get('bitrate') > self.bitrate:
                                    self.bitrate = i.get('bitrate')
                                    url = i.get('url')
                controller.show_frame(Success)
            except:
                controller.show_frame(Fail2)
        except:
            controller.show_frame(Fail1)  

class Fail1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        fail = tk.Label( self,
            text="Link is not a tweet.",
            fg="white",
            bg = "black",
            width=60,
            height=20)
        fail.pack()
        self.button = tk.Button(self, text="Retry", command=lambda: controller.show_frame(Start))
        self.button.pack()

class Fail2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        fail = tk.Label( self,
            text="Tweet does not have a video.",
            fg="white",
            bg = "black",
            width=60,
            height=20)
        fail.pack()
        self.button = tk.Button(self, text="Retry", command=lambda: controller.show_frame(Start))
        self.button.pack()

class Success(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        success = tk.Label( self,
            text="Select filepath.",
            fg="white",
            bg = "black",
            width=60,
            height=20)
        success.pack()
        savebut = tk.Button(self, text = "Save as", command =lambda: [save_as(url), controller.show_frame(Done)])
        savebut.pack()

class Done(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        done = tk.Label( self,
            text="File successfully downloaded.",
            fg="white",
            bg = "black",
            width=60,
            height=20)
        done.pack()

app = GUI()
app.mainloop()

