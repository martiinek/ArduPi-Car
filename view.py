#view.py

import os

os.environ['QT_QPA_PLATFORM'] = 'xcb'

import cv2
import numpy as np
import RPi.GPIO as GPIO
import sched
import time

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

last_distance = 0

def check_ground():
    step_size = 6
    fov_width = 173
    edge_array = []

    _, img = capture.read()
    img = cv2.resize(img, (640, 480))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.bilateralFilter(img_gray, 10, 25, 50)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10))
    dilate = cv2.morphologyEx(img_gray, cv2.MORPH_DILATE, kernel)
    img_edge = cv2.Canny(dilate, 35, 150)
    imagewidth = img_edge.shape[1] - 1
    imageheight = img_edge.shape[0] - 1

    for j in range(0, imagewidth, step_size):
        for i in range(imageheight-5, 0, -1):
            if img_edge.item(i, j) == 255:
                edge_array.append((j, i))
                break
        else:
            edge_array.append((j, 0))
            
    edge_array.insert(0, (0, imageheight))
    edge_array.append((imagewidth, imageheight))
    
    top_left = (0, 0)
    bottom_left = (0, imageheight)
    top_right = (imagewidth, 0)
    bottom_right = (imagewidth, imageheight)
    pts1 = np.float32([top_left, bottom_left, top_right, bottom_right])
    pts2 = np.float32([[fov_width, 0], [0, imageheight], [(imagewidth - fov_width), 0], [imagewidth, imageheight]])
    
    transform_matrix = cv2.getPerspectiveTransform(pts1, pts2)

    transformed_edge_array = []
    for point in edge_array:
        x, y = point
        original_coordinates = np.array([x, y, 1])
        transformed_coordinates = np.dot(transform_matrix, original_coordinates)
        transformed_x = int(transformed_coordinates[0] / transformed_coordinates[2])
        transformed_y = int(transformed_coordinates[1] / transformed_coordinates[2])
        transformed_edge_array.append((transformed_x, transformed_y))
        
    cv2.waitKey(1)

    return transformed_edge_array

def ping():
    global last_distance
    GPIO.setmode(GPIO.BOARD)

    TRIG_PIN = 13
    ECHO_PIN = 15

    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

    pulse_start_time = 0
    pulse_end_time = 0

    try:

        GPIO.output(TRIG_PIN, GPIO.LOW)
        time.sleep(2E-6)
        GPIO.output(TRIG_PIN, GPIO.HIGH)
        time.sleep(10E-6)
        GPIO.output(TRIG_PIN, GPIO.LOW)

        while GPIO.input(ECHO_PIN) == 0:
            pulse_start_time = time.time()
        while GPIO.input(ECHO_PIN) == 1:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        if distance > 300 or distance <= 0:
            distance = last_distance
        else:
            last_distance = distance
            
        #print(distance)
        time.sleep(0.1)
        return distance
        
    except Exception as e:
        print(f"Error in ping function: {e}")

# pri zmene vzdalenosti se meni uhel, bude se muset prepocitavat uhel podle vzdalenosti z hc sr04
# pridat nejakou maximalni vzdalenost kamery od objektu aby nedochazelo k prilis nizkym hodnotam y v edge_array
