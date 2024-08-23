import cv2
import numpy as np
import pyautogui

#display screen resolution, get it using pyautogui itself.
SCREEN_SIZE=tuple(pyautogui.size())

#define the codec
fourcc = cv2.VideoWriter_fourcc(*"XVID")

#frames per second
fps = 12.0

#create the video write object
out = cv2.VideoWriter("output.avi", fourcc, fps, (SCREEN_SIZE))

#the time you want to record in seconds
record_seconds = 10

for i in range(int(record_seconds*fps)):
    #make a screen shot
    img = pyautogui.screenshot()

    #convert these pixels to a proper numpy array to work with opencv
    frame = np.array(img)

    #convert colours from BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #write the frame
    out.write(frame)

    #show the frame
    cv2.imshow("screenshot", frame)

    #if user clicks q it exits
    if cv2.waitKey(1) == ord("q"):
        break

#make sure everything is closed when clicking q
cv2.destroyAllWindows()
out.release()

img = pyautogui.screenshot(region=(0, 0, 300, 400))