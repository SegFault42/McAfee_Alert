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

fee = 0.25
percentBuySecure = 10

def checkAvailableCoin(bittrexApi, coin):
    balances = bittrexApi.get_balances()
    for coinLoop in balances['result']:
        if coinLoop['Currency'] == coin:
            if (coinLoop['Available'] > 0.0):
                print colored("Available " + coin + " : " + str(coinLoop['Available']), "green")
                return coinLoop['Available']
    print colored("No " + coin + " available !", "red")
    return False

def maxCoinBuy(availableBtc, pricePerCoin, buy_sell):
    if buy_sell == 0:
        units = availableBtc / pricePerCoin
    elif buy_sell == 1:
        units = availableBtc * pricePerCoin
    feeInBtc = units * fee / 100
    units = units - feeInBtc
    return round(units, 8)

def allIn(coinOfTheWeek, bittrexApi):
    print "AllIn :"
    btcBalance = checkAvailableCoin(bittrexApi, "BTC")
    if btcBalance == False:
        sys.exit(-1)
    pricePerCoin = bittrexApi.get_marketsummary("BTC-" + coinOfTheWeek)['result'][0]['Ask']
    maxCoin = maxCoinBuy(btcBalance, pricePerCoin, 0)
    print "btcBalance = " + str(btcBalance)
    print "pricePerCoin = " + str(pricePerCoin)
    print colored("Trying to buy :" + str(round(maxCoin * pricePerCoin, 8)) + " ETH", "cyan")
    #retBuy = bittrexApi.buy_limit("BTC-" + coinOfTheWeek, maxCoin, pricePerCoin)
    #if retBuy['success'] == True:
        #print colored("Order placed", "green")
    #else:
        #print colored (retBuy['message'], "red")

def allOut(coinOfTheWeek, bittrexApi):
    print "AllOut :"
    coinBalance = checkAvailableCoin(bittrexApi, coinOfTheWeek)
    if coinBalance == False:
        sys.exit(-1)
    pricePerCoin = bittrexApi.get_marketsummary("BTC-" + coinOfTheWeek)['result'][0]['Bid']
    print "pricePerCoin = " + str(round(pricePerCoin, 8))
    print "coinBalance = " + str(coinBalance)
    maxCoin = maxCoinBuy(coinBalance, pricePerCoin, 1)
    print "maxCoin = " + str(maxCoin)
    #retBuy = bittrexApi.sell_limit("BTC-" + coinOfTheWeek, maxCoin, pricePerCoin)
    #if retBuy['success'] == True:
        #print colored("Order placed", "green")
    #else:
        #print colored (retBuy['message'], "red")

def getRich(coinOfTheWeek, bittrexApi):
    allIn(coinOfTheWeek, bittrexApi)
    #orders = bittrexApi.get_open_orders("BTC-" + coinOfTheWeek)
    #while True:
        #if orders['success'] == True and not orders['result']:
            #print "No order\nSelling all " + coinOfTheWeek
    allOut(coinOfTheWeek, bittrexApi)
            #print "All coin as been selled"
            #break
        #else:
            #print "Order not selled"
        #time.sleep(1)
