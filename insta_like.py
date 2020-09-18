#!/usr/bin/env python3

from ppadb.client import Client
from PIL import Image
import time
import cv2
import numpy as np
import random

RANDOM_TRESHOLD = 50

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
    device.shell('input touchscreen swipe %d %d %d %d %d' % (getRandom(500), getRandom(500), getRandom(500), getRandom(1000), getRandom(300)))

def scrollDown(device):
    device.shell('input touchscreen swipe %d %d %d %d %d' % (getRandom(500), getRandom(1000), getRandom(500), getRandom(500), getRandom(300)))

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
    locations = []

    img_rgb = cv2.imread('screen.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('like.png',0)
    w, h = template.shape[::-1]
    
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
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

if __name__ == "__main__":
    device = getAdbDevice()
    #press(device, 100, 200)
    