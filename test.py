# Documentation
# This program calculates the speed of a car.
# Basic phenomenon of this program is to track an object in a particular vision until that particular object escapes that vision.
# This program needs to be manually calibrated for every particular road after that results are expected to be positive upto 95%.
# Formula : Speed = Distance/Time.

import cv2
from datetime import datetime


cap = cv2.VideoCapture(0)
start_loop = True
start_time = 0
stop_loop = False
stop_time = 0
middle_loop = False
start_arr = [0]
stop_arr = [0]
counter = 0
second_elapsed = float(0)
speed = 0

f = open("record.txt", mode='w+', encoding='utf-8')
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
out = cv2.VideoWriter("output.avi", fourcc, 4.0, (1280, 720))

ret, frame = cap.read()
ret, frame1 = cap.read()
ret, frame2 = cap.read()
# print(frame1.shape)

while cap.isOpened():

    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(
        dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if(stop_loop):
        now = datetime.now()
        stop_arr.append(now.strftime('%S.%f'))
        #counter = counter + 1
        # print("start")
        stop_loop = False
        start_loop = True
        middle_loop = True

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < 1500:
            continue

        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame1, "Movement {}".format('Detected'),
                    (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        cv2.imwrite('images.png', frame)
        if(start_loop):
            now = datetime.now()
            temp = float(now.strftime('%S.%f'))
            if(counter == 0):
                start_arr[0] = temp
                counter = counter + 1
            # print("end")
            start_loop = False
            middle_loop = False
            stop_loop = True

    #cv2.drawContours(frame1, contours, -1, (255, 255, 0), 2)

    image = cv2.resize(frame1, (1280, 720))
    out.write(image)
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()
cap.release()
out.release()
# print(start_arr)
# print(stop_arr)
last_index = (len(stop_arr)-1)
first = float(start_arr[0])
last = float(stop_arr[last_index])
second_elapsed = (last - first)
print(f"Seconds Elapsed = ", second_elapsed)
speed = 15.57/second_elapsed
speed_kmph = (speed * 3600)/1000
print(f"Speed of the vehicle : ", "%.2f" % round(speed_kmph, 2), "km/h")
