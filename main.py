# -*- coding: utf8 -*-

import parseJson
import auth
import tweepy
import parseJson as data
import json
import wget
import image
from bittrex.bittrex import Bittrex
import os
import sys
import re
import time

reload(sys)
sys.setdefaultencoding('utf8')

def downloadImageFromTweet(apiTwitter):
    try:
        lastTweet = apiTwitter.user_timeline(screen_name = data.dataTwitter['twitterAccount'], count = 1, include_rts = False)
    except:
        print "Failing to get last tweet"
        return False
    #print lastTweet
    #print json.dumps(lastTweet[0]._json, indent = 2)
    imgUrl = lastTweet[0]._json['extended_entities']['media'][0]['media_url']
    imageName = wget.download(imgUrl)
    print ""
    return imageName

def seekCurrencie(content, allCurrencys):
    word = content.split(' ')
    i = 0
    j = 0
    while i < len(allCurrencys['result']):
        j = 0
        while j < len(word):
            if word[j] == allCurrencys['result'][i]['MarketCurrency'].lower():
                return allCurrencys['result'][i]['MarketCurrency']
            elif word[j] == allCurrencys['result'][i]['MarketCurrencyLong'].lower():
                return allCurrencys['result'][i]['MarketCurrencyLong']
            j += 1
        i += 1
    return 0

def epurContent(imageContent):
    imageContent = re.sub('[^a-zA-Z]+', ' ', imageContent)
    return imageContent.lower()

def main():
    parseJson.parseSecret()
    apiTwitter = auth.authentification()
    imageName = downloadImageFromTweet(apiTwitter)
    imageContent = image.imageToStr(imageName)
    os.remove(imageName)

    mybittrex = Bittrex(data.dataBittrex['my_api_key'], data.dataBittrex['my_api_secret'])
    #print json.dumps(mybittrex.get_markets(), indent = 4)

    imageContent = epurContent(imageContent)

    allCurrencys = mybittrex.get_markets()
    coinOfTheWeek =  seekCurrencie(imageContent, allCurrencys)
    print coinOfTheWeek


if __name__ == '__main__':
    main()
