# Real-time Student Class Attendance System with AI Face Recognition

## Project Description

This project aims to develop a comprehensive end-to-end real-time student class attendance system using AI face recognition. The system operates as follows: After the class concludes, students stand in front of a camera positioned within the classroom. They position their faces within a designated red square frame within the camera's view. When the AI detects a face, it performs facial recognition and crops the image for further processing. The cropped image is then sent to the YOLOv5 model.

The project is divided into two main modules:

1. **capture_image.py**
   - This module captures images of students for face recognition.
   - Images are saved in the current folder with filenames corresponding to the students' names.

2. **face_recognition_code.py**
   - This module uses the face_recognition library, which boasts an accuracy of 99.38%, compared to the approximate 95% accuracy of the YOLOv5 model.
   - After recognizing the face, it updates the attendance of the student in an Excel file maintained by this module.

## Getting Started

To use this attendance system, follow these steps:

1. **Prerequisites**:
   - Ensure you have Python installed on your system (Python 3.x recommended).
   - Install the required libraries mentioned in the `requirements.txt` file using `pip install -r requirements.txt`.

2. **Capture Student Images**:
   - Run `capture_image.py` to capture student images. Enter the student's name when prompted. Images will be saved in the current folder.
   - Hit 'r' on the keyboard to retake the image.
   - Hit 'q' on the keyboard to quit the window and save the image to the current directory.

3. **Recognition and Attendance**:
   - Run `face_recognition_code.py` to perform facial recognition and update attendance in the Excel file.
   - The facial recognition process will use the highly accurate face_recognition library.
   - Make sure the camera is set up to capture students' faces as described in the project description.
   - Hit 'q' on keyboard to quit.

## Project Structure

- `capture_image.py`: Captures student images for face recognition.
- `face_recognition_code.py`: Performs face recognition and updates attendance.
- `requirements.txt`: Lists the required Python libraries for this project.
- `attendance.xls`: Excel file to maintain attendance records.

## Dependencies

This project relies on the following Python libraries:

- face_recognition
- OpenCV
- numpy
- xlrd

Please refer to `requirements.txt` for the exact versions.

## Author

- Arjit Bhardwaj
- iamarjitbhardwaj@gmail.com
