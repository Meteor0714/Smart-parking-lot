import cv2
import sys
file = "C:/Users/Andrew/Desktop/yolov7-main/utils/firebase/123.txt"
fo = open(file, mode='r')
str = fo.readline()
print(str)

cap = cv2.VideoCapture(0)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
assert cap.isOpened(), f'Failed to open {0}'
f = 0 #連線失敗攝影機數
s = 0 #成功連線攝影機數
print(f"Load Multi Cam W={w}  H={h}")
print(f"Success {s} Failed {f}")