#!/usr/bin/env python
# -*- coding: utf8 -*-
import requests
import sys
import tweepy
import sys
from bittrex.bittrex import Bittrex, API_V1_1


consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
my_api_key = ""
my_api_secret = ""
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

def getCryptos(token):
    markets = token.get_markets()
#   markets format
#    {'success': True,
#     'message': '',
#     'result': [{'Notice' : '',
#                 'Created' : '',
#                 'MinTradeSize' : '',
#                 'IsSponsored' : '',
#                 'BaseCurrencyLong' : '',
#                 'MarketName' : '',
#                 'IsActive' : '',
#                 'LogoUrl' : '',
#                 'MarketCurrencyLong' : '',
#                 'BaseCurrency' : '',
#                 'MarketCurrency' : ''}, ...]
#    }
    if markets['success'] != True:
        print("FATAL ERROR : " + markets['message'])
        sys.exit()
    return (markets['result'])

def getBalance(token, crypto):
    result = token.get_balance(crypto)
#   response format
#    {'success': True, 
#     'message': '',
#     'result': {'Currency': 'ETH',
#                'Balance': 0.0,
#                'Available': 0.0, 
#                'Pending': 0.0,
#                'CryptoAddress': None}
#    }
    if result['success'] != True:
        print("FATAL ERROR : " + result['message'])
        sys.exit()
    return (result['result']['Balance'])
    
def getCoinOfTheDay(tweet):
    return ("BTC")

def main():
#   Init
    tweet = api.user_timeline(screen_name = '@officialmcafee', count = 1, include_rts = False)[0].text
    bittrex_token = Bittrex(my_api_key, my_api_secret, api_version=API_V1_1)
    cotd = getCoinOfTheDay(tweet)
    cotd_info = ""

#   Body
    print("God McAfee Says : " + tweet)
    
    if cotd != "":
        print("Crypto of the day is " + cotd)
    else:
        print("God McAfee isn't dropping any of those shiny shekels :'(")
        sys.exit()

    cryptos = getCryptos(bittrex_token)
    for crypto in cryptos:
        if cotd == crypto['BaseCurrency'] or cotd == crypto['BaseCurrencyLong']:
            print("Coin of the day '" + cotd + "' is tradeable")
            cotd_info = crypto
            break
    if cotd_info == "":
        print("FATAL ERROR : Coin of the day is not tradeable")
        sys.exit()
    print("You currently have " + str(getBalance(bittrex_token, "USDT")) + " " + str(cotd_info['BaseCurrency']))
    
#    for crypto in cryptos:
#        for key in crypto.keys():
#            if crypto[key]:
#                print("Key " + key + " = " + str(crypto[key]))



if __name__ == '__main__':
    main()
