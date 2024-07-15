import cv2 
import numpy as np 
import mediapipe as mp
import time
import math
import pyautogui
import keyboard
from mediapipe_pose_py.im_geometry import midpoint, distance
import tensorflow as tf
from tensorflow import keras

model = tf.keras.models.load_model('thumbs_up_model.keras')

mp_hands = mp.solutions.hands
hands_model = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

capture = cv2.VideoCapture(0)

size = pyautogui.size()

screenx = size.width
screeny = size.height

a = (int(0.01 * screenx), int(0.65 * screeny))
        
def get_hand_landmarks(hls, screenx, screeny):

    hl_list = []
    for hl in hls:
        hl_list.append({
                            'x': hl.x * screenx,
                            'y': hl.y * screeny,
                            'vis': hl.visibility
                        })
                        
    return hl_list

def predict_hand(hl_list, model):
    landmarks_array = np.array([[hl['x'], hl['y']] for hl in hl_list]).flatten()
    landmarks_array = landmarks_array.reshape(1,42)
    pred = model.predict(landmarks_array)
    if pred > 0.5:
        gesture = 'thumbs up'
    else:
        gesture = 'none'
    return gesture

while capture.isOpened():
    ret, frame = capture.read()
    if ret:
        frame = cv2.resize(frame, (screenx, screeny))

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = hands_model.process(image)
        image.flags.writeable = True

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                hl_list = get_hand_landmarks(hand_landmarks.landmark, screenx, screeny)
        else:
            hl_list = []

        if len(hl_list) < 21:
            gest = 'none'
        else:

            gest = predict_hand(hl_list, model)
        
        flip_image = cv2.flip(image,1)

        cv2.putText(flip_image, f"Predict: {gest}", a, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow("thumbs up", flip_image)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
    else:
        break

capture.release()
cv2.destroyAllWindows()