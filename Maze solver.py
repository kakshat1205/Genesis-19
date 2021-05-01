import cv2
import numpy as np
import serial
import time

points=[]
c=[]
p=0

pen=serial.Serial('com6',9600) # intializes the serial communication between your python script and arduino

def send(x,y):  # send(x,y) sends the coordinate to the arduino through pyserial

    s=str(x)+' '+str(y)+'\n'
    pen.flush()
    pen.write(s.encode())
    time.sleep(1)

send(-11.7,22)
time.sleep(5)

frame = cv2.imread('mazef3.jpeg')   
frame=cv2.resize(frame,(900,900),interpolation=cv2.INTER_AREA)
cv2.imshow("sck",frame)

def nothing(x):
    pass

cv2.namedWindow("Tracking")

cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LS", "Tracking", 141, 255, nothing)
cv2.createTrackbar("LV", "Tracking", 98, 255, nothing)
cv2.createTrackbar("UH", "Tracking", 255, 255, nothing)
cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)
# These functions create the trackbar we would later use to 
#determine the range of colours we want to extract from the image


hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)#changes the image from BGR to HSV format


while True:
    l_h = cv2.getTrackbarPos("LH", "Tracking")
    l_s = cv2.getTrackbarPos("LS", "Tracking")
    l_v = cv2.getTrackbarPos("LV", "Tracking")

    u_h = cv2.getTrackbarPos("UH", "Tracking")
    u_s = cv2.getTrackbarPos("US", "Tracking")
    u_v = cv2.getTrackbarPos("UV", "Tracking")

    l_r = np.array([l_h, l_s, l_v])
    u_r = np.array([u_h, u_s, u_v])
    #creates an array which stores the range of values for colour
    mask = cv2.inRange(hsv, l_r, u_r)
    # masking operation carried out
    
    res = cv2.bitwise_and(frame, frame, mask=mask)
    #performs the and operation to extract red dots and display it 
    cv2.imshow("res", res)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()

# thresholding
bgr = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5),0)
ret, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)
#into perfect black and white
#finding red dots

kernel = np.ones((5, 5), np.uint8)
erosion = cv2.erode(thresh, kernel, iterations=1) 
contours, _ = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(len(contours))
imc=cv2.drawContours(res,contours,-1,(0,255,0),5)
cv2.imshow("imc",imc) 
for i in range(len(contours) - 1):
        (x,y),radius = cv2.minEnclosingCircle(contours[i+1])
        #finds the centre of the red dots 
        x=int(x)
        y=int(y)
        #stores it in a list we have created
        c.append([x,y])
               

c = np.float32(c) 
print(c)
crop = np.float32([[0,0],[600,0],[0,600],[600,600]]) #this is the final orientation we want our
#perspective transform to return
M = cv2.getPerspectiveTransform(c, crop) #finds the transformation matrix
img = cv2.warpPerspective(frame, M, (600, 600))
cv2.imshow("img",img)


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
kernel = np.ones((2, 2), np.uint8)
dilate = cv2.dilate(thresh, kernel, iterations=3)

contours, _ = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
imc=cv2.drawContours(img,contours,4,(0,255,0),5)
cv2.imshow("cnt",imc)

drawing1 = np.zeros(thresh.shape, np.uint8)
drawing2 = np.zeros(thresh.shape, np.uint8)

print(len(contours))
# Drawing contour[0],in drawing 1
draw1=cv2.drawContours(drawing2, contours, 2, (255, 255, 255), -1)
# Drawing contour[1],in drawing 2
draw2=cv2.drawContours(drawing1, contours, 3, (255, 255, 255), -1)
cv2.imshow("imc1",draw1)
cv2.imshow("imc2",draw2)
dilate_mask = np.ones((19, 19), np.uint8)

dilate1 = cv2.dilate(drawing1, dilate_mask, iterations=4)
dilate2 = cv2.dilate(drawing2, dilate_mask, iterations=4)
#dilating both halves of the contours to overlap 
path = cv2.bitwise_and(dilate1, dilate2)
#the part of contours which overlap is the path for our maze

cv2.imshow("path",path)
kernel = np.ones((2, 2), np.uint8)
erosion = cv2.erode(path, kernel, iterations=10)
cnts, _ = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

print(len(cnts))
l = len(cnts[0])    #finds how many contour points are defining the path

l /= 2 # takes first half of the points as that
#defines one half of the path
l = int(l)
for i in range(0, l,20):  #this for loop takes txhe the 20th contour point
    a = cnts[0][i]
    (x, y) = (a[0][0], a[0][1]) # the current x and y coordinate of point
                                #we are sending
    points.append((x,y)) # we store all the points we get into the list

for i in range(len(points)):            
    (x,y)=points[i]
    cv2.circle(thresh, (x, y), 1, (255, 255, 255), -1) 
    cv2.imshow("result",thresh)
    cv2.waitKey(0)
    if(p==0):
        time.sleep(5)
    p+=1
    print(x,y)
    send(x,y)
