import cv2 
import numpy as np 
import mediapipe as mp
import time
import math
import pyautogui
import keyboard
import os

mp_pose = mp.solutions.pose
pose_model = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

capture = cv2.VideoCapture(0)

size = pyautogui.size()

screenx = size.width
screeny = size.height

a = (int(0.01 * screenx), int(0.65 * screeny))
b = (int(0.01 * screenx), int(0.7 * screeny))
c = (int(0.01 * screenx), int(0.75 * screeny))
d = (int(0.01 * screenx), int(0.8 * screeny))
e = (int(0.01 * screenx), int(0.85 * screeny))
f = (int(0.01 * screenx), int(0.9 * screeny))

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
def midpoint(x1, y1, x2, y2):
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    return (mx, my)
    
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
    
def get_pose_landmarks(pls, screenx, screeny):

    pl_list = []
    for pl in pls:
        pl_list.append({
                            'x': pl.x * screenx,
                            'y': pl.y * screeny,
                            'vis': pl.visibility
                        })
                        
    return pl_list
    
def get_face(pl_list, screenx, screeny):
    
    face_dict = {
                    'l_eye': (int(pl_list[2]['x']),  int(pl_list[2]['y'])),
                    'r_eye': (int(pl_list[5]['x']),  int(pl_list[5]['y'])),
                    'nose': (int(pl_list[0]['x']),  int(pl_list[0]['y'])),
                    'l_ear': (int(pl_list[7]['x']),  int(pl_list[7]['y'])),
                    'r_ear': (int(pl_list[8]['x']),  int(pl_list[8]['y'])),
                    'l_mouth': (int(pl_list[9]['x']),  int(pl_list[9]['y'])),
                    'r_mouth': (int(pl_list[10]['x']),  int(pl_list[10]['y']))
                }
    
    return face_dict
    
def get_left_arm(pl_list, screenx, screeny):
    
    lsh_slope = getSlope(pl_list[11]['x'], pl_list[11]['y'], pl_list[23]['x'], pl_list[23]['y'])
    lse_slope = getSlope(pl_list[11]['x'], pl_list[11]['y'], pl_list[13]['x'], pl_list[13]['y'])
    lew_slope = getSlope(pl_list[13]['x'], pl_list[13]['y'], pl_list[15]['x'], pl_list[15]['y'])
    
    hs_se_angle = getAngle(lsh_slope, lse_slope)
    se_ew_angle = getAngle(lse_slope, lew_slope)
    
    hssea = int(hs_se_angle)
    seewa = 180 - int(se_ew_angle)
    
    l_arm_dict = {'shoulder': (int(pl_list[11]['x']),  int(pl_list[11]['y'])),
                    'elbow': (int(pl_list[13]['x']), int(pl_list[13]['y'])),
                    'wrist': (int(pl_list[15]['x']), int(pl_list[15]['y'])),
                    'index': (int(pl_list[19]['x']), int(pl_list[19]['y'])),
                    'arm_body_angle': hssea,
                    'elbow_angle': seewa}
    
    return l_arm_dict
    
def get_left_leg(pl_list, screenx, screeny):
    
    lhk_slope = getSlope(pl_list[23]['x'], pl_list[23]['y'], pl_list[25]['x'], pl_list[25]['y'])
    lka_slope = getSlope(pl_list[25]['x'], pl_list[25]['y'], pl_list[27]['x'], pl_list[27]['y'])
    
    hk_ka_angle = getAngle(lhk_slope, lka_slope)
    
    hkkaa = int(hk_ka_angle)
    
    l_leg_dict = {'hip': (int(pl_list[23]['x']),  int(pl_list[23]['y'])),
                    'knee': (int(pl_list[25]['x']), int(pl_list[25]['y'])),
                    'ankle': (int(pl_list[27]['x']), int(pl_list[27]['y'])),
                    'heel': (int(pl_list[29]['x']), int(pl_list[29]['y'])),
                    'toes': (int(pl_list[31]['x']), int(pl_list[31]['y'])),
                    'knee_angle': hkkaa}
    
    return l_leg_dict
    
