# -*- coding: utf8 -*-

import parseJson
import tweepy
import json
from bittrex.bittrex import Bittrex, API_V1_1
import os
import sys
import re
import time
from termcolor import colored

import auth
import image
import parseJson as data
import coinOfTheWeek as cotw
import rich

reload(sys)
sys.setdefaultencoding('utf8')
bittrex_api_version = API_V1_1

def main():
    parseJson.parseSecret()
    apiTwitter = auth.authentification()

    while True:
        try:
            lastTweetFirst = apiTwitter.user_timeline(screen_name = data.dataTwitter['twitterAccount'], count = 1, include_rts = False)[0].text
        except:
            print colored('Getting last tweet error', 'red')
            time.sleep(3)
            continue
        break
    while True:
        try:
            lastTweet = apiTwitter.user_timeline(screen_name = data.dataTwitter['twitterAccount'], count = 1, include_rts = False)
        except:
            print colored('Getting last tweet error', 'red')
            time.sleep(3)
            continue
        if lastTweet[0].text != lastTweetFirst and 'coin of the week' in lastTweet[0].text.lower():
            lastTweetFirst = lastTweet[0].text
            print colored('New tweet about coin of the week !!!', 'red')
            mybittrex = Bittrex(data.dataBittrex['my_api_key'], data.dataBittrex['my_api_secret'], api_version=bittrex_api_version)
            coinOfTheWeek = cotw.getCoinOfTheWeek(apiTwitter, mybittrex, lastTweet)
    #coinOfTheWeek = "ETH"
            if coinOfTheWeek == False:
                print colored('Coin not available in Bittrex :(', 'magenta')
                continue
            print colored(coinOfTheWeek, 'magenta')
            rich.getRich(coinOfTheWeek, mybittrex)
        else:
            print colored('Current tweet : ', 'green'), colored (lastTweet[0].text, 'yellow'), colored('\nWaiting for new tweet', 'green')
        time.sleep(3)


if __name__ == '__main__':
    main()
