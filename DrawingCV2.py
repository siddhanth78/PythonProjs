import cv2 
import numpy as np 
import mediapipe as mp
import time
import math
import pyautogui
import keyboard

mp_hands = mp.solutions.hands
hands_model = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

figs = []

state = 'pen up'
fincol = (0,0,0)
currcol = [255,255,255]

capture = cv2.VideoCapture(0)

size = pyautogui.size()

screenx = size.width
screeny = size.height

penup_pos = (int(0.01 * screenx), int(0.05 * screeny))
pendown_pos = (int(0.2 * screenx), int(0.05 * screeny))
clear_pos = (int(0.4 * screenx), int(0.05 * screeny))
line_pos = (int(0.6 * screenx), int(0.05 * screeny))
circle_pos = (int(0.8 * screenx), int(0.05 * screeny))
state_pos = (int(0.01 * screenx), int(0.1 * screeny))

penup_startx = int(0.01 * screenx)
penup_endx = int(0.075 * screenx)

penup_checkx_s = int(screenx * 0.9)
penup_checkx_e = int(screenx * 0.95)

pendown_startx = int(0.2 * screenx)
pendown_endx = int(0.28 * screenx)

pendown_checkx_s = int(screenx * 0.7)
pendown_checkx_e = int(screenx * 0.8)

clear_startx = int(0.4 * screenx)
clear_endx = int(0.45 * screenx)

clear_checkx_s = int(screenx * 0.55)
clear_checkx_e = int(screenx * 0.65)

line_startx = int(0.6 * screenx)
line_endx = int(0.65 * screenx)

line_checkx_s = int(screenx * 0.37)
line_checkx_e = int(screenx * 0.42)

circle_startx = int(0.8 * screenx)
circle_endx = int(0.85 * screenx)

circle_checkx_s = int(screenx * 0.15)
circle_checkx_e = int(screenx * 0.22)

buttonsy = int(0.055 * screeny)

canvas = np.array([[0,0], [0, screeny],
                   [screenx, screeny], [screenx, 0]])

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def midpoint(x1, y1, x2, y2):
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    return (mx, my)

def undo():
    if figs == []:
        pass
    else:
        figs.pop(-1)

def red():
    currcol[0] = 0
    currcol[1] = 0
    currcol[2] = 255

def green():
    currcol[0] = 0
    currcol[1] = 255
    currcol[2] = 0

def blue():
    currcol[0] = 255
    currcol[1] = 0
    currcol[2] = 0

def cyan():
    currcol[0] = 255
    currcol[1] = 255
    currcol[2] = 0

def magenta():
    currcol[0] = 255
    currcol[1] = 0
    currcol[2] = 255

def yellow():
    currcol[0] = 0
    currcol[1] = 255
    currcol[2] = 255

def white():
    currcol[0] = 255
    currcol[1] = 255
    currcol[2] = 255

keyboard.add_hotkey('u', undo, suppress=True, trigger_on_release=True)
keyboard.add_hotkey('r', red, suppress=True, trigger_on_release=True)
keyboard.add_hotkey('g', green, suppress=True, trigger_on_release=True)
keyboard.add_hotkey('b', blue, suppress=True, trigger_on_release=True)
keyboard.add_hotkey('c', cyan, suppress=True, trigger_on_release=True)
keyboard.add_hotkey('m', magenta, suppress=True, trigger_on_release=True)
keyboard.add_hotkey('y', yellow, suppress=True, trigger_on_release=True)
keyboard.add_hotkey('w', white, suppress=True, trigger_on_release=True)

