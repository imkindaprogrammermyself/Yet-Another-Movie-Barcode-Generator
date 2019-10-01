import cv2
import numpy as np

file = "video.mp4"
cap = cv2.VideoCapture(file)
filename = file.split('.')
fcount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
duration = fcount/fps
print("FPS: %s, COUNT %s, DURATION %s" %(fps,fcount,duration))

image = np.zeros((500, int(duration) + 1, 3), np.uint8)

frames = []
imagecolumn = 0
framesprocessed = 0
framesremain = fcount % fps

while True:
    flag,frame = cap.read()
    if flag:
        avg_color_per_row = np.average(frame, axis=0)
        avg_colors = np.average(avg_color_per_row, axis=0)
        avg_color_int = np.array(avg_colors, dtype=np.uint8)
        frames.append(avg_color_int)
        if len(frames) == fps:
            image[:,[imagecolumn]] = np.average(frames, axis=0)
            imagecolumn += 1
            framesprocessed += fps
            print("%s/%s" %(framesprocessed,fcount))
            frames.clear()
    else:
        if framesremain > 0 and len(frames) > 0:
            image[:,[imagecolumn]] = np.average(frames, axis=0)
            framesprocessed += framesremain
            print("%s/%s" %(framesprocessed,fcount))
        cv2.imwrite(filename[0] + '.png',image)
        print("TOTAL FRAMES: %s, PROCESSED FRAMES %s" %(fcount,framesprocessed))
        cap.release()
        break