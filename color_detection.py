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

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:

    cv2.imshow("image", img)
    if clicked:
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        clicked = False
    if cv2.waitKey(20) & 0xFF == 8:
        break
cv2.destroyAllWindows()