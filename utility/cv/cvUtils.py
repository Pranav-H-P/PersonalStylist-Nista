import cv2
import numpy as np
import mediapipe as mp
import math
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from deepface import DeepFace

base_options = python.BaseOptions(model_asset_path='utility/cv/models/pose_landmarker_full.task')
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    output_segmentation_masks=True)
detector = vision.PoseLandmarker.create_from_options(options)

# Constants for landmark position index
# Ear and heel positions will be used to approximate height
# I'm assuming that height is approximately equal to =>
#  distance(rightEar,leftEar) + distance(leftEar,leftHeel)

LEFT_EAR_IDX = 7
RIGHT_EAR_IDX = 8

LEFT_SHOULDER_IDX = 11
RIGHT_SHOULDER_IDX = 12

LEFT_HIP_IDX = 23
RIGHT_HIP_IDX = 24

LEFT_HEEL_IDX = 27

def _convertFormImage(image): # converts the binary file into a np Array
                              # for further processing

    imgBytes = np.frombuffer(image.read(), np.uint8)
    imgArr = cv2.imdecode(imgBytes, cv2.IMREAD_COLOR)

    return imgArr


def getDistance(point1, point2): # returns Distance between 2 points
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def _getBodyRatios(image): # returns shoulder to hip ratio and 
                           # waist to height ratio

    rgbImg = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # convert to rgb, cv2 uses bgr

    mpImage = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgbImg) # convert into mediapipe img format

    detectionResult = detector.detect(mpImage)
    
    if detectionResult.pose_landmarks and len(detectionResult.pose_landmarks) >= 1: # if person is actually detected
        
        results = detectionResult.pose_landmarks[0] # gets first result (data of first person detected in image)
        
        leftEar = results[LEFT_EAR_IDX]
        rightEar = results[RIGHT_EAR_IDX]

        leftShoulder = results[LEFT_SHOULDER_IDX]
        rightShoulder = results[RIGHT_SHOULDER_IDX]

        leftHip = results[LEFT_HIP_IDX]
        rightHip = results[RIGHT_HIP_IDX]

        leftHeel = results[LEFT_HEEL_IDX]

        height = getDistance(leftEar, rightEar) + getDistance(leftEar, leftHeel)
        hipWidth = getDistance(leftHip, rightHip)
        shoulderWidth = getDistance(leftShoulder, rightShoulder)

        hHR = round(hipWidth / height, 2) # hip to height ratio
        sHR = round(shoulderWidth / hipWidth, 2) #shoulder to hip ratio

        return sHR, hHR


    else:
        return None

def _getFacialImageData(image): # returns age, gender, ethnicity and skin tone
    
    result = DeepFace.analyze(image, actions = ['age', 'gender', 'race'], silent = True)[0]
    
    age = result['age']
    faceRegion = result['region']
    gender = result['dominant_gender']
    ethnicity = result['dominant_race']

    if gender == "Man":
        gender = "Male"
    else:
        gender = "Female"

    x = faceRegion['x'] + 25
    y = faceRegion['y'] + 25
    w = faceRegion['w'] - 50
    h = faceRegion['h'] - 50

    # hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    face = image[y:y+h, x:x+w]
    
    

    # Calculate the average color of the face region
    avgColor = cv2.mean(face)
    
    avgColorString = "Red: " + str(round(avgColor[2], 2)) + ", Green: " + str(round(avgColor[1], 2)) + ", Blue: "+ str(round(avgColor[0], 2))

    return age, gender, ethnicity, avgColorString



def getImageData(file): # to be accessed by the main script for
                        # processing and getting data from image
    
    img = _convertFormImage(file)

    tup = _getBodyRatios(img) # temporary variable to check if process failed or not

    if tup == None:
        return None

    shoulderToHip, hipToHeight = tup # tuple unpacking
    
    otherDat = _getFacialImageData(img) # temporary variable again for failure checking

    if otherDat == None:
        return None
    
    age, gender, race, skinTone = otherDat


    return {
        "age": age,
        "gender": gender,
        "ethnicity": race,
        "skinTone": skinTone,
        "sHR": shoulderToHip,
        "hHR": hipToHeight
    }


if __name__ == "__main__":
    pass
"""
    image1 = cv2.imread("experimentation/face.jpg")
    image2 = cv2.imread("experimentation/face.png")
    image3 = cv2.imread("experimentation/face2.jpg")
    image4 = cv2.imread("experimentation/face3.png")
    image5 = cv2.imread("experimentation/face4.jpg")

    print(_getFacialImageData(image1))
    print(_getFacialImageData(image2))
    print(_getFacialImageData(image3))
    print(_getFacialImageData(image4))
    print(_getFacialImageData(image5))
"""