import cv2
import pandas as pd
import streamlit as st

img_path = r'colorful.jpeg'
img = cv2.imread(img_path)

def rescaleFrame(frame, scale = 0.75):
    height = int(frame.shape[0] * scale + 0.5)
    width = int(frame.shape[1] * scale)
    dimenssions = (width,height)
    return cv2.resize(frame,dimenssions,interpolation=cv2.INTER_AREA)

img = rescaleFrame(img,scale=1)

index = ["color", "color_name", "HEX code", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

csv.drop("color",axis=1,inplace=True)
def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)