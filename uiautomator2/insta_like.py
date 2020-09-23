#!/usr/bin/env python3

import uiautomator2 as u2

##### DEVICE start #####

def getDevice(ip = None):
    device = None
    if (ip):
        device = u2.connect("%s" % (ip))
    else:
        device = u2.connect()
    return device

##### DEVICE end #####
##### SCREEN INTERACT start #####

def scrollDown(device):
    device(scrollable=True).scroll.vert.forward(steps=50)

def scrollUp(device):
    device(scrollable=True).scroll.vert.backward(steps=50)
    
def scrollTop(device):
    device(scrollable=True).scroll.toBeginning()

def scrollBottom(device):
    device(scrollable=True).scroll.toEnd()

##### SCREEN INTERACT end #####
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