while capture.isOpened():
    ret, frame = capture.read()
    if ret:
        frame = cv2.resize(frame, (screenx, screeny))

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = hands_model.process(image)
        image.flags.writeable = True

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        image = cv2.fillPoly(image, [canvas], (0,0,0))

        # GET INDEX, THUMB, AND MIDDLE
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                index_tipx = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * screenx
                index_tipy = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * screeny

                thumb_tipx = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * screenx
                thumb_tipy = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * screeny

                middle_tipx = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * screenx
                middle_tipy = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * screeny
        else:
            index_tipx, index_tipy, thumb_tipx, thumb_tipy,middle_tipx, middle_tipy = 0,0,0,0,0,0

        point_dist_it = distance(index_tipx, index_tipy, thumb_tipx, thumb_tipy)
        point_dist_im = distance(index_tipx, index_tipy, middle_tipx, middle_tipy)

        ccol = (currcol[0],currcol[1],currcol[2])

        # POINTERS
        if state == 'pen down':
            mx, my = midpoint(index_tipx, index_tipy, thumb_tipx, thumb_tipy)
            image = cv2.circle(image, (int(mx), int(my)), 5, ccol, 5)
            
        if state == 'line start':
            mx, my = midpoint(index_tipx, index_tipy, thumb_tipx, thumb_tipy)
            image = cv2.circle(image, (int(mx), int(my)), 5, ccol, 5)

        if state == 'circle start':
            mx, my = midpoint(index_tipx, index_tipy, thumb_tipx, thumb_tipy)
            image = cv2.circle(image, (int(mx), int(my)), 5, ccol, 5)

        # PEN DOWN
        if 10 <= point_dist_it <= 70 and state == 'pen down':
            mx, my = midpoint(index_tipx, index_tipy, thumb_tipx, thumb_tipy)
            figs.append(('p',(int(mx), int(my)),ccol))

        # LINE
        if 10 <= point_dist_it <= 90 and state == 'line start':
            mx, my = midpoint(index_tipx, index_tipy, thumb_tipx, thumb_tipy)
            linep1 = (int(mx), int(my))
            state = 'line draw'

        if 10 <= point_dist_it <= 90 and state == 'line draw':
            mx, my = midpoint(index_tipx, index_tipy, thumb_tipx, thumb_tipy)
            linep2 = (int(mx), int(my))
            image = cv2.line(image, linep1, linep2, ccol, 3)
            image = cv2.circle(image, (int(mx), int(my)), 5, ccol, 5)

        if point_dist_it > 90 and state == 'line draw':
            figs.append(('l',(linep1, linep2),ccol))
            state = 'line start'

        # CIRCLE
        if 10 <= point_dist_it <= 90 and state == 'circle start':
            mx, my = midpoint(index_tipx, index_tipy, thumb_tipx, thumb_tipy)
            cc = (int(mx), int(my))
            state = 'circle draw'

        if 10 <= point_dist_it <= 90 and state == 'circle draw':
            mx, my = midpoint(index_tipx, index_tipy, thumb_tipx, thumb_tipy)
            co = (int(mx), int(my))
            rad = int(distance(cc[0], cc[1], co[0], co[1]))
            image = cv2.circle(image, cc, rad, ccol, 3)

        if point_dist_it > 90 and state == 'circle draw':
            figs.append(('c',(cc, rad),ccol))
            state = 'circle start'

        # CHECK POS
        if (60 <= point_dist_im <= 110) and (penup_checkx_s <= index_tipx <= penup_checkx_e) and (55 <= index_tipy <= 130):
            state = 'pen up'
            fincol = (0,0,0)

        if (60 <= point_dist_im <= 110) and (pendown_checkx_s <= index_tipx <= pendown_checkx_e) and (55 <= index_tipy <= 130):
            state = 'pen down'
            fincol = (255,255,255)

        if (60 <= point_dist_im <= 110) and (clear_checkx_s <= index_tipx <= clear_checkx_e) and (55 <= index_tipy <= 130):
            figs.clear()

        if (60 <= point_dist_im <= 110) and (line_checkx_s <= index_tipx <= line_checkx_e) and (55 <= index_tipy <= 130):
            state = 'line start'
            fincol = (255,255,255)

        if (60 <= point_dist_im <= 110) and (circle_checkx_s <= index_tipx <= circle_checkx_e) and (55 <= index_tipy <= 130):
            state = 'circle start'
            fincol = (255,255,255)

        # DRAW
        image = cv2.circle(image, (int(index_tipx), int(index_tipy)), 5, fincol, 5)
        image = cv2.circle(image, (int(thumb_tipx), int(thumb_tipy)), 5, fincol, 5)
        image = cv2.circle(image, (int(middle_tipx), int(middle_tipy)), 5, fincol, 5)

        
        for f in figs:
            if f[0] == 'p':
                image = cv2.circle(image, (f[1][0], f[1][1]), 3, f[2], 3)
            elif f[0] == 'l':
                image = cv2.line(image, f[1][0], f[1][1], f[2], 3)
            elif f[0] == 'c':
                image = cv2.circle(image, f[1][0], f[1][1], f[2], 3)

        flip_image = cv2.flip(image,1)

        flip_image = cv2.line(flip_image, (penup_startx, buttonsy), (penup_endx, buttonsy), (255, 0, 0), 3)
        flip_image = cv2.line(flip_image, (pendown_startx, buttonsy), (pendown_endx, buttonsy), (255, 0, 0), 3)
        flip_image = cv2.line(flip_image, (clear_startx, buttonsy), (clear_endx, buttonsy), (255, 0, 0), 3)
        flip_image = cv2.line(flip_image, (line_startx, buttonsy), (line_endx, buttonsy), (255, 0, 0), 3)
        flip_image = cv2.line(flip_image, (circle_startx, buttonsy), (circle_endx, buttonsy), (255, 0, 0), 3)

        # TEXT
        #cv2.putText(flip_image, f'{penup_startx:.2f}, {penup_endx:.2f}', (10, 160), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(flip_image, f'State: {state}', state_pos, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(flip_image, 'pen up', penup_pos, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(flip_image, 'pen down', pendown_pos, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(flip_image, 'clear all', clear_pos, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(flip_image, 'line', line_pos, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(flip_image, 'circle', circle_pos, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Hand Landmarks", flip_image)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
    else:
        break

capture.release()
cv2.destroyAllWindows()