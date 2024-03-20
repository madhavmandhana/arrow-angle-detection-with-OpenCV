import cv2
import numpy as np
import math
from math import pi as PI

def getAng(a, b, c): #a = [1,2]

    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang

def findit(approx):
    yo = approx.copy()
    
    #appending duplicates for future problems
    yo.append(yo[0])
    yo.append(yo[1])
    yo.append(yo[2])
    yo.append(yo[3])
    ans={}

    #loop for all angles
    for i in range(0,7,1):
         ang = getAng(yo[i][0],yo[i+1][0],yo[i+2][0]) 
         if i == 6:
             j= 0
         else:
             j = i+1
         ans[j] = ang
    temp = max(ans.values())
    res = [key for key in ans if ans[key] == temp]

    if res[0]>=3:
        one = res[0]
        two = res[0]-4
        three = res[0] -3
    else:
        one = res[0]
        two = res[0]+3
        three = res[0] +4

    return one,two,three

def empty(a):
    pass

def getcont(img,imgcnt):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area= cv2.contourArea(cnt)
        if area>1180:
            cv2.drawContours(imgcnt,cnt, -1,(0,255,255),7)
            perimeter = cv2.arcLength(cnt,True)
            approx=  cv2.approxPolyDP(cnt,0.02*perimeter,True)
            if len(approx) == 7:

                mp,sp,dp = findit(approx.tolist())
                vertex_x,vertex_y = approx[mp][0]
                other_x,other_y = (approx[sp][0] + approx[dp][0])/2
              
                try:
                    m= (other_y - vertex_y) /(other_x - vertex_x)
                except ZeroDivisionError:
                    m = (other_y - vertex_y) /(other_x - vertex_x + 0.001)
                  
                PI = 3.14159265
              
                myatan = lambda x,y: np.pi*(1.0-0.5*(1+np.sign(x))*(1-np.sign(y**2))\
                -0.25*(2+np.sign(x))*np.sign(y))\
                -np.sign(x*y)*np.arctan((np.abs(x)-np.abs(y))/(np.abs(x)+np.abs(y)))
              
                angle = np.arctan(m)
                angle = (angle * 180) / PI
                if angle <0:
                    angle = 180 -abs(angle)

                angle = round(angle,2)
                
                cv2.rectangle(imageContour,(5,0),(190,30),(0,0,0),-1)
                cv2.putText(imageContour,"Angle : " + str(angle),(10,20),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2)

# ---------------- END-----------


#Main Program

cap= cv2.VideoCapture(0)
while True:
    _, frame =  cap.read() 
    imageContour = frame.copy()


    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lower_red = np.array([140,80,80])
    upper_red = np.array([255,200,255])
    mask = cv2.inRange(hsv,lower_red,upper_red) #filtering out red color objects using a range
    kernel = np.ones((5,5),np.uint8) #declaring kernel for erosion,dilation,morphology
    
    erosion = cv2.erode(mask,kernel,iterations=1) #using erosion to reduce noise

    edges = cv2.Canny(frame,160,154) #getting the edges
    getcont(erosion,imageContour) #Finally runnng the main funcn to get corners,plot the arrow and put angle on image as text



    #SHOWING FRAMES
    cv2.imshow('cont',imageContour)


    k = cv2.waitKey(1)
    if k==48:
        break



cv2.destroyAllWindows()
cap.release()
