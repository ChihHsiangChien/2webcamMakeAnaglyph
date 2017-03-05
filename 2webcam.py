#!/usr/bin/env python
#-*- coding: utf-8 -*-

# open camera 0, 1
import cv2
import numpy as np
import time

cameraCapture0 = cv2.VideoCapture(0)
cameraCapture1 = cv2.VideoCapture(1)

width = int(cameraCapture0.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cameraCapture0.get(cv2.CAP_PROP_FRAME_HEIGHT))
size = (height,width,3)
fps = 15




cyan = np.zeros((size),dtype = np.float32)
cyan[:,:,0:2]=255

red = np.zeros((size),dtype = np.float32)
red[:,:,2]=255


success0, frame0 = cameraCapture0.read()
success1, frame1 = cameraCapture1.read()


#捕捉滑鼠，按左鍵就開始錄製影片
#設定影片寫入的檔名與格式
videoWriter = cv2.VideoWriter(time.strftime("%Y%m%d-%H-%M-%S")+".avi",cv2.VideoWriter_fourcc('X','V','I','D'),fps,(width,height))


clicked = False
def onMouse(event, x, y, flage, param):
    global clicked
    if event == cv2.EVENT_LBUTTONUP:
        if clicked == True:
            clicked = False
        if clicked == False:
            clicked = True


cv2.namedWindow('combine')
cv2.setMouseCallback('combine', onMouse)


print(success0,success1)

while (success0 or success1) and cv2.waitKey(1) == -1 :# 1ms delay
    if success0:
        #cv2.imshow("L",frame0)
        success0, frame0 = cameraCapture0.read()
    if success1:
        #cv2.imshow("R",frame1)
        success1, frame1 = cameraCapture1.read()
    
    
    #screen cyan and frame0,make left image
    frame0 = np.float32(frame0)
    left = 255-(255-cyan)*(255-frame0)/255
    left = np.uint8(left)

    #screen red and frame1,make right image
    frame1 = np.float32(frame1)
    right = 255 -(255-red)*(255-frame1)/255
    right = np.uint8(right)
    
    #cv2.imshow('left',left)
    #cv2.imshow('right',right)

    left=np.float32(left)
    right=np.float32(right)
    #multiply two layer
    frameAll = (left * right)/255
    frameAll =np.uint8(frameAll)
    cv2.imshow('combine',frameAll)
    
    #錄製影片
    if clicked:
        videoWriter.write(frameAll)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.waitKey(0)
cv2.destroyAllWindows()




