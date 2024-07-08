import cv2 
import numpy as np 
import mediapipe as mp
import time
import math
import pyautogui
import keyboard
import os

mp_hands = mp.solutions.hands
hands_model = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

figs = []

state = 'none'
currstate = state
fincol = (0,0,0)
currcol = [255,255,255]

count = 0
dots = 0

currdir = os.getcwd()

capture = cv2.VideoCapture(0)

size = pyautogui.size()

screenx = size.width
screeny = size.height

index_pos = (int(0.01 * screenx), int(0.75 * screeny))
thumb_pos = (int(0.01 * screenx), int(0.8 * screeny))
middle_pos = (int(0.01 * screenx), int(0.85 * screeny))
it_pos = (int(0.01 * screenx), int(0.9 * screeny))
im_pos = (int(0.01 * screenx), int(0.95 * screeny))

angle_pos = (int(0.01 * screenx), int(0.7 * screeny))

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
    
def drawFigs(figs, image):
    fig_arr = np.array(figs)
        
    for i in range(len(fig_arr)):
        if fig_arr[i][0] == 'p':
            for j in range(len(fig_arr[i][1])):
                image = cv2.circle(image, (fig_arr[i][1][j][0][0], fig_arr[i][1][j][0][1]), 3, fig_arr[i][1][j][1], -1)
                if j+1 < len(fig_arr[i][1]):
                    image = cv2.line(image, (fig_arr[i][1][j][0][0], fig_arr[i][1][j][0][1]),
                                        (fig_arr[i][1][j+1][0][0], fig_arr[i][1][j+1][0][1]), fig_arr[i][1][j][1], 3)
        elif fig_arr[i][0] == 'l':
            image = cv2.line(image, fig_arr[i][1][0], fig_arr[i][1][1], fig_arr[i][2], 3)
        elif fig_arr[i][0] == 'c':
            image = cv2.circle(image, fig_arr[i][1][0], fig_arr[i][1][1], fig_arr[i][2], 3)
                
    figs = fig_arr.tolist()
    
    return figs, image
    
import math

def getSlope(x1, y1, x2, y2):
    if x1 == x2:
        x1 = x2+1
        y2 = y1
    slope = (y2 - y1) / (x2 - x1)
    return slope

