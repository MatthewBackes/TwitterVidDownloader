import tweepy
import config
import urllib.request
import tkinter as tk

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

api = tweepy.API(auth)

class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.ID = 0
        self.header = tk.Label(
        text="Enter Tweet ID:",
        fg="white",
        bg = "black",
        width=20,
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

app = GUI()
app.mainloop()
vidToGet = app.retID()
tweet = api.get_status(vidToGet, tweet_mode="extended")
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
    fn = input("Save filename as: ") + '.mp4'
    urllib.request.urlretrieve(url, fn) 

else:
    print("Tweet does not contain a video.")