import os
import cv2

from source.image_io.ImageOperation import get_brightness
from source.image_io.ImageOperation import remove_similar_faces
from source.image_io.ImageOperation import get_standard_derivation

from source.file_io.PathAnalysis import get_all_frames
from source.file_io.PathAnalysis import get_all_directories

from source.file_io.PathAnalysis import get_frame_name
from source.file_io.PathAnalysis import get_last_directory_name


class FaceDetector:
    def __init__(self, cascade_path):
        self.CASCADE_PATH = cascade_path
        assert (os.path.exists(self.CASCADE_PATH)), "Face Detect: No cascade file detected."

        self.FACE_CASCADE = cv2.CascadeClassifier(self.CASCADE_PATH)

    def extract_faces(self, movie_name, path_manager):
        scenes_path = path_manager.get_movie_workspace(movie_name)['SCENES']
        events_directories = get_all_directories(scenes_path)
        print "\tDetecting faces (total " + str(len(events_directories)) + "):"
        print_index = 1
        for directory in events_directories:
            event_index = get_last_directory_name(directory)
            frames = get_all_frames(directory)

            echo_index = 0
            all_indexes_string = " out of " + str(len(frames))
            for frame in frames:
                frame_index = get_frame_name(frame)
                frame_image = cv2.imread(frame)

                faces = self.get_faces(frame_image)
                face_index = 0

                for face in faces:
                    if get_brightness(face) > 10 and get_standard_derivation(face) > 10:
                        face_path = path_manager.get_face_path(movie_name, event_index, frame_index, face_index)
                        cv2.imwrite(face_path, face)
                        face_index += 1

                echo_index += 1
                if echo_index % 20 == 0:
                    print "\t\t\t Detect faces: Processed image " + str(echo_index) + all_indexes_string

            print "\t\tCurrently processed: " + str(print_index)
            print_index += 1

    def get_faces(self, image):
        regions, image = self.detect(image)
        return self.crop(regions, image)

    def detect(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        faces = self.FACE_CASCADE.detectMultiScale(
            gray_image,
            scaleFactor=1.5,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE,
        )

        if not len(faces):
            return [], image

        faces[:, 2:] += faces[:, :2]
        return faces, image

    @staticmethod
    def crop(regions, image):
        face_list = []
        for x_min, y_min, x_max, y_max in regions:
            cut = image[y_min:y_max, x_min:x_max]
            face_list.append(cut)

        return face_list

    @staticmethod
    def remove_redundancy(movie_name, path_manager):
        actor_path = path_manager.get_movie_workspace(movie_name)['ACTORS']
        actor_directories = get_all_directories(actor_path)
        print "\tRemoving redundant faces (total " + str(len(actor_directories)) + "):"

        event_index = 0
        for directory in actor_directories:
            remove_similar_faces(directory)
            event_index += 1
            print "\t\tCurrently processed: " + str(event_index)
