from cvzone.HandTrackingModule import HandDetector
import cv2
import numpy as np
import math
import osascript
import time
from ctypes import CDLL, c_int, c_double
import subprocess
import re

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.7, maxHands=2)
target_brightness = 0
volBar = target_brightness
area = 0
colorVol = (255, 0, 0)
colorBrightness = (255, 0, 0)


def getBrightness():
    result = subprocess.run(['brightness', '-l'], stdout=subprocess.PIPE)
    a = str(result.stdout)
    a = round(float(a[82:-4]), 1)
    return a


def getVolume():
    command = "osascript -e 'output volume of (get volume settings)'"  # get volume
    ret = subprocess.run(command, capture_output=True, shell=True)
    a = int(ret.stdout.decode('utf-8'))
    return a


brightnessSet = getBrightness() * 100  # percentage of brightness
volSet = getVolume()  # volume percentage

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)  # With Draw
    # hands = detector.findHands(img, draw=False)  # No Draw

    #  precaution for 0 brightness
    if brightnessSet < 10:
        subprocess.run(['brightness', '0.2'])  # Set brightness to 20% precaution for 0 brightness
        brightnessSet = 20
        time.sleep(0.1)

    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmarks points
        bbox1 = hand1["bbox"]  # Bounding Box info x,y,w,h
        centerPoint1 = hand1["center"]  # center of the hand cx,cy
        handType1 = hand1["type"]  # Hand Type Left or Right
        # print(len(lmList1),lmList1)
        # print(bbox1)
        # print(centerPoint1)
        # fingers1 = detector.fingersUp(hand1)
        # length, info, img = detector.findDistance(lmList1[8], lmList1[12], img)  # with draw
        # length, info = detector.findDistance(lmList1[8], lmList1[12])  # no draw
        if len(hands) == 1:
            area = (bbox1[2] - bbox1[0]) * (bbox1[3] - bbox1[1]) // 100

            if handType1 == "Right":
                area = -area
                if -450 < area < 2000:
                    cv2.putText(img, "Volume Control", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    length, info, img = detector.findDistance(lmList1[8][:2], lmList1[4][:2], img)  # with draw
                    target_volume = np.interp(length, [50, 300], [0, 100])  # Normalising the volume with the length of
                    # the hand
                    volBar = np.interp(length, [50, 300],
                                       [400, 150])  # Normalising the volumeBar with the length of the
                    # hand

                    # Smoothening the volume
                    smoothness = 10
                    volPer: int = smoothness * round(target_volume / smoothness)

                    cv2.putText(img, f'{int(volPer)}%', (40, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, colorVol, 2)
                    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
                    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
                    fingers = detector.fingersUp(hand1)  # Checking if the fingers are raised

                    # If pinky is down set volume
                    if fingers[4] == 0:
                        if volSet != volPer:
                            commandVol = np.interp(volPer, [0, 100], [0, 10])
                            command = f"osascript -e \"set Volume {commandVol}\""  # set volume
                            subprocess.run(command, shell=True)
                            volSet = volPer
                            colorVol = (0, 255, 0)
                    else:
                        colorVol = (255, 0, 0)

            if handType1 == "Left":
                # print("Brightness Control")
                cv2.putText(img, "Brightness Control", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                length, info, img = detector.findDistance(lmList1[8][:2], lmList1[4][:2], img)  # with draw
                target_brightness = np.interp(length, [50, 300],
                                              [0, 100])  # Normalising the brightness with the length of
                # the hand
                brightnessBar = np.interp(length, [50, 300],
                                          [400, 150])  # Normalising the BrightnessBar with the length of the
                # hand

                # Smoothening the volume
                smoothness = 10
                brightnessPer: int = smoothness * round(target_brightness / smoothness)

                cv2.putText(img, f'{int(brightnessPer)}%', (40, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, colorBrightness, 2)
                cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
                cv2.rectangle(img, (50, int(brightnessBar)), (85, 400), (255, 0, 0), cv2.FILLED)
                fingers = detector.fingersUp(hand1)  # Checking if the fingers are raised

                # If pinky is down set volume
                if fingers[4] == 0:
                    curr = getBrightness()  # curr is in range(0,1)

                    #  precaution for 0 brightness
                    if brightnessPer < 10:
                        brightnessPer = 20

                    if curr != target_brightness:
                        subprocess.run(["brightness", f"{brightnessPer / 100}"])
                        brightnessSet = brightnessPer
                        colorBrightness = (0, 255, 0)
                else:
                    colorBrightness = (255, 0, 0)

        if len(hands) == 2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # List of 21 Landmarks points
            bbox2 = hand2["bbox"]  # Bounding Box info x,y,w,h
            centerPoint2 = hand2["center"]  # center of the hand cx,cy
            handType2 = hand2["type"]  # Hand Type Left or Right

            fingers2 = detector.fingersUp(hand2)
            # print(fingers1, fingers2)
            # length, info, img = detector.findDistance(lmList1[8], lmList2[8], img) # with draw
            length, info, img = detector.findDistance(centerPoint1, centerPoint2, img)  # with draw

    cv2.putText(img, f'Volume Set {volSet}% ', (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                colorVol, 2)
    cv2.putText(img, f'Brightness Set {int(brightnessSet)}% ', (400, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                colorBrightness, 2)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
