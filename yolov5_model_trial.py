import os
from datetime import date
import cv2 as cv
import face_recognition
import numpy as np
import xlrd
from xlutils.copy import copy as xl_copy

# Load YOLOv5 model for face detection
CurrentFolder = os.getcwd()
yolo_weights = CurrentFolder + '\\yolov5s.pt'
yolo_config = CurrentFolder + '\\yolov5s.yaml'
yolo_net = cv.dnn.readNet(yolo_weights, yolo_config, "Darknet")

# Read current folder path
image1 = CurrentFolder + '\\arjit.png'
image2 = CurrentFolder + '\\hemant.png'

cam_port = 0
video_capture = cv.VideoCapture(cam_port)

# Load a sample picture and learn how to recognize it.
person1_name = "arjit"
person1_image = face_recognition.load_image_file(image1)
person1_face_encoding = face_recognition.face_encodings(person1_image)[0]

person2_name = "hemant"
person2_image = face_recognition.load_image_file(image2)
person2_face_encoding = face_recognition.face_encodings(person2_image)[0]

# Create list of known face encodings and their names
known_face_encodings = [
    person1_face_encoding,
    person2_face_encoding
]
known_face_names = [
    person1_name,
    person2_name
]

# Initialize some variables
face_names = []
process_this_frame = True

# Setting up the attendance Excel file
rb = xlrd.open_workbook('attendance_excel.xls', formatting_info=True)
wb = xl_copy(rb)
subject_name = input('Please give current subject lecture name ')
sheet1 = wb.add_sheet(subject_name)
sheet1.write(0, 0, 'Name/Date')
sheet1.write(0, 1, str(date.today()))
row = 1
col = 0
already_attendance_taken = ""

while True:
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster processing
    small_frame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color
    rgb_small_frame = cv.cvtColor(small_frame, cv.COLOR_BGR2RGB)

    if process_this_frame:
        # Detect faces using YOLOv5
        blob = cv.dnn.blobFromImage(rgb_small_frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        yolo_net.setInput(blob)
        detections = yolo_net.forward()

        face_locations = []
        for detection in detections[0]:
            confidence = detection[4]
            if confidence > 0.5:
                center_x = int(detection[0] * small_frame.shape[1])
                center_y = int(detection[1] * small_frame.shape[0])
                width = int(detection[2] * small_frame.shape[1])
                height = int(detection[3] * small_frame.shape[0])

                # Calculate face bounding box coordinates
                left = max(center_x - width // 2, 0)
                top = max(center_y - height // 2, 0)
                right = min(center_x + width // 2, small_frame.shape[1])
                bottom = min(center_y + height // 2, small_frame.shape[0])

                face_locations.append((top, right, bottom, left))

        face_encodings = [face_recognition.face_encodings(rgb_small_frame, [box])[0] for box in face_locations]
        face_names = []

        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)
            if (already_attendance_taken != name) and (name != "Unknown"):
                # Update the attendance of the student
                sheet1.write(row, col, name)
                col = col + 1
                sheet1.write(row, col, "Present")
                row = row + 1
                col = 0
                print("Attendance taken for", name)
                wb.save('attendance_excel.xls')
                already_attendance_taken = name
            else:
                print("Next student")

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv.FILLED)
        font = cv.FONT_HERSHEY_DUPLEX
        cv.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv.imshow("Video", frame)

    # Hit 'q' on the keyboard to quit
    if cv.waitKey(1) & 0xFF == ord('q'):
        print("Data saved")
        break

# Release handle to the webcam
video_capture.release()
cv.destroyAllWindows()
