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

#figs = []

capture = cv2.VideoCapture(0)

size = pyautogui.size()

screenx = size.width
screeny = size.height

cx = screenx/2
cy = screeny/2

state_pos = (int(0.01 * screenx), int(0.1 * screeny))

state = 'free'

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def midpoint(x1, y1, x2, y2):
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    return (mx, my)

while capture.isOpened():
    ret, frame = capture.read()
    if ret:
        frame = cv2.resize(frame, (screenx, screeny))

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = hands_model.process(image)
        image.flags.writeable = True

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # GET INDEX, THUMB, AND MIDDLE
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                #mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

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

        mx, my = midpoint(index_tipx, index_tipy, thumb_tipx, thumb_tipy)
        mx, my = int(mx), int(my)
        image = cv2.circle(image, (mx, my), 5, (255,255,255), 5)
        
        #fig_arr = np.array(figs)
        cx, cy = int(cx), int(cy)
        lx, ly = cx+200, cy
        rx, ry = cx-200, cy
        
        lx, ly, rx, ry = int(lx), int(ly), int(rx), int(ry)
        
        if state == 'free':
            if (distance(mx, my, lx, ly) <= 150) and (10 <= point_dist_it <= 80):
                state = 'lclamped'
            elif (distance(mx, my, rx, ry) <= 150) and (10 <= point_dist_it <= 80):
                state = 'rclamped'
            
        if state == 'lclamped':
            lx, ly = mx, my
            cx, cy = lx-200, ly
        elif state == 'rclamped':
            rx, ry = mx, my
            cx, cy = rx+200, ry
            
        if (state == 'lclamped' or state == 'rclamped') and (point_dist_it > 150):
            state = 'free'
        
        image = cv2.circle(image, (cx, cy), 200, (0,255,0), 3)
        image = cv2.circle(image, (lx, ly), 3, (0,0,255), 5)
        image = cv2.circle(image, (rx, ry), 3, (0,0,255), 5)
                
        #figs = fig_arr.tolist()
		
        flip_image = cv2.flip(image,1)
        
        cv2.putText(flip_image, f'{point_dist_it:.2f}', (10, 160), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(flip_image, f'State: {state}', state_pos, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
		
        cv2.imshow("Hand Landmarks", flip_image)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
    else:
        break

capture.release()
cv2.destroyAllWindows()