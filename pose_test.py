import cv2 
import numpy as np 
import mediapipe as mp
import time
from im_geometry import midpoint, getAngle, getSlope
import pyautogui
import keyboard
import os
import base64
import sys
from pose_utils import get_face, get_left_arm, get_right_arm, get_left_leg, get_right_leg

mp_pose = mp.solutions.pose
pose_model = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

capture = cv2.VideoCapture(1)

size = pyautogui.size()

screenx = 640
screeny = 480

url = 'http://localhost:3000/upload'

a = (int(0.01 * screenx), int(0.65 * screeny))
b = (int(0.01 * screenx), int(0.7 * screeny))
c = (int(0.01 * screenx), int(0.75 * screeny))
d = (int(0.01 * screenx), int(0.8 * screeny))
e = (int(0.01 * screenx), int(0.85 * screeny))
f = (int(0.01 * screenx), int(0.9 * screeny))
    
def get_pose_landmarks(pls, screenx, screeny):

    pl_list = []
    for pl in pls:
        pl_list.append({
                            'x': pl.x * screenx,
                            'y': pl.y * screeny,
                            'vis': pl.visibility
                        })
                        
    return pl_list

while capture.isOpened():
    ret, frame = capture.read()
    if ret:
        frame = cv2.resize(frame, (screenx, screeny))

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = pose_model.process(image)
        image.flags.writeable = True

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=10, circle_radius=3),
                                        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=10, circle_radius=1))
            pl_list = get_pose_landmarks(results.pose_landmarks.landmark, screenx, screeny)
        else:
            pl_list = []
        
        if len(pl_list) <= 22:
            continue
        
        face = get_face(pl_list)
        left_arm = get_left_arm(pl_list)
        right_arm = get_right_arm(pl_list)
        left_leg = get_left_leg(pl_list)
        right_leg = get_right_leg(pl_list)
        
        msx, msy = midpoint(left_arm['shoulder'][0], left_arm['shoulder'][1], right_arm['shoulder'][0], right_arm['shoulder'][1])
        image = cv2.circle(image, (int(msx), int(msy)), 3, (255, 0, 255), 10)
        image = cv2.line(image, (int(msx), int(msy)), (face['nose'][0], face['nose'][1]), (0, 255, 0), 10)
        
        state = 'none'
        
        flip_image = cv2.flip(image,1)
        
        cv2.putText(flip_image, f"angle left arm to body: {left_arm['arm_body_angle']}", a, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(flip_image, f"angle left elbow: {left_arm['elbow_angle']}", b, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(flip_image, f"angle right arm to body: {right_arm['arm_body_angle']}", c, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(flip_image, f"angle right elbow: {right_arm['elbow_angle']}", d, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(flip_image, f"angle left knee: {left_leg['knee_angle']}", e, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(flip_image, f"angle right knee: {right_leg['knee_angle']}", f, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)
        
        #cv2.imshow("pose_test", flip_image)
        
        _, buffer = cv2.imencode('.jpg', flip_image, [cv2.IMWRITE_JPEG_QUALITY, 70])
        jpg_as_text = base64.b64encode(buffer).decode()
        print(jpg_as_text)
        sys.stdout.flush()
        
        time.sleep(0.033)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
    else:
        break

capture.release()
cv2.destroyAllWindows()