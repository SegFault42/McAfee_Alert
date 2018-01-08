import wget
import json
import os
import re

import image

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
                return allCurrencys['result'][i]['MarketCurrency']
            j += 1
        i += 1
    return 0

def epurContent(imageContent):
    imageContent = re.sub('[^a-zA-Z]+', ' ', imageContent)
    return imageContent.lower()

def downloadImageFromTweet(apiTwitter, lastTweet):
    #print lastTweet
    #print json.dumps(lastTweet[0]._json, indent = 2)
    imgUrl = lastTweet[0]._json['extended_entities']['media'][0]['media_url']
    imageName = wget.download(imgUrl)
    print ""
    return imageName

def getCoinOfTheWeek(apiTwitter, mybittrex, lastTweet):
    if len(lastTweet[0]._json['entities']) == 4:
        return 2
    imageName = downloadImageFromTweet(apiTwitter, lastTweet)
    if imageName == False:
        return False
    imageContent = image.imageToStr(imageName)
    os.remove(imageName)
    imageContent = epurContent(imageContent)

    allCurrencys = mybittrex.get_markets()
    return seekCurrencie(imageContent, allCurrencys)
