from __future__ import absolute_import

from cv_bridge import CvBridge
import face_recognition
import actionlib
import fnmatch
import rospy
import time
import cv2
import os

from agent.abstract_action import AbstractAction
from agent.util.enuns import LogColor

from hera.msg import faceFeedback, faceResult, faceAction, faceGoal

class Face(AbstractAction):
    """docstring for FaceRecognition."""
    def __init__(self, robot):
        super(Face, self).__init__(robot)
        self.robot_ns = rospy.get_namespace()

        self._as = actionlib.SimpleActionServer("face", faceAction, self.goal_callback, False)
        self._as.start()

        self.bridge = CvBridge()
        self.people_dir = rospy.get_param('resources') + '/people/'

    def goal_callback(self, goal):
        result = self.execute()
        self._as.set_succeeded(faceResult(result=result))

    def execute(self):
        files = fnmatch.filter(os.listdir(self.people_dir), '*.jpg')

        faces_images = []
        known_face_encodings = []
        known_face_names = []
        for i in range(0,len(files)):
            faces_images.append(face_recognition.load_image_file(self.people_dir + files[i]))
            known_face_encodings.append(face_recognition.face_encodings(faces_images[i])[0])
            known_face_names.append(files[i].replace('.jpg',''))

        # robot vision
        frame = self.bridge.imgmsg_to_cv2(self.robot.get_sensors('camera'), 'bgr8')
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        now = time.strftime("%H%M%S", time.localtime(time.time()))
        output_file = self.robot_ns+'/face_recognition_'+now+'.jpg'
        cv2.imwrite(output_file, frame)

        face_names_str = " - ".join(face_names)

        now = time.strftime("%H:%M:%S", time.localtime(time.time()))
        # rospy.loginfo('Face recognition: ' + colored(face_names_str, 'magenta'))
        # self.report.log.append('\\lbrack' + str(now) + '\\rbrack ~ Face recognition: \\textcolor{magenta}{'+ face_names_str + '} (See Figure \\ref{fig:' + output_file + '}).')
        # self.report.pictures.append([output_file, 'Face recognition: ' + face_names_str])
        #

        self.robot.add_log('Face recognition', face_names_str, color=LogColor.MAGENTA, fig_file=output_file)

        face_names = [x for x in face_names if x != 'Unknown']
        if (len(face_names) > 0):
            return face_names[0]
        else:
            return ''