def getAngle(m1, m2):
    
    tan_theta = (m1 - m2) / (1 + m1 * m2)

    theta_radians = math.atan(tan_theta)

    theta_degrees = math.degrees(theta_radians)
    
    if theta_degrees < 0:
        theta_degrees += 180
    
    return theta_degrees

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

        #image = cv2.fillPoly(image, [canvas], (0,0,0))

        # GET INDEX, THUMB, AND MIDDLE
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                index_tipx = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * screenx
                index_tipy = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * screeny
                
                index_mcpx = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x * screenx
                index_mcpy = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y * screeny

                thumb_tipx = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * screenx
                thumb_tipy = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * screeny
                
                thumb_mcpx = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].x * screenx
                thumb_mcpy = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y * screeny

                middle_tipx = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * screenx
                middle_tipy = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * screeny
        else:
            index_tipx, index_tipy, index_mcpx, index_mcpy, thumb_tipx, thumb_tipy, thumb_mcpx, thumb_mcpy, middle_tipx, middle_tipy = 0,0,0,0,0,0,0,0,0,0

        m1 = getSlope(thumb_tipx, thumb_tipy, thumb_mcpx, thumb_mcpy)
        m2 = getSlope(index_tipx, index_tipy, thumb_mcpx, thumb_mcpy)
        theta_deg = getAngle(m1, m2)
        
        m3 = getSlope(middle_tipx, middle_tipy, index_mcpx, index_mcpy)
        m4 = getSlope(index_tipx, index_tipy, index_mcpx, index_mcpy)
        theta_deg_2 = getAngle(m3, m4)
        theta_deg_2 = 180 - theta_deg_2

        ccol = (currcol[0],currcol[1],currcol[2])
        
        mx, my = midpoint(index_tipx, index_tipy, thumb_tipx, thumb_tipy)
        mx, my = int(mx), int(my)
        
        # MODES
        if state == 'none':
            if 85 <= theta_deg <= 95 and theta_deg_2 > 130:
                state = 'line? [ ]'
                dots, count = 0, 0
            elif 85 <= theta_deg <= 95 and theta_deg_2 <= 20:
                state = 'circle? [ ]'
                dots, count = 0, 0
            elif 1 <= theta_deg <= 10:
                state = 'pen? [ ]'
                dots, count = 0, 0
        
        # SWITCH TO LINE
        if ('line?' in state) and 85 <= theta_deg <= 95 and theta_deg_2 > 130:
            count += 1
            if count%30 == 0:
                dots += 1
            state = 'line? [' + '*'*dots + ' '*(1-dots) + ']'
            if dots >= 2:
                state = 'line'
                currstate = 'line'
                
        if ('line?' in state) and (theta_deg < 85 or theta_deg > 95):
            if dots < 2:
                state = currstate
                
        # SWITCH TO CIRCLE
        if ('circle?' in state) and 85 <= theta_deg <= 95 and theta_deg_2 <= 20:
            count += 1
            if count%30 == 0:
                dots += 1
            state = 'circle? [' + '*'*dots + ' '*(1-dots) + ']'
            if dots >= 2:
                state = 'circle [ ]'
                currstate = 'circle'
                count, dots = 0, 0
                
        if ('circle?' in state) and (theta_deg < 85 or theta_deg > 95):
            if dots < 2:
                state = currstate
                
        if ('circle [' in state):
            count += 1
            if count%30 == 0:
                dots += 1
            state = 'circle [' + '*'*dots + ' '*(1-dots) + ']'
            if dots >= 2:
                state = 'circle'
        
        # SWITCH TO PEN
        if ('pen?' in state) and 1 <= theta_deg <= 10:
            count += 1
            if count%30 == 0:
                dots += 1
            state = 'pen? [' + '*'*dots + ' '*(1-dots) + ']'
            if dots >= 2:
                state = 'pen [ ]'
                currstate = 'pen'
                count, dots = 0, 0
                
        if ('pen?' in state) and theta_deg > 10:
            if dots < 2:
                state = currstate
                
        if ('pen [' in state):
            count += 1
            if count%30 == 0:
                dots += 1
            state = 'pen [' + '*'*dots + ' '*(1-dots) + ']'
            if dots >= 2:
                state = 'pen'
        
        # SWITCH TO NONE
        if ('none' not in state) and ('circle?' not in state) and theta_deg_2 <= 20 and 85 <= theta_deg <= 95:
            state = 'none? [  ]'
            dots, count, mflag = 0, 0, 0
                
        if ('none?' in state) and theta_deg_2 <= 20 and 1 <= theta_deg <= 20:
            mflag = 1
            count += 1
            if count%30 == 0:
                dots += 1
            state = 'none? [' + '*'*dots + ' '*(1-dots) + ']'
            if dots >= 2:
                state = 'none'
                currstate = 'none'
                
        if ('none?' in state) and theta_deg > 20 and mflag == 1:
            if dots < 2:
                state = currstate
                
        # POINTERS
        if state == 'pen':
            image = cv2.circle(image, (mx, my), 5, ccol, 5)
            
        if state == 'line':
            image = cv2.circle(image, (mx, my), 5, ccol, 5)

        if state == 'circle':
            image = cv2.circle(image, (mx, my), 5, ccol, 5)

        # PEN
        if 1 <= theta_deg <= 20 and state == 'pen':
            state = 'pen start'
            pen_arr = []
        
        if state == 'pen start':
            pen_arr.append(((mx, my),ccol))
            
        if (theta_deg > 20) and state == 'pen start':
            figs.append(('p', pen_arr))
            state = 'pen'

        # LINE
        if 1 <= theta_deg <= 10 and state == 'line':
            linep1 = (mx, my)
            state = 'line draw'

        if state == 'line draw':
            linep2 = (mx, my)
            image = cv2.line(image, linep1, linep2, ccol, 3)
            image = cv2.circle(image, (mx, my), 5, ccol, 5)

        if theta_deg > 10 and theta_deg < 150 and state == 'line draw':
            figs.append(('l',(linep1, linep2),ccol))
            state = 'line'

        # CIRCLE
        if 1 <= theta_deg <= 10 and state == 'circle':
            cc = (mx, my)
            state = 'circle draw'

        if state == 'circle draw':
            co = (mx, my)
            rad = int(distance(cc[0], cc[1], co[0], co[1]))
            image = cv2.circle(image, cc, rad, ccol, 3)

        if theta_deg > 10 and state == 'circle draw':
            figs.append(('c',(cc, rad),ccol))
            state = 'circle'

        # DRAW
        #image = cv2.circle(image, (int(index_tipx), int(index_tipy)), 5, fincol, 5)
        #image = cv2.circle(image, (int(thumb_tipx), int(thumb_tipy)), 5, fincol, 5)
        #image = cv2.circle(image, (int(middle_tipx), int(middle_tipy)), 5, fincol, 5)
        
        #image = cv2.line(image, (int(index_tipx), int(index_tipy)), (int(thumb_mcpx), int(thumb_mcpy)), fincol, 5)
        #image = cv2.line(image, (int(thumb_tipx), int(thumb_tipy)), (int(thumb_mcpx), int(thumb_mcpy)), fincol, 5)
        
        figs, image = drawFigs(figs, image)

        flip_image = cv2.flip(image,1)

        # TEXT
        cv2.putText(flip_image, f'Angle: {theta_deg:.2f}, {theta_deg_2:.2f}', angle_pos, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(flip_image, f'Index: {index_tipx:.2f}, {index_tipy:.2f}', index_pos, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(flip_image, f'Thumb: {thumb_tipx:.2f}, {thumb_tipy:.2f}', thumb_pos, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(flip_image, f'Middle: {middle_tipx:.2f}, {middle_tipy:.2f}', middle_pos, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(flip_image, f'State: {state}', (screenx-int(middle_tipx), int(middle_tipy)-20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("DrawingCV2", flip_image)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
    else:
        break

capture.release()
cv2.destroyAllWindows()