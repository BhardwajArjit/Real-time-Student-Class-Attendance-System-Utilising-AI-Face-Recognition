import cv2 as cv

# Capturing the images of students for face recognition
cam_port = 0
video_capture = cv.VideoCapture(cam_port)

name = input('Enter your name ')

while 1:
    result, image = video_capture.read()
    cv.imshow(name, image)
    if cv.waitKey(0):
        cv.imwrite(name + ".png", image)
        print("Image Taken")

    else:
        print("No image detected. Please try again!")