#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
from datetime import datetime
import requests
import sys
import tweepy
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import time
from bittrex.bittrex import Bittrex, API_V1_1
import json
import cv2
import numpy as np
import pytesseract
from PIL import Image

# mail parameters
server_login = ""
server_password = ""
fromAddr = ""
toAddr = ""
# twitter parameters
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
# bittrex parameters
my_api_key = ""
my_api_secret = ""
bittrex_api_version = API_V1_1
# details
this_path = os.path.abspath(os.path.dirname(sys.argv[0]))
logfiles_location = os.path.join(this_path, "logfiles/")
logfile_name = os.path.join(logfiles_location, "LOG_" + str(datetime.now()) + ".txt")
logfile = None
twitterAccount = ""
twitterAccountReceiver = ""

src_path = "/home/segfault42/Desktop/"


server = smtplib.SMTP('smtp.gmail.com', 587)

commission_percentage = 1.25
percentage_change_to_trigger_sell = 5.0
safe_buyorsell_percentage = 4.0

def authMail(data):
    global toAddr
    global fromAddr
    global server_login
    global server_password
    server_login = data["server_login"]
    server_password = data["server_password"]
    toAddr = data["toAddr"]
    fromAddr = server_login
    server.starttls()
    server.login(server_login, server_password)

def authTwitter(data):
    global twitterAccount
    global twitterAccountReceiver
    global consumer_key
    global consumer_secret
    global access_token
    global access_token_secret
    consumer_key = data["consumer_key"]
    consumer_secret = data["consumer_secret"]
    access_token = data["access_token"]
    access_token_secret = data["access_token_secret"]
    twitterAccount = data["twitterAccount"]
    twitterAccountReceiver = data["twitterAccountReceiver"]
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def authBittrex(data):
    global my_api_key
    global my_api_secret
    my_api_key = data["my_api_key"]
    my_api_secret = data["my_api_secret"]
    bittrex_token = Bittrex(my_api_key, my_api_secret, api_version=bittrex_api_version)
    return bittrex_token

def logger(msg):
    logfile.write(msg + '\n')
    print(msg)

def sendMail(message):
    msg = MIMEMultipart()
    msg['From'] = fromAddr
    msg['To'] = toAddr
    msg['Subject'] = "McAfee Alert !"
    msg.attach(MIMEText(message.encode('utf-8'), 'plain'))
    server.sendmail(fromAddr, toAddr, msg.as_string())
    server.quit()

def tweetAlert(api):
    tweet = twitterAccountReceiver + "\n" + ''.join("McAfee Alert !!")
    try:
        api.update_status(status=tweet)
    except:
        pass

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

def getBalance(token, crypto):
    balance = token.get_balance(crypto)
#   response format
#    {'success': True, 
#     'message': '',
#     'result': {'Currency': 'ETH',
#                'Balance': 0.0,
#                'Available': 0.0, 
#                'Pending': 0.0,
#                'CryptoAddress': None}
#    }
    if balance['success'] != True:
        logger("FATAL ERROR : " + balance['message'])
        return (None)
    if balance['result'] is None:
        return (0.0)
    return (balance['result']['Balance'])
    
def getCoinOfTheDay(tweet, cryptos):
    if "Coin of the day" in tweet:
        words = tweet.split(' ')
        for word in words:
            for crypto in cryptos:
                if word.lower() == crypto['Currency'].lower() or word.upper() == crypto['CurrencyLong'].upper():
                    return (crypto)
    return (None)

def getMarket(token, name):
    logger("Fetching market " + name)
    results = token.get_market_summaries()
    if results['success'] != True:
        logger("FATAL ERROR : " + results['message'])
        return (None)
    #api 2.0 code, not used
    #for result in results['result']:
    #    if result['Summary']['MarketName'] == name:
    #        return (result['Summary'])
    for result in results['result']:
        if result['MarketName'] == name:
            return (result)
#api 2.0 format, not used
#   summary format
#     'summary': {'PrevDay': 4.95e-06,
#                'Volume': 447815716.2715876,
#                'Last': 4.59e-06,
#                'OpenSellOrders': 3645,
#                'TimeStamp': '2017-12-24T06:45:47.06',
#                'Bid': 4.57e-06,
#                'Created': '2014-09-16T07:41:56.047',
#                'OpenBuyOrders': 1384,
#                'High': 6.84e-06,
#                'MarketName': 'BTC-BURST',
#                'Low': 4.05e-06,
#                'Ask': 4.59e-06,
#                'BaseVolume': 2334.52544487}
    logger("ERROR : Failed to fetch market")
    return (None)

def allIn(token, market, btc_balance):
    quantity = btc_balance / (market['Ask'] + market['Ask'] * safe_buyorsell_percentage / 100.0)
    commission = quantity * market['Ask'] * commission_percentage / 100.0
    logger("Buying on " + market['MarketName'] + ", quantity = " + str(quantity) + ", price = " + str(market['Ask']) + ", commission = " + str(commission) + ", subtotal = " + str(quantity - commission))
    quantity -= commission
    #api 2.0 code, not used
    #buy = token.trade_buy(market=market['MarketName'], order_type='LIMIT', quantity=quantity, time_in_effect='GOOD_TIL_CANCELLED', rate=market['Ask'])
    buy = token.buy_limit(market['MarketName'], quantity, market['Ask'])
    if buy['success'] != True:
        logger("FATAL ERROR : " + buy['message'])
        return (False)
    for key in buy['result'].keys():
        logger(str(key) + ": " + str(buy['result'][key]))
    return (True)

