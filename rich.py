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
import tempfile
import subprocess
import re
import wget
import image
from termcolor import colored

commission_percentage = 1.25
safe_buyorsell_percentage = 4.0
percentage_change_to_trigger_sell = 5.0

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

def getBalance(token, crypto):
    balance = token.get_balance(crypto)
    if balance['success'] != True:
        print "FATAL ERROR : " + balance['message']
        return (None)
    if balance['result'] is None:
        return (0.0)
    return (balance['result']['Balance'])

def getMarket(token, name):
    print "Fetching market " + name
    results = token.get_market_summaries()
    #print results
    if results['success'] != True:
        print "FATAL ERROR : " + results['message']
        return (None)
    for result in results['result']:
        if result['MarketName'] == name:
            return (result)
    print "ERROR : Failed to fetch market"
    return (None)

def allOut(token, market, crypto_balance):
    quantity = btc_balance / (market['Bid'] - market['Bid'] * safe_buyorsell_percentage / 100.0)
    commission = quantity * market['Bid'] * commission_percentage / 100.0
    print "Selling on " + market['MarketName'] + ", quantity = " + str(quantity) + ", price = " + str(market['Bid']) + ", commission = " + str(commission) + ", subtotal = " + str(quantity - commission)
    quantity -= commission
    sell = token.sell_limit(market['MaketName'], quantity, market['Bid'])
    if sell['success'] != True:
        print "FATAL ERROR : " + sell['message']
        return (False)
    for key in sell['result'].keys():
        print str(key) + ": " + str(sell['result'][key])
    return (True)

def allIn(token, market, btc_balance):
    quantity = btc_balance / (market['Ask'] + market['Ask'] * safe_buyorsell_percentage / 100.0)
    commission = quantity * market['Ask'] * commission_percentage / 100.0
    print "Buying on " + market['MarketName'] + ", quantity = " + str(quantity) + ", price = " + str(market['Ask']) + ", commission = " + str(commission) + ", subtotal = " + str(quantity - commission)
    quantity -= commission
    buy = token.buy_limit(market['MarketName'], quantity, market['Ask'])
    if buy['success'] != True:
        print "FATAL ERROR : " + buy['message']
        return (False)
    for key in buy['result'].keys():
        print str(key) + ": " + str(buy['result'][key])
    return (True)

def getRich(coinOfTheWeek, bittrex_token):
#   Init
    btc_balance = 0.0
    market = ""

#   Body    
    btc_balance = getBalance(bittrex_token, "BTC")
    if btc_balance is None:
        print colored("You have no BTC :'(, aborting", 'red')
        return (False)
    coinOfTheWeek_balance = getBalance(bittrex_token, coinOfTheWeek)
    if coinOfTheWeek_balance is None:
        coinOfTheWeek_balance = 0.0
    print "You currently have " + str(coinOfTheWeek_balance) + " " + str(coinOfTheWeek) + " and " + str(btc_balance) + " BTC"
    market = getMarket(bittrex_token, "BTC-" + coinOfTheWeek)
    if market is None:
        print("Market is None", 'red')
        return
    if allIn(bittrex_token, market, btc_balance) != True:
        print("Failed to all in", 'red')
    btc_balance = getBalance(bittrex_token, "BTC")
    if btc_balance is None:
        print("btc_balance is None", 'red')
        return
    coinOfTheWeek_balance = getBalance(bittrex_token, coinOfTheWeek)
    if coinOfTheWeek_balance is None:
        return
    print ("You now have " + str(coinOfTheWeek_balance) + " " + str(coinOfTheWeek) + " and " + str(btc_balance) + " BTC")
    while True:
        if monitor(bittrex_token, market, coinOfTheWeek) != True:
            print colored("Monitor failed, retrying", red)
        else:
            break
        time.sleep(1)
