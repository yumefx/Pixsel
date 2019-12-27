#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/12/27 12:08
# @Author : yumefx
# @File : isGrayPic.py

import os
from PIL import Image

#
def changeSize(url,resizeDir = "",resizeDirect = "y",resizePixel = 250):
    img = Image.open(url)
	width = img.size[0]
	height = img.size[1]
	imgName = os.path.basename(url)
	if resizeDir == "":
	    newpath = os.path.join(os.path.dirname(url),"resize_" + imgName)
	else:
	    newpath = os.path.join(resizeDir,"resize_" + os.path.basename(url))
	if resizeDirect == "y":
		img.resize((int(width/(height/resizePixel)),resizePixel)).save(newpath)
	else:
	    img.resize((resizePixel,int(height/(width/resizePixel)))).save(newpath)
	return newpath
	
def get_color_Scatter(url):
	img = Image.open(url)
	pix = im.convert("RGB")
	width = img.size[0]
	height = img.size[1]
	maxColorScatter = 0
	for x in range(width):
	    for y in range(height):
			r,g,b = pix.getpixel((x,y))
			pixelCol = [int(r),int(g),int(b)]
			pixelCol.sort()
			if pixelCol[2] - pixelCol[0] > maxColorScatter:
				maxColorScatter = pixelCol[2] - pixelCol[0]
	try:
		os.remove(url)
	except:
	    print(url + " delete failed!")
		
def getPicFiles(dirPath):
    pics = []
	for root,files,dirs in os.walk(dirPath):
		for f in files:
		    if f.split(".")[-1].lower() in ["bmp","jpg","jpeg","png","tiff"]:
				pics.append(os.path.join(root,f))
	return pics

def isGrayPic(picpath,scatterSize=0,resizePath = "",resizeType = "y",resizeLenth = 250):
	if not scatterSize in range(256):
		return "wrong scatterSize"
	if not os.path.isdir(resizePath):
	    os.mkdir(resizePath)
	if not resizeType in ["x","y"]:
	    return "wrong resizeType"
	if type(resizeLenth) != int:
		return "wrong resizeLenth type"
	if resizeLenth <= 0 :
	    return "wrong resizeLenth"
    if os.path.isfile(picpath):
		resizePicPath = changeSize(picpath,resizeDir = resizePath,resizeDirect = resizeType,resizePixel = resizeLenth) 
		if get_color_Scatter(resizePicPath) > scatterSize:
			return False
		else:
		    return True
	elif os.path.isdir(picpath):
	    picScatters = {}
		picfiles = getPicFiles(picpath)
		for pf in picfiles:
			picScatters[pf] = get_color_Scatter(changeSize(pf,resizeDir = resizePath,resizeDirect = resizeType,resizePixel = resizeLenth))
		return picScatters
		
	else:
	    return "wrong path"