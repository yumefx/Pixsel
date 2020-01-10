#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/12/27 12:08
# @Author : yumefx
# @File : isGrayPic.py

import os
from PIL import Image
import win32api,win32con,win32gui

#change image type to jpg
def imgConvertJpg(img,path=""):
    image = Image.open(img)
    image = image.convert("RGB")
    imgName = os.path.basename(img)
    newName = imgName[:imgName.rindex(".")] + ".jpg"
    if path == "":
        path = os.path.dirname(img)
    newImagePath = os.path.join(path,newName)
    image.save(newImagePath)
    return newImagePath
    
#set Wallpaper,only support [".jpg",".bmp"]
def setWallpaper(imgpath):
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,imgpath,1+2)
    
#set Wallpaper parameter,use fill to fit the desktop proportionally
def setWallpaperInit():
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,r"Control Panel\Desktop",0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key,"WallpaperStyle",0,win32con.REG_SZ,"6")
    win32api.RegSetValueEx(key,"TileWallpaper",0,win32con.REG_SZ,"0")

#reduce pixels,to get scatter fast
def changeSize(url,resizeDir = "",resizeDirect = "y",resizePixel = 250):
    #check input value
    if not os.path.isdir(resizeDir):
        os.mkdir(resizeDir)
    if not resizeDirect in ["x","y"]:
        return "wrong resizeType"
    if type(resizePixel) != int:
        return "wrong resizeLenth type"
    if resizePixel <= 0 :
        return "wrong resizeLenth"
    if not os.path.exists(url):
        return "wrong path"
    
    img = 0
    try:
        img = Image.open(url)
    except:
        return 0
    width = img.size[0]
    height = img.size[1]

    imgName = os.path.basename(url)
    if resizeDir == "":
        newpath = os.path.join(os.path.dirname(url),"resize_" + imgName)
    else:
        newpath = os.path.join(resizeDir,"resize_" + os.path.basename(url))
    try:
        if resizeDirect == "y":
            img.resize((int(width/(height/resizePixel)),resizePixel)).save(newpath)
        else:
            img.resize((resizePixel,int(height/(width/resizePixel)))).save(newpath)
    except:
        return 0
    return newpath
    
def get_color_Scatter(url):
    if url == 0:
        return -1
    img = 0
    try:
        img = Image.open(url)
    except:
        return -1
    pix = img.convert("RGB")
    width = img.size[0]
    height = img.size[1]
        
    maxColorScatter = 0
    avrColorScatter = 0
    for x in range(width):
        for y in range(height):
            #get pixel color scatter
            r,g,b = pix.getpixel((x,y))
            pixelCol = [int(r),int(g),int(b)]
            pixelCol.sort()
            pixColMinus = pixelCol[2] - pixelCol[0]
            if pixColMinus > maxColorScatter:    #it is find max scatter,now use average scatter
               maxColorScatter = pixColMinus
            avrColorScatter += pixColMinus
    avrColorScatter = avrColorScatter/(width*height)
    return avrColoScatter,maxColorScatter
        
#if picpath is directory,get all pictures.
def getPicFiles(dirPath):
    pics = []
    for root,dirs,files in os.walk(dirPath):
        for f in files:
            if f.split(".")[-1].lower() in ["bmp","jpg","jpeg","png","tiff"]:
                pics.append(os.path.join(root,f))
    return pics

#try to delete temp file
def tryDelPic(url):
    try:
        os.remove(resizePicPath)
    except:
        print(resizePicPath + " delete failed!")

#judge pic is gray or not
def isGrayPic(picpath,scatterSize = 0):
    if scatterSize < 0 or scatterSize > 255:
        return "wrong scatterSize"
    #when path is file,return bool
    if os.path.isfile(picpath):
        avrScatter,maxScatter = get_color_Scatter(PicPath)
        if avrScatter > scatterSize or maxScatter > scatterSize:
            return False
        else:
            return True
    else:
        return "wrong file"
        
        
