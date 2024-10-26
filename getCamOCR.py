import easyocr
import time
import requests
import datetime
import os
from datetime import datetime
import shutil

def get_image(url, destination):
    response = requests.get(url)
    if response.status_code == 200:
        with open(destination, 'wb') as file:
            file.write(response.content)

path = os.getcwd()
print("Current Directory", path)

url = "http://cameraftpapi.drivehq.com/api/Camera/GetCameraThumbnail.ashx?parentID=267333388&shareID=14174284"
localTime = datetime.now()
eval_file = path + '/pictures/eval/eval.png'
lastPictureStamp = datetime.now()

# Get image to temporary folder and get the timestamp
reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory

while True:
    get_image(url,eval_file)
    result = reader.readtext(eval_file, detail = 0)
    datetime_str = result[2] + " " + result[3]
    datetime_str = datetime_str.replace(".", ":")
    try:
        pictureStamp = datetime.strptime(datetime_str, '%d-%m-%Y %H:%M:%S')
        print(pictureStamp)

        if pictureStamp == lastPictureStamp:
            print("Still the same image")
        else:
            folderName = path + '/pictures/' + pictureStamp.strftime("%Y%m%d")
            fileName = pictureStamp.strftime("%H-%M-%S") + ".png" 
            if (os.path.exists(folderName)):
                print("Folder exists")
            else:
                print("Folder does not exist")
                os.mkdir(folderName)
            
            print("Moving image")
            shutil.move(eval_file, folderName + "/" + fileName)
    except:
        print("An error occurred")
    lastPictureStamp = pictureStamp
    time.sleep(60)
