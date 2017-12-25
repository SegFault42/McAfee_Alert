#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
from bittrex.bittrex import Bittrex, API_V1_1
from datetime import datetime
import requests
import sys
import tweepy
import time
import subprocess
import json
from pprint import pprint

#twitter
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
# bittrex parameters
my_api_key = ""
my_api_secret = ""
bittrex_api_version = API_V1_1

bittrex_token = Bittrex(my_api_key, my_api_secret, api_version=bittrex_api_version)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

this_path = os.path.abspath(os.path.dirname(sys.argv[0]))
logfiles_location = os.path.join(this_path, "logfiles/")
logfile = None

def logger(msg):
    logfile.write(msg + '\n')
    print(msg)

def getCryptos(token):
    currencies = token.get_currencies()
#   response format
#    {'success': True,
#     'message': '',
#     'result': [{'TxFee': 1.0
#                 'CurrencyLong': Enigma
#                 'CoinType': ETH_CONTRACT
#                 'Currency': ENG
#                 'MinConfirmation': 36
#                 'BaseAddress': 0xfbb1b73c4f0bda4f67dca266ce6ef42f520fbb98
#                 'IsActive': True}, ...]
#    }
    if currencies['success'] != True:# or currencies['result'] is None:
        logger("FATAL ERROR : " + currencies['message'])
        return (None)
    return (currencies['result'])

def getCoinOfTheDay(tweet, cryptos):
    if "Coin of the day" in tweet:
        words = tweet.split(' ')
        for word in words:
            for crypto in cryptos:
                if word.lower() == crypto['Currency'].lower() or word.upper() == crypto['CurrencyLong'].upper():
                    return (crypto)
    return (None)

if __name__ == '__main__':
    global logfile_name
    if not os.path.isdir(logfiles_location):
        os.mkdir(logfiles_location)
    lastTweet = api.user_timeline(screen_name = '@officialmcafee', count = 1, include_rts = False)[0].text.encode('utf-8')
    print ("Starting program ! Current last tweet is " + lastTweet + ", waiting for new one")
    while True:
        tweet = api.user_timeline(screen_name = '@officialmcafee', count = 1, include_rts = False)[0].text.encode('utf-8')
        #tweet = "Coin of the day: burst"
        if tweet != lastTweet:
            lastTweet = tweet
            logfile_name = os.path.join(logfiles_location, "LOG_" + str(datetime.now()) + ".txt")
            logfile = open(logfile_name, 'wb')
            logger("Holy shit new tweet from god McAfee !!!11!1!")
            logger(" It says : " + str(tweet))
            if "coin of the day" in tweet.lower():
                logger("OMFG It's actually about a new coin of the day !!111!! TIME TO GET RICH AF $$$")
                coin = getCryptos(bittrex_token)
               	coin = getCoinOfTheDay(tweet, coin)
                subprocess.call(["python2", "pump/pumpdump.py", "-o", "-b", "5", "-s", "40", "-c", coin['Currency']])
                logger("Done")
            else:
                logger("God McAfee isn't talking about shiny e-shekels :'(")
            logfile.close()
        time.sleep(1)
