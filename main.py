import tweepy
import config
import urllib.request
import tkinter as tk

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

api = tweepy.API(auth)

class GUI(tk.Tk):
    def __init__(self, t):
        tk.Tk.__init__(self)
        self.ID = 0
        self.header = tk.Label(
        text= t,
        fg="white",
        bg = "black",
        width=30,
        height=10)
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
    fail = tk.Label(
        text="Invalid Tweet ID.",
        fg="white",
        bg = "black",
        width=30,
        height=10)
    fail.pack()
    fail.mainloop()
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
    fn = GUI("Save filename as: ")
    fn.mainloop()
    name = fn.retID() + '.mp4'
    urllib.request.urlretrieve(url, name) 

else:
    fail = tk.Label(
        text="Tweet does not have a video.",
        fg="white",
        bg = "black",
        width=30,
        height=10)
    fail.pack()
    fail.mainloop()