def allOut(token, market, crypto_balance):
    quantity = btc_balance / (market['Bid'] - market['Bid'] * safe_buyorsell_percentage / 100.0)
    commission = quantity * market['Bid'] * commission_percentage / 100.0
    logger("Selling on " + market['MarketName'] + ", quantity = " + str(quantity) + ", price = " + str(market['Bid']) + ", commission = " + str(commission) + ", subtotal = " + str(quantity - commission))
    quantity -= commission
    #api 2.0 code, not used
    #sell = token.trade_sell(...)
    sell = token.sell_limit(market['MaketName'], quantity, market['Bid'])
    if sell['success'] != True:
        logger("FATAL ERROR : " + sell['message'])
        return (False)
    for key in sell['result'].keys():
        logger(str(key) + ": " + str(sell['result'][key]))
    return (True)

def monitor(token, market, crypto):
    max_price = 0.0
    percent_change = 0.0
    while True:
        market = getMarket(token, market['MarketName'])
        if market is None:
            return False
        if market['Last'] > max_price:
            max_price = market['Last']
        else:
            percent_change = (1.0 - market['Last'] / max_price) * 100.0
            if percent_change >= percentage_change_to_trigger_sell:
                if not allOut(token, market, getBalance(token, crypto)):
                    return False
                else:
                    return True
                break
        time.sleep(1)
    return False
            
    
def getRich(tweet, bittrex_token):
#   Init
    cryptos = getCryptos(bittrex_token)
    cotd = getCoinOfTheDay(tweet, cryptos)
    btc_balance = 0.0
    market = ""
    
#   Body    
    if cotd != None:
        logger("Crypto of the day is " + cotd['CurrencyLong'] + " (" + cotd['Currency'] + ")")
    else:
        logger("Oh no, it seems that he's not talking about a coin that's available on bittrex... better luck next time I guess...")
        return
    btc_balance = getBalance(bittrex_token, "BTC")
    if btc_balance is None:
        logger("You have no BTC :'(, aborting")
        return (False)
    cotd_balance = getBalance(bittrex_token, cotd['Currency'])
    if cotd_balance is None:
        cotd_balance = 0.0
    logger("You currently have " + str(cotd_balance) + " " + str(cotd['Currency']) + " and " + str(btc_balance) + " BTC")
    market = getMarket(bittrex_token, "BTC-" + cotd['Currency'])
    if market is None:
        return
    if allIn(bittrex_token, market, btc_balance) != True:
        logger("Failed to all in")
    btc_balance = getBalance(bittrex_token, "BTC")
    if btc_balance is None:
        return
    cotd_balance = getBalance(bittrex_token, cotd['Currency'])
    if cotd_balance is None:
        return
    logger("You now have " + str(cotd_balance) + " " + str(cotd['Currency']) + " and " + str(btc_balance) + " BTC")
    while True:
        if monitor(bittrex_token, market, cotd['Currency']) != True:
            logger("Monitor failed, retrying")
        else:
            break
        time.sleep(1)

def get_string(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    cv2.imwrite(src_path + "removed_noise.png", img)
    cv2.imwrite(src_path + "thres.png", img)
    result = pytesseract.image_to_string(Image.open(src_path + "thres.png"))
    return result

def main():
    global logfile_name
    global logfile
    if not os.path.isdir(logfiles_location):
        os.mkdir(logfiles_location)
    data = json.load(open('config.json'))
    print get_string(src_path + "image.jpeg")
    #authMail(data)
    #api = authTwitter(data)
    #bittrex_token = authBittrex(data)
    #lastTweet = api.user_timeline(screen_name = twitterAccount, count = 1, include_rts = False)[0].text.encode('utf-8')
    #print ("Starting program ! Current last tweet is " + lastTweet + ", waiting for new one")
    #while True:
        #tweet = api.user_timeline(screen_name = twitterAccount, count = 1, include_rts = False)[0].text.encode('utf-8')
        ##tweet = "Coin of the day: burst"
        #if tweet != lastTweet:
            #lastTweet = tweet
            #logfile_name = os.path.join(logfiles_location, "LOG_" + str(datetime.now()) + ".txt")
            #logfile = open(logfile_name, 'wb')
            #logger("Holy shit new tweet from god McAfee !!!11!1!")
            #logger(" It says : " + str(tweet))
            #if "coin of the week" in tweet.lower():
                #logger("OMFG It's actually about a new coin of the week !!111!! TIME TO GET RICH AF $$$")
                #getRich(tweet, bittrex_token)
                #logger("Done")
            #else:
                #logger("God McAfee isn't talking about shiny e-shekels :'(")
            #logfile.close()
            #if "coin of the week" in tweet.lower():
                #tweetAlert(api)
            ##with open(logfile_name, 'r') as message:
                ##sendMail(message.read())
        #time.sleep(2)

if __name__ == '__main__':
    main()
