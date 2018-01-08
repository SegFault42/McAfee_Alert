import json

dataTwitter = []
dataBittrex = []

def parseTwitter(data):
    global dataTwitter
    dataTwitter = data["Twitter param"]

def parseBittrex(data):
    global dataBittrex
    dataBittrex = data["Bittrex param"]

def parseSecret():
    data = json.load(open('config.json'))
    parseTwitter(data)
    parseBittrex(data)
