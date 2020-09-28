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
    device.swipe_ext("up", scale=0.3)

def scrollUp(device):
    device.swipe_ext("down", scale=0.3)
    
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
##### HOME start #####

def isHome(device):
    return device.xpath("//android.widget.FrameLayout[@content-desc='Home']").info["selected"] == "true"

def homeGo(device):
    device.xpath("//android.widget.FrameLayout[@content-desc='Home']").click()
    
def getWidgetY(widget):
    return widget.center()[1]

def getProfiles(device):
    profiles = device(className="android.widget.TextView", resourceId="com.instagram.android:id/row_feed_photo_profile_name")
    if (len(profiles)):
        return profiles
    return []

def getTopProfile(device):
    profiles = getProfiles(device)
    if len(profiles):
        return profiles[0]
    return None

def getNextProfile(device, profile):
    for widget in getProfiles(device):
        if getWidgetY(widget) > getWidgetY(profile):
            return widget 
    return None

def getProfileName(profile):
    return profile.info["text"]

def swipeProfileToTop(device, profile):
    HEADER_OFFSET = 150
    profile.swipe_ext("up", box=(100, 500, 100, 500+))

def isProfileSponsored(profile):
    sibling = profile.sibling(text="Sponsored")
    if (len(sibling)):
        return True
    return False

def printProfileNames(device, num):
    currentView = None
    for i in range(num):
        view = getTopProfile(device)
        print(view)
        if (view != currentView):
            print(getProfileName(view))
            currentView = view
        scrollDown(device)
        

def getTopButtons(device):
    return device.xpath("//*[@resource-id='com.instagram.android:id/row_feed_view_group_buttons']")

def getButtonsBelowProfile(device, profile):
    for widget in device.xpath("//*[@resource-id='com.instagram.android:id/row_feed_view_group_buttons']").all():
        if getWidgetY(widget) > getWidgetY(profile):
            return widget 
    return None
    

##### HOME end #####
##### SEARCH AND EXPLORE start #####

def isSearchAndExplore(device):
    return device.xpath("//android.widget.FrameLayout[@content-desc='Search and Explore']").info["selected"] == "true"

def searchAndExploreGo(device):
    device.xpath("//android.widget.FrameLayout[@content-desc='Search and Explore']").click()

##### SEARCH AND EXPLORE end #####
##### CAMERA start #####

def isCamera(device):
    return device.xpath("//android.widget.FrameLayout[@content-desc='Camera']").info["selected"] == "true"

def cameraGo(device):
    device.xpath("//android.widget.FrameLayout[@content-desc='Camera']").click()

##### CAMERA end #####
##### ACTIVITY start #####

def isActivity(device):
    return device.xpath("//android.widget.FrameLayout[@content-desc='Activity']").info["selected"] == "true"

def activityGo(device):
    device.xpath("//android.widget.FrameLayout[@content-desc='Activity']").click()

##### ACTIVITY end #####
##### PROFILE start #####

def isProfile(device):
    return device.xpath("//android.widget.FrameLayout[@content-desc='Profile']").info["selected"] == "true"

def profileGo(device):
    device.xpath("//android.widget.FrameLayout[@content-desc='Profile']").click()

##### PROFILE end #####
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