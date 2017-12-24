import requests
import sys
import tweepy
import sys

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
#twitter_account_sender = "" #without @
#twitter_account_receiver = "" # without @

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def tweet_current_value(tweet):
    try:
        api.update_status(status=tweet)
    except:
        pass

def main():
    #tweet_current_value("Hello world")
    stuff = api.user_timeline(screen_name = '@officialmcafee', count = 1, include_rts = True)
    for status in stuff:
        print(status.text)

if __name__ == '__main__':
    main()
