# Face-Recognition-System-with-Attendance-System

The Attendance System uses face recognition to match the individual's face and write their names to a csv file. The system uses libraries like numpy, cv2 and face recognition.

The two methods that are pivotal for the system to work are the window and markAttendance method. The former shows a window which uses the webcam to show to face of the individual and the markAttendance method makes sure that the face detected is marked on a csv file.

At first, the system is trained based on some training data which in this case are the images of individuals whose attendance is supposed to be marked and then the model is tested on the test data which are the real time images from webcam captured frame by frame.
