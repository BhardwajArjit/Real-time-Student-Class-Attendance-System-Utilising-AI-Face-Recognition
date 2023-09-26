import os
from datetime import date
import cv2 as cv
import face_recognition
import numpy as np
import xlrd
from xlutils.copy import copy as xl_copy

# Read current folder path
CurrentFolder = os.getcwd()
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
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Setting up the attendance Excel file
rb = xlrd.open_workbook('attendance_excel.xls', formatting_info=True)
wb = xl_copy(rb)
subject_name = input('Please give current subject lecture name: ')
sheet1 = wb.add_sheet(subject_name)
sheet1.write(0, 0, 'Name/Date')
sheet1.write(0, 1, str(date.today()))
row = 1
col = 0
already_attendance_taken = ""

while True:
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

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
                print("attendance taken")
                wb.save('attendance_excel.xls')
                already_attendance_taken = name
            else:
                print("next student")

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

    # Hit 'q' on the keyboard to quit!
    if cv.waitKey(1) & 0xff == ord('q'):
        print("data save")
        break

# Release handle to the webcam
video_capture.release()
cv.destroyAllWindows()