def get_right_arm(pl_list, screenx, screeny):
    
    rsh_slope = getSlope(pl_list[12]['x'], pl_list[12]['y'], pl_list[24]['x'], pl_list[24]['y'])
    rse_slope = getSlope(pl_list[12]['x'], pl_list[12]['y'], pl_list[14]['x'], pl_list[14]['y'])
    rew_slope = getSlope(pl_list[14]['x'], pl_list[14]['y'], pl_list[16]['x'], pl_list[16]['y'])
    
    hs_se_angle = getAngle(rsh_slope, rse_slope)
    se_ew_angle = getAngle(rse_slope, rew_slope)
    
    hssea = 180 - int(hs_se_angle)
    seewa = int(se_ew_angle)
    
    r_arm_dict = {'shoulder': (int(pl_list[12]['x']),  int(pl_list[12]['y'])),
                    'elbow': (int(pl_list[14]['x']), int(pl_list[14]['y'])),
                    'wrist': (int(pl_list[16]['x']), int(pl_list[16]['y'])),
                    'index': (int(pl_list[20]['x']), int(pl_list[20]['y'])),
                    'arm_body_angle': hssea,
                    'elbow_angle': seewa}
    
    return r_arm_dict
    
def get_right_leg(pl_list, screenx, screeny):
    
    rhk_slope = getSlope(pl_list[24]['x'], pl_list[24]['y'], pl_list[26]['x'], pl_list[26]['y'])
    rka_slope = getSlope(pl_list[26]['x'], pl_list[26]['y'], pl_list[28]['x'], pl_list[28]['y'])
    
    hk_ka_angle = getAngle(rhk_slope, rka_slope)
    
    hkkaa = 180 - int(hk_ka_angle)
    
    r_leg_dict = {'hip': (int(pl_list[24]['x']),  int(pl_list[24]['y'])),
                    'knee': (int(pl_list[26]['x']), int(pl_list[26]['y'])),
                    'ankle': (int(pl_list[28]['x']), int(pl_list[28]['y'])),
                    'heel': (int(pl_list[30]['x']), int(pl_list[30]['y'])),
                    'toes': (int(pl_list[32]['x']), int(pl_list[32]['y'])),
                    'knee_angle': hkkaa}
    
    return r_leg_dict

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
        
        face = get_face(pl_list, screenx, screeny)
        left_arm = get_left_arm(pl_list, screenx, screeny)
        right_arm = get_right_arm(pl_list, screenx, screeny)
        left_leg = get_left_leg(pl_list, screenx, screeny)
        right_leg = get_right_leg(pl_list, screenx, screeny)
        
        msx, msy = midpoint(left_arm['shoulder'][0], left_arm['shoulder'][1], right_arm['shoulder'][0], right_arm['shoulder'][1])
        image = cv2.circle(image, (int(msx), int(msy)), 3, (255, 0, 255), 10)
        image = cv2.line(image, (int(msx), int(msy)), (face['nose'][0], face['nose'][1]), (0, 255, 0), 10)
        
        state = 'none'
        
        flip_image = cv2.flip(image,1)
        
        cv2.putText(flip_image, f"angle left arm to body: {left_arm['arm_body_angle']}", a, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(flip_image, f"angle left elbow: {left_arm['elbow_angle']}", b, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(flip_image, f"angle right arm to body: {right_arm['arm_body_angle']}", c, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(flip_image, f"angle right elbow: {right_arm['elbow_angle']}", d, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(flip_image, f"angle left knee: {left_leg['knee_angle']}", e, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(flip_image, f"angle right knee: {right_leg['knee_angle']}", f, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow("pose_test", flip_image)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
    else:
        break

capture.release()
cv2.destroyAllWindows()