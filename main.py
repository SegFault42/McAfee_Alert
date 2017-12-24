# -*- coding: utf-8 -*-

import requests
import sys
import tweepy
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import sys

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
#twitter_account_sender = "" #without @
#twitter_account_receiver = "" # without @

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("YOUR_MAIL", "YOUR_PASS")
fromAddr = "YOUR_MAIL"
toAddr = "TARGET_MAIL"

def tweet_current_value(tweet):
    try:
        api.update_status(status=tweet)
    except:
        pass

def sendMail(tweet):
    msg = MIMEMultipart()

    msg['From'] = fromAddr
    msg['To'] = toAddr
    msg['Subject'] = "McAfee Alert !"

    body = tweet.encode('utf-8')
    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()
    server.sendmail(fromAddr, toAddr, text)
    server.quit()

def alert(tweet):
    sendMail(tweet)

def main():
    #tweet_current_value("Hello world")
    stuff = api.user_timeline(screen_name = '@officialmcafee', count = 10, include_rts = True)
    for status in stuff:
        if "Coin of the day" in status.text:
            alert(status.text);

if __name__ == '__main__':
    main()
