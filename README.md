# Ball_Balance
Balancing a ball on a 1 DOF platform using OpenCV,python and arduino

# DEMO: https://www.youtube.com/watch?v=ZzTRvkJum4c <br />

I used Arduino to control the servo motor. <br />
The video from the webcam is processed in the laptop using OpenCV and python. <br />
The relative position of the ball from the center position is tracked and is accordingly fed into the PID algorithm and then a signal is sent to Arduino over the serial port to move the servo to prevent the ball from falling. <br />
