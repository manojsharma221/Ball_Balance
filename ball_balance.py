#Importing dependencies
import cv2
import numpy as np
import time
import serial
#Setting arduino board com port and baudrate
ArduinoSerial = serial.Serial('com6',115200)
time.sleep(2)
#HSV Range for orange  color 
lowerbound=np.array([0,120,40])
upperbound=np.array([12,200,255])
#Video Source(0 for WebCam)
cam= cv2.VideoCapture(0)

#PID initialisation 
desired_posn = 200#Centre of the video
kp=0.4
ki=0
kd=0.1
previous_error=0
timenow=0
pid_i=0
while True:
 #Getting image from video
 ret, img=cam.read()
 #Resizing the image to 340x220
 img=cv2.resize(img,(400,300))
 #Smoothning image using GaussianBlur
 imgblurred=cv2.GaussianBlur(img,(11,11),0)
 #Converting image to HSV format
 imgHSV=cv2.cvtColor(imgblurred,cv2.COLOR_BGR2HSV) #source:https://thecodacus.com/opencv-object-tracking-colour-detection-python/#.Wz9tQN6Wl_k
 #Masking orange color
 mask=cv2.inRange(imgHSV,lowerbound,upperbound)
 #source:https://www.pyimagesearch.com/2015/09/21/opencv-track-object-movement/
 #Removing Noise from the mask
 mask = cv2.erode(mask, None, iterations=2)
 mask = cv2.dilate(mask, None, iterations=2)
 #Extracting contour
 cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_NONE)[1]
#Drawing Contour		
 cv2.drawContours(img,cnts,-1,(255,0,0),3)
 #Processing each contour
 for c in cnts:   #source: https://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/
  # compute the center of the  maximum area contour
  m=max(cnts,key=cv2.contourArea)#finding the contour with maximum area
  M = cv2.moments(m)
  cX = int(M["m10"] / M["m00"])
  cY = int(M["m01"] / M["m00"])
 
  # draw the max area contour and center of the shape on the image
  cv2.drawContours(img, [m], -1, (0, 255, 0), 2)
  cv2.circle(img, (cX, cY), 7, (255, 255, 255), -1)
  cv2.putText(img, "center", (cX - 20, cY - 20),
   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
  #Drawing a vertical central line(at x=170) with RED color(BGR)
  cv2.line(img,(200,0),(200,300),(0,0,255),2)
  #Drawing a vertical line at the centre with Blue color
  cv2.line(img,(cX,0),(cX,300),(255,0,0),2)
  #Displaying mask
 cv2.imshow("mask",mask)
  #Displaying image
 cv2.imshow("cam",img)
  
  
  #PID calcuation
 error=(cX-desired_posn)/1.5
  #Proportional
 pid_p=kp*error
  #Integral
 if -30<error<30:
  pid_i=pid_i+(ki*error)
  #Derivative
 time_previous=timenow
 timenow=time.time()
 elapsedTime=timenow-time_previous
 pid_d=kd*((error-previous_error)/elapsedTime)
 previous_error=error
 PID=pid_p+pid_i+pid_d
 servo_signal=90+PID
  
 if servo_signal<=5:
  servo_signal=5 
 if servo_signal>=170:
  servo_signal=170 
  
 print int(servo_signal)#servo_signal is a float so converting it to integer values
 #press q to end loop
 if cv2.waitKey(1) & 0xFF == ord('q'):
       break
 #Sending servo signal value to arduino
 #Only unsigned 8 bit integer values allowed
 ArduinoSerial.write(str(chr(int(servo_signal))))
 #time.sleep(1./120)
 #print ArduinoSerial.readline()
 
 #Note: Not having any orange color to the camera will cause the loop to stop or result in different kinds of errors
 #
  
 

