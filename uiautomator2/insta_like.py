#!/usr/bin/env python3

import uiautomator2 as u2

##### DEVICE start #####

def getDevice():
    return u2.connect()

def isScreenOn(device):
    return device.info.get("screenOn")

def screenOn(device):
    device.screen_on()

def screenOff(device):
    device.screen_off()

def screenUnlock(device):
    device.unlock()

def getScreenWidth(device):
    return device.info["displayWidth"]

def getScreenHeight(device):
    return device.info["displayHeight"]

##### DEVICE end #####
##### UI INTERACT start #####

def pressHome(device):
    device.press("home")

def pressBack(device):
    device.press("back")

def pressMenu(device):
    device.press("menu")

def scrollDown(device):
    device(scrollable=True).scroll.vert.forward(steps=50)

def scrollUp(device):
    device(scrollable=True).scroll.vert.backward(steps=50)
    
def scrollTop(device):
    device(scrollable=True).scroll.toBeginning()

def scrollBottom(device):
    device(scrollable=True).scroll.toEnd()

##### UI INTERACT end #####
##### APP INFO start #####

PACKAGE_NAME = "com.instagram.android"

def isAppInstalled(device):
    try:
        return any(device.app_info(PACKAGE_NAME))
    except:
        return False
    
def isAppRunning(device):
    return PACKAGE_NAME in device.app_list_running()

def isAppInForeground(device):
    return device.info["currentPackageName"] == PACKAGE_NAME
    
def appStart(device):
    return device.app_start(PACKAGE_NAME)

def appStop(device):
    return device.app_stop(PACKAGE_NAME)

def appAutoResume(device):
    if (not isScreenOn(device)):
        screenUnlock(device)
    appStart(device)

def appAutoRestart(device):
    if isAppRunning(device):
        appStop(device)
    appAutoResume(device)

##### APP INFO end #####
##### BLOGGER start #####

def getUserName(device):
    text = device(className="android.widget.TextView", resourceId="com.instagram.android:id/action_bar_textview_title").get_text()
    return text

def getUserFullName(device):
    text = device(className="android.widget.TextView", resourceId="com.instagram.android:id/profile_header_full_name").get_text()
    return text

def getPostsCount(device):
    text = device(className="android.widget.TextView", resourceId="com.instagram.android:id/row_profile_header_textview_post_count").get_text()
    text = text.replace(",", "")
    return int(text)

def getFollowersCount(device):
    text = device(className="android.widget.TextView", resourceId="com.instagram.android:id/row_profile_header_textview_followers_count").get_text()
    text = text.replace(",", "")
    return int(text)

def getFollowingCount(device):
    text = device(className="android.widget.TextView", resourceId="com.instagram.android:id/row_profile_header_textview_following_count").get_text()
    text = text.replace(",", "")
    return int(text)

##### BLOGGER end #####

if __name__ == "__main__":
    device = getDevice()