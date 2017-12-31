import json

dataMail = []
dataTwitter = []
dataBittrex = []

def parseMail(data):
    global dataMail
    dataMail = data["Mail param"]

def parseTwitter(data):
    global dataTwitter
    dataTwitter = data["Twitter param"]

def parseBittrex(data):
    global dataBittrex
    dataBittrex = data["Bittrex param"]

def parseSecret():
    data = json.load(open('config.json'))
    parseMail(data)
    parseTwitter(data)
    parseBittrex(data)
