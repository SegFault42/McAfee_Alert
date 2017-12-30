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
    content = content.replace('\n', ' ')
    word = content.split(' ')
    i = 0
    j = 0
    while i < len(allCurrencys['result']):
        j = 0
        while j < len(word):
            print "word[j] = " + word[j] + '\n' + "Currency = " + allCurrencys['result'][i]['MarketCurrency']
            word[j] = word[j].lower()
            allCurrencys['result'][i]['MarketCurrency'] = allCurrencys['result'][i]['MarketCurrency'].lower()

            if (word[j].find(allCurrencys['result'][i]['MarketCurrency']) != -1):
                return allCurrencys['result'][i]['MarketCurrency']
            j += 1
        i += 1
    return 0

def main():
    parseJson.parseSecret()
    apiTwitter = auth.authentification()
    imageName = downloadImageFromTweet(apiTwitter)
    imageContent = image.imageToStr(imageName)
    os.remove(imageName)

    mybittrex = Bittrex(data.dataBittrex['my_api_key'], data.dataBittrex['my_api_secret'])
    #print json.dumps(mybittrex.get_markets(), indent = 4)
    allCurrencys = mybittrex.get_markets()
    print seekCurrencie(imageContent, allCurrencys)


if __name__ == '__main__':
    main()
