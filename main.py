#!/usr/bin/env python
# -*- coding: utf8 -*-
import requests
import sys
import tweepy
import sys

consumer_key = "LR3m9NtcR7YsDTc5uaxkAAKrv"
consumer_secret = "LZ4BzhzqJxLzOhhVv5stXo4GaHgfpqCOyYhaV2XvuUdfMipM7B"
access_token = "868192136830885889-2Nlk6pEBKHw6zYSYmr9W1YSZ2JGqrdl"
access_token_secret = "HVDL4CX4NDOFMWr7NxXmSCeFIw02iRtgFAw9R0mpT4Cin"
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
