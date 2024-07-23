import re
import requests
from datetime import datetime, timezone
import time
from bs4 import BeautifulSoup
import pytz
import os
import paramiko
# pip install --upgrade pip
# #pip install beautifulsoup4
# pip install pytz
# pip install paramiko

inTheZone = False

def getLocalTime():
    timeZone = pytz.timezone("Europe/Oslo")
    localTime = datetime.now(timeZone)
    return localTime


def extract_numeric_value(string):
    numeric_value = re.findall(r'\d+', string)
    if numeric_value:
        return int(numeric_value[0])
    else:
        return None


def get_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print("Image saved successfully!")
    else:
        print("Failed to download image.")


def isNowInTimePeriod(startTime, endTime, nowTime): 
    if startTime < endTime: 
        return nowTime >= startTime and nowTime <= endTime 
    else: 
        #Over midnight: 
        return nowTime >= startTime or nowTime <= endTime 


def get_Interval():
    #Get the interval for camera updates
    global interval
    website_url = "https://trmfk.no/next/p/66934/webcam-udduvoll"
    page_data = requests.get(website_url).content
    page_content = page_data.decode()
    position1 = page_content.find("Bildet oppdateres hvert")
    position2 = page_content.find("minutt",position1)
    if (position1 > 0):
        interval = extract_numeric_value(page_content[position1:position2])
        print(interval)


def get_Timespan():
    #Get the time range for camera updates
    global inTheZone
    
    website_url = "https://trmfk.no/next/p/66934/webcam-udduvoll"
    page_data = requests.get(website_url).content
    page_content = page_data.decode()
    position = page_content.find(" i perioden ")
    if (position > 0):
        timeStart = page_content[position+12:position+17].split(':')
        print(timeStart)
        timeEnd = page_content[position+22:position+27].split(':')
        print(timeEnd)
        print('found time range')

        currentTime = getLocalTime()
        startPeriod = currentTime.replace(hour=int(timeStart[0]),minute=int(timeStart[1]),second=0)
        endPeriod   = currentTime.replace(hour=int(timeEnd[0]),minute=int(timeEnd[1]),second=0)
        print(currentTime)
        print(startPeriod)
        print(endPeriod)
        if isNowInTimePeriod(startPeriod, endPeriod, currentTime):
            print("time is within range")
            inTheZone = True
        else:
            print("time is outside range")

get_Timespan()
get_Interval()

if (inTheZone == True):
    localTime = getLocalTime()
    currentLocalTime = localTime.strftime("%H:%M")
    folderName = ".devcontainer/images/" + localTime.strftime("%Y%m%d")
    if (os.path.exists(folderName)):
        print("Folder exists")
    else:
        print("Folder does not exist")
        os.mkdir(folderName)

    print(inTheZone)

    print(folderName)
    url = "http://cameraftpapi.drivehq.com/api/Camera/GetCameraThumbnail.ashx?parentID=267333388&shareID=14174284"
    save_path = folderName + "/" + currentLocalTime + ".png"
    get_image(url, save_path)

