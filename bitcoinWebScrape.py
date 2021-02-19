#!/usr/bin/env python
#
# The first half of this code was pulled from gistable on GITHub (https://github.com/gistable). Thanks to them, we were able to pull all the data we needed. 
#
import requests, subprocess, time, smtplib, math
from bs4 import BeautifulSoup
from notify_run import Notify
import array as arr

class BitcoinPrice:
    price = 0

    website = "http://www.bitcoinexchangerate.org/"

    def _getSite(self):
        rawHtml = requests.get(self.website).text
        return rawHtml

    def _parseSite(self, rawHtml):
        site = BeautifulSoup(rawHtml, features="html.parser")
        titleString = site.title.string
        priceString = ""
        #iterate through webpage title and grab the numbers
        for char in titleString:
            if char.isdigit() or char == ".":
                priceString += char #add digit to string
            elif(char == 'U'): #end on the USD
                break
        return priceString

    def _getPriceFromWeb(self):
        self.price = float(self._parseSite(self._getSite()))

    def getPrice(self):
        return self.price

    def updatePrice(self):
        self._getPriceFromWeb()

    def __init__(self):
        self._getPriceFromWeb()


priceObj = BitcoinPrice()

def toPurchase(bitPrices):
    k = 0
    priceChange = 0
    for i in bitPrices :
        priceChange += i * (math.pow(-1, k))
        k+=1
    return priceChange

bitPrices = [None]*40
bitCounter = 0
shouldBuy = 0
scriptStart = True
timePass = 0
bitHigh = priceObj.getPrice()
bitLow = bitHigh
highChange = 0
lowChange = 0
notify = Notify()
result = ""

#In this section, the logic behind when to buy/sell is developed. It definitely needs some waork, as it it is not very adaptable. 
while True: #Main loop that will send the text and Push Alert
    price = priceObj.getPrice()
    bitPrices[bitCounter] = price
    bitCounter += 1
    
    if scriptStart:
        result = "Script is starting. Bitcoin Price: $" + str(price)
        notify.send(result)
        scriptStart = False

    if price > bitHigh :
        bitHigh = price
        highChange += 1

    elif price < bitLow :
        bitLow = price
        lowChange += 1

    if highChange > 8 :
        result = "$" + str(price) + " Bitcoin is rising."
        notify.send(result)
        highChange = 0
        lowChange = 0

    elif lowChange > 8 :
        result = "$" + str(price) + " Bitcoin is falling."
        notify.send(result)
        highChange = 0
        lowChange = 0

    if bitCounter >= 40 :
        shouldBuy = toPurchase(bitPrices)
        bitCounter = 0

    if (shouldBuy > 100) :
        result = "$" + str(price) + " Bitcoin price is rising fast."
        notify.send(result)

    elif (shouldBuy < -100) :
        result = "$" + str(price) + " Bitcoin price is falling fast."
        notify.send(result)

    if timePass == 360 :
        result = "$" + str(price) + " Hour High Price: $" + str(bitHigh) + " Hour Low Price: $" + str(bitLow)
        notify.send(result)
        bitHigh = price
        bitLow = price
        timePass = 0

    priceObj.updatePrice()
    timePass += 1
    #only check the price every 10 seconds. Be careful of limits that sites set for scraping.
    time.sleep(10)
