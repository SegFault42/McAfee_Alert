import parseJson as data
import tweepy

def authTwitter():
    auth = tweepy.OAuthHandler(data.dataTwitter['consumer_key'], data.dataTwitter['consumer_secret'])
    auth.set_access_token(data.dataTwitter['access_token'], data.dataTwitter['access_token_secret'])
    api = tweepy.API(auth)
    return api

def authentification():
    return authTwitter()
