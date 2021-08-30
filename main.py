import tweepy

consumer_key = input("Consumer Key")
consumer_secret = input("Secret Key")
access_token = input("Access Token")
access_token_secret = input("Access Secret")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)