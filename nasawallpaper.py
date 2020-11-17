from ctypes import windll
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from os import listdir, remove
import urllib.request


def main():
    try:
        print("Retrieving NASA image...")
        imageURL = getImageURL()
        print("Clearing old files...")
        fileDirectory = "YOUR_FILE_DIRECTORY_GOES_HERE"
        clearImages(fileDirectory)
        print("Saving file...")
        filename = getFilename()
        filePath = fileDirectory + filename
        saveImage(imageURL, filePath)
        print("Setting wallpaper...")
        setWallpaper(filePath)
        print("COMPLETE!")
    except:
        print("There is no new photo today")


def clearImages(fileDirectory):
    # Get list of all files in folder
    filesInDirectory = listdir(fileDirectory)

    # Delete photos
    for i in range(len(filesInDirectory)):
        if filesInDirectory[i][-4:] == ".jpg":
            file = fileDirectory + filesInDirectory[i]
            remove(file)


def getFilename():
    # Get filename based on date
    currentDateTime = datetime.now()
    month = currentDateTime.strftime("%B")
    day = currentDateTime.strftime("%d")
    year = currentDateTime.strftime("%Y")
    return "NASA-" + month + "-" + day + "-" + year + ".jpg"


def getImageURL():
    # Get link to latest image
    html = get("https://apod.nasa.gov/apod/astropix.html")
    soup = BeautifulSoup(html.text, "html.parser")
    parse = soup.findAll("a")
    imageURL = "https://apod.nasa.gov/apod/" + parse[1].get("href")
    return imageURL


def saveImage(imageURL, filePath):
    # Download image
    urllib.request.urlretrieve(imageURL, filePath)


def setWallpaper(filePath):
    # Set wallpaper
    windll.user32.SystemParametersInfoW(20, 0, filePath, 0)


if __name__ == "__main__":
    main()
