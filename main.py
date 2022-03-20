import tweepy
import config
import urllib.request

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

api = tweepy.API(auth)

vidToGet = input("Enter tweet ID:")
tweet = api.get_status(vidToGet, tweet_mode="extended")
vidCheck = ''
bitrate = 0
url = ''
for tweetType in tweet.extended_entities['media']:
    vidCheck = tweetType['type']
if vidCheck == "video":
    for vid in tweet.extended_entities['media']:
        vidin = vid.get('video_info')
        for i in vidin.get('variants'):
            if i.get('content_type') == 'video/mp4':
                if i.get('bitrate') > bitrate:
                    bitrate = i.get('bitrate')
                    url = i.get('url')

else:
    print("Tweet does not contain a video.")

fn = input("Save filename as: ") + '.mp4'
urllib.request.urlretrieve(url, fn) 
