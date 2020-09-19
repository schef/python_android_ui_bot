#!/usr/bin/env python3

import sys
from ppadb.client import Client
from PIL import Image
import time
import cv2
import numpy as np
import random
import re

TAB = "    "
NEW_LINE = "\n"

RANDOM_TRESHOLD = 50
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
FLAG_DARK_MODE = 1
ENABLE_CAUGHT_UP = False
PASSWD = 0

def getRandom(num, treshold = RANDOM_TRESHOLD):
    random.randint(num - RANDOM_TRESHOLD, num + RANDOM_TRESHOLD)
    return num

def getAdbDevice():
    adb = Client(host='127.0.0.1', port=5037)
    devices = adb.devices()

    if len(devices) == 0:
        print('no device attached')
        quit()

    device = devices[0]
    return device

def press(device, x, y):
    device.shell('input touchscreen swipe %d %d %d %d %d' % (getRandom(x, 5), getRandom(y, 5), getRandom(x, 5), getRandom(y, 5), getRandom(50)))
    
def scrollUp(device):
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    device.shell('input touchscreen swipe %d %d %d %d %d' % (getRandom(SCREEN_WIDTH*0.5), getRandom(SCREEN_HEIGHT*0.4), getRandom(SCREEN_WIDTH*0.5), getRandom(SCREEN_HEIGHT*0.6), getRandom(300)))

def scrollDown(device):
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    device.shell('input touchscreen swipe %d %d %d %d %d' % (getRandom(SCREEN_WIDTH*0.5), getRandom(SCREEN_HEIGHT*0.6), getRandom(SCREEN_WIDTH*0.5), getRandom(SCREEN_HEIGHT*0.4), getRandom(300)))

def getImage(device):
    image = device.screencap()
    with open('screen.png', 'wb') as f:
        f.write(image)

def drawLikeInImage():
    img_rgb = cv2.imread('screen.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('like.png',0)
    w, h = template.shape[::-1]
    
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    
    cv2.imwrite('result.png',img_rgb)

def findLikeInImage():
    global FLAG_DARK_MODE
    global ENABLE_CAUGHT_UP
    locations = []

    img_rgb = cv2.imread('screen.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    if(int(FLAG_DARK_MODE) == 2):
        template = cv2.imread('like_dark_mode_on.png',0)
        caughtup = cv2.imread('caught_up_dark_mode_on.png',0)
    else:
        template = cv2.imread('like_dark_mode_off.png',0)
        caughtup = cv2.imread('caught_up_dark_mode_off.png',0)

    w, h = template.shape[::-1]

    if(ENABLE_CAUGHT_UP == True):
        res = cv2.matchTemplate(img_gray,caughtup,cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            locationFound = False
            for l in locations:
                if (abs(pt[0] - l[0]) < 5 and abs(pt[1] - l[1]) < 5):
                    locationFound = True
            if (not locationFound):
                locations.append(pt)

        if(locations):
            quit()

    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.6
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        locationFound = False
        for l in locations:
            if (abs(pt[0] - l[0]) < 5 and abs(pt[1] - l[1]) < 5):
                locationFound = True
        if (not locationFound):
            locations.append(pt)
    return locations

def findLike(device):
    while True:
        scrollDown(device)
        time.sleep(1)
        getImage(device)

        locations = findLikeInImage()
        print(locations)
        locations.pop()
        if (locations):
            print("Found")
            press(device, locations[0][0], locations[0][1])
            time.sleep(1)

def getResolution(device):
    deviceDump = device.shell('dumpsys display')
    reSearch = ".*deviceWidth=(\d+), deviceHeight=(\d+).*"
    resolution = re.search(reSearch, deviceDump)
    width = resolution.group(1)
    height = resolution.group(2)
    return int(width), int(height)

def getDarkModeFlag(device):
    stream = device.shell('settings get secure ui_night_mode')
    if (stream == "1"):
        return 1
    else:
        return 0

def openDevice(device):
    global PASSWD
    flag = isDeviceUnlocked(device)
    if (flag):
        stream = device.shell('input keyevent 26')
        time.sleep(1)

    stream = device.shell('input keyevent 26')
    time.sleep(1)
    stream = device.shell('input touchscreen swipe %d %d %d %d' % (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.6, SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.3))
    time.sleep(1)
    stream = device.shell('input text ' + PASSWD)
    time.sleep(1)
    stream = device.shell('input keyevent 66')
    time.sleep(1)
    flag = isDeviceUnlocked(device)
    return flag

def isDeviceUnlocked(device):
    deviceDump = device.shell('dumpsys display')
    reSearch = ".*mScreenState=(\w+).*"
    screenState = re.search(reSearch, deviceDump)
    state = screenState.group(1)
    if (state == "ON"):
        return 1
    else:
        return 0

def startInstagramApp(device):
    stream = device.shell('am start -n com.instagram.android/.activity.MainTabActivity -c android.intent.category.HOME')

def printCmdList():
    global NEW_LINE
    global TAB

    info = "Usage:" + NEW_LINE + NEW_LINE
    info += "<MANDATORY> commands:" + NEW_LINE
    info += TAB + "-e/-d" + NEW_LINE
    info += TAB + TAB + "enable/disable feature stop liking when \"caught up\" message is hit" + NEW_LINE
    info += "<OPTIONAL> commands:" + NEW_LINE
    info += TAB + "-a [PASSWD]" + NEW_LINE
    info += TAB + TAB + "use plug and play feature; needs your phone password [PASSWD]" + NEW_LINE
    print(info)
    sys.exit()

if __name__ == "__main__":

    if (len(sys.argv) >= 2):
        if (sys.argv[1] == "-e"):
            ENABLE_CAUGHT_UP = True
        elif (sys.argv[1] == "-d"):
            ENABLE_CAUGHT_UP = False
        else:
            print("Missing <MANDATORY> command!\n")
            printCmdList()
            sys.exit()

        device = getAdbDevice()
        SCREEN_WIDTH, SCREEN_HEIGHT = getResolution(device)
        FLAG_DARK_MODE = getDarkModeFlag(device)

        if (len(sys.argv) == 3):
            print("Missing data!\n")
            printCmdList()

        if (len(sys.argv) == 4):
            if (sys.argv[2] == "-a"):
                if (sys.argv[3]):
                    PASSWD = str(sys.argv[3])
                else:
                    print("Missing [PASSWD] for automatic mode!\n")
                    printCmdList()
                if (openDevice(device)):
                    time.sleep(1)
                    startInstagramApp(device)
            else:
                print("Not valid command!\n")
                printCmdList()

    else:
        print("Missing commands!\n")
        printCmdList()

    if (isDeviceUnlocked(device)):
        startInstagramApp(device)
        time.sleep(1)
        findLike(device)
    else:
        print("Device not unlocked!\n")
