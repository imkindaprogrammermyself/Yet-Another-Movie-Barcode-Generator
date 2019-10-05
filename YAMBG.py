import cv2
import numpy as np
import time

#############################
input_file = "wildlife.mp4" #<-INPUT FILENAME
output_image_height = 500   #<-OUTPUT IMAGE HEIGHT
width_scale = 20            #<-USEFUL WHEN INPUT VIDEO DURATION IS SHORT
#############################

file_name = input_file.split('.')[0]
cap = cv2.VideoCapture(input_file)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frames_per_second = int(cap.get(cv2.CAP_PROP_FPS))
duration = frame_count / frames_per_second
print("FPS: %s, FRAME COUNT: %s" % (frames_per_second,frame_count))

image = np.zeros((output_image_height, (int(duration) + 1) * width_scale, 3), np.uint8)
avg_color_per_frame = []
color_column_index = 0
frames_processed = 0
frames_remain = frame_count % frames_per_second

def append_to_image():
    average_color = np.average(avg_color_per_frame, axis=0)
    image[:,color_column_index:color_column_index + width_scale] = np.round(average_color)
    avg_color_per_frame.clear()

while True:
    flag,frame = cap.read()
    if flag:
        avg_color_per_row = np.average(frame, axis=0)
        avg_colors = np.average(avg_color_per_row, axis=0)
        avg_color_int = np.array(avg_colors, dtype=np.uint8)
        avg_color_per_frame.append(avg_color_int)
        if len(avg_color_per_frame) == frames_per_second:
            append_to_image()
            color_column_index += 1 * width_scale
            frames_processed += frames_per_second
            print("PROGRESS: %s/%s" % (frames_processed,frame_count))
    else:
        if frames_remain > 0 and len(avg_color_per_frame) > 0:
            append_to_image()
            frames_processed += frames_remain
            print("PROGRESS: %s/%s" % (frames_processed,frame_count))
        cv2.imwrite(file_name + '.png',image)
        print("PROCESSED FRAMES: %s, TOTAL FRAMES %s" % (frames_processed,frame_count))
        cap.release()
        break