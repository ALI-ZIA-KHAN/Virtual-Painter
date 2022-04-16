import cv2
import numpy as np
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set (4, frameHeight)
cap.set(10,240)
# 98,179,151,253,0,190



# myColors = [[102,169,122,245,59,255],
#             [133,56,8,159,156, 255],
#             [57,76,0,180, 255, 255]]
# def findcolor(img,myColors):
#     imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
#     lower = np.array(myColors[0][0:3])
#     upper = np.array(myColors[0][3:6])
#     mask =cv2.inRange(imgHSV,lower,upper)
#     cv2.imshow("img",mask)

myColors = [
             [100,150,0,140,255,255],
            [102,169,122,245,59,255],
            [133,56,8,159,156, 255],
            [57,76,0,100, 255,255]]
#bgr
myColorValues=[[255,0,0],
               [0,0,0],
               [200,63,100],
               [121,20,0]]
#(0,0,255)(0,0,0)

myPoints=[]
def findColor(img,myColors,myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count=0
    newPoints=[]
    for color in myColors:
        lower =np.array(color[0:3])
        upper =np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y=getContours(mask)
        if x !=0 and y!= 0:
           newPoints.append([x, y,count])
        cv2.circle(imgResult, (x, y), 10,myColorValues[count],cv2.FILLED)
        count+=1
        # getContours(mask)
        # cv2.imshow(str(color[0]),mask)
    return  newPoints
def getContours(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
       area = cv2.contourArea(cnt)
       if(area>500):
        # cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)
        peri=cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt,0.02 * peri, True)
        #bounding box around shapes
        x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y

def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10,myColorValues[point[2]],cv2.FILLED)



while True:
    success,img = cap.read()
    imgResult=img.copy()
    newPoints=findColor(img,myColors,myColorValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints) != 0:
        drawOnCanvas(myPoints,myColorValues)

    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & 0XFF == ord('q'):
      break