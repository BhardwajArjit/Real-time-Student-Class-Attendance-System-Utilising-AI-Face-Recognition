import cv2 as cv

# Capturing the images of students for face recognition
cam_port = 0
video_capture = cv.VideoCapture(cam_port)

name = input('Enter your name: ')

while True:
    result, image = video_capture.read()
    cv.imshow(name, image)

    # Hit 'q' to quit the window and save the image
    if cv.waitKey(0) & 0xff == ord('q'):
        cv.imwrite(name + ".png", image)
        print("Image Taken")
        break

    # Hit 'r' to retake the image
    if 0xff == ord('r'):
        pass


video_capture.release()
cv.destroyAllWindows()