import tweepy
import config
import urllib.request
import tkinter as tk
from tkinter.filedialog import asksaveasfilename

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

api = tweepy.API(auth)

def save_as(vid):
    filepath = asksaveasfilename(
        defaultextension=".mp4",
        filetypes=[("Media Files", "*.mp4*")]
    )
    if not filepath:
        return
    urllib.request.urlretrieve(vid, filepath)

class GUI(tk.Tk):
    def __init__(self, t):
        tk.Tk.__init__(self)
        self.ID = 0
        self.title("Twitter Video Downloader")
        self.header = tk.Label(
        text= t,
        fg="white",
        bg = "black",
        width=60,
        height=20)
        self.entry = tk.Entry(self)
        self.button = tk.Button(self, text="Enter", command=self.on_button)
        self.header.pack()
        self.entry.pack()
        self.button.pack()

    def on_button(self):
        self.ID = self.entry.get()
        self.destroy()
    
    def retID(self):
        return self.ID

app = GUI("Enter Tweet ID:")
app.mainloop()
vidToGet = app.retID()
try:
    tweet = api.get_status(vidToGet, tweet_mode="extended")
except:
    failhead = tk.Tk()
    failhead.title("Twitter Video Downloader")
    fail = tk.Label( failhead,
        text="Invalid Tweet ID.",
        fg="white",
        bg = "black",
        width=60,
        height=20)
    fail.pack()
    failhead.mainloop()
    quit()
vidCheck = ''
bitrate = 0
url = ''
try:
    for tweetType in tweet.extended_entities['media']:
        vidCheck = tweetType['type']
except:
    pass
if vidCheck == "video":
    for vid in tweet.extended_entities['media']:
        vidin = vid.get('video_info')
        for i in vidin.get('variants'):
            if i.get('content_type') == 'video/mp4':
                if i.get('bitrate') > bitrate:
                    bitrate = i.get('bitrate')
                    url = i.get('url')
    suchead = tk.Tk()
    suchead.title("Twitter Video Downloader")
    success = tk.Label( suchead,
        text="Select filepath.",
        fg="white",
        bg = "black",
        width=60,
        height=20)
    savebut = tk.Button(suchead, text = "Save as", command =lambda: save_as(url))
    success.pack()
    savebut.pack()
    suchead.mainloop()

else:
    failhead = tk.Tk()
    failhead.title("Twitter Video Downloader")
    fail = tk.Label( failhead,
        text="Tweet does not have a video.",
        fg="white",
        bg = "black",
        width=60,
        height=20)
    fail.pack()
    failhead.mainloop()