import os
import cv2
import math
import numpy

from source.image_io.ImageEncoder import ImageEncoder
from source.image_io.FaceDetector import FaceDetector

from source.file_io.PathAnalysis import get_key
from source.file_io.PathAnalysis import get_movie_event

from source.file_io.PathAnalysis import get_all_clips
from source.file_io.PathAnalysis import get_all_frames
from source.file_io.PathAnalysis import get_all_directories

from source.file_io.PathAnalysis import get_movie_name
from source.file_io.PathAnalysis import get_last_directory_name

from source.file_io.PathManager import PathManager
from source.database_io.DataLoader import DataLoader


class Interface:

    def __init__(self, root_directory):
        self.ENCODER = ImageEncoder()
        self.DETECTOR = FaceDetector(os.path.join(root_directory,
                                                  'source', 'image_io', 'haarcascade_frontalface_default.xml'))
        self.DATA_LOADER = DataLoader("", PathManager(root_directory))

        self._forbidden_project_path = root_directory
        self.RESOURCES_PATH = os.path.join(self._forbidden_project_path, "resources")
        self.RAW_VIDEO_PATH = os.path.join(self.RESOURCES_PATH, "raw_videos")
        self.CLIP_INFO_PATH = os.path.join(self.RESOURCES_PATH, "clip_information")

        self.INFO_CPICKLE = os.path.join(self.CLIP_INFO_PATH, "info.cpickle")
        self.SCENE_CPICKLE = os.path.join(self.CLIP_INFO_PATH, "scene.cpickle")
        self.ACTOR_CPICKLE = os.path.join(self.CLIP_INFO_PATH, "actor.cpickle")
        self.SPEED_CPICKLE = os.path.join(self.CLIP_INFO_PATH, "speed.cpickle")

        assert (os.path.isdir(self.RESOURCES_PATH)), "Path: Resources directory is not valid."
        assert (os.path.isdir(self.RAW_VIDEO_PATH)), "Path: Raw video directory is not valid."
        assert (os.path.isdir(self.CLIP_INFO_PATH)), "Path: Clip information directory is not valid."

        if os.path.exists(self.INFO_CPICKLE):
            assert (os.path.exists(self.INFO_CPICKLE)), "Path: Information file path is not valid."
            assert (os.path.exists(self.SCENE_CPICKLE)), "Path: Scene file path is not valid."
            assert (os.path.exists(self.ACTOR_CPICKLE)), "Path: Actor file path is not valid."
            assert (os.path.exists(self.SPEED_CPICKLE)), "Path: Speed file path is not valid."

    def _get_settings(self):
        return {
            'RESOURCES_PATH': self.RESOURCES_PATH,
            'RAW_VIDEO_PATH': self.RAW_VIDEO_PATH,
            'CLIP_INFO_PATH': self.CLIP_INFO_PATH,

            'INFO_CPICKLE': self.INFO_CPICKLE,
            'SCENE_CPICKLE': self.SCENE_CPICKLE,
            'ACTOR_CPICKLE': self.ACTOR_CPICKLE,
            'SPEED_CPICKLE': self.SPEED_CPICKLE
        }

    def _get_movie_workspace(self, movie_name):
        return {
            'ROOT': os.path.join(self.CLIP_INFO_PATH, movie_name),
            'CLIPS': os.path.join(self.CLIP_INFO_PATH, movie_name, 'clips'),
            'SCENES': os.path.join(self.CLIP_INFO_PATH, movie_name, 'scenes'),
            'ACTORS': os.path.join(self.CLIP_INFO_PATH, movie_name, 'actors'),
            'FACE_POOL': os.path.join(self.CLIP_INFO_PATH, movie_name, 'face_pool'),
            'SEARCH_POOL': os.path.join(self.CLIP_INFO_PATH, movie_name, 'search_pool')
        }

    def _get_face_directory(self, movie_name, event_index):
        return os.path.join(self._get_movie_workspace(movie_name)['ACTORS'], str(event_index))

    def _get_scene_directory(self, movie_name, event_index):
        return os.path.join(self._get_movie_workspace(movie_name)['SCENES'], str(event_index))

    def get_info_data(self):
        return self.DATA_LOADER.load_info_data()

    def get_scene_data(self):
        return self.DATA_LOADER.load_scene_data()

    def get_actor_data(self):
        return self.DATA_LOADER.load_actor_data()

    def get_speed_data(self):
        return self.DATA_LOADER.load_speed_data()

    # Return a list of movie names
    def get_all_movie_names(self):
        movie_names = []
        for movie_directory in get_all_directories(self.CLIP_INFO_PATH):
            movie_names.append(get_last_directory_name(movie_directory))
        return movie_names

    # Input movie name
    # Return the raw video path
    def get_raw_movie_path(self, movie_name):
        return os.path.join(self.RAW_VIDEO_PATH, movie_name + '.mov')

    # Input movie name
    # Return the keys of all the events
    def get_all_keys(self, movie_name):
        clip_paths = self.get_all_clip_paths(movie_name)
        all_keys = []

        for clip_path in clip_paths:
            all_keys.append(get_key(movie_name, get_movie_name(clip_path)))
        return all_keys

    # Input movie name
    # Return all the paths of all the event clips
    def get_all_clip_paths(self, movie_name):
        clip_root_path = self._get_movie_workspace(movie_name)['CLIPS']
        clip_paths = get_all_clips(clip_root_path)
        return clip_paths

    # Input event key
    # Return the clip path to that event
    def get_clip_path(self, key):
        movie, event = get_movie_event(key)
        return os.path.join(self._get_movie_workspace(movie)['CLIPS'], event + ".mp4")

    # Input event key
    # Return the paths of face images appeared in that event
    def get_face_paths(self, key):
        movie, event = get_movie_event(key)
        face_directory = self._get_face_directory(movie, event)
        if not os.path.isdir(face_directory):
            return []
        return get_all_frames(face_directory)

    # Input event key
    # Return the paths of scene images belonging to that event
    def get_scene_paths(self, key):
        movie, event = get_movie_event(key)
        scene_directory = self._get_scene_directory(movie, event)
        if not os.path.isdir(scene_directory):
            return []
        return get_all_frames(scene_directory)

    # Input movie name
    # Return the middle key frame of the middle key events
    def get_cover_for_movie(self, movie_name):
        keys = self.get_all_keys(movie_name)
        index = int(math.floor(len(keys) / 2.0))
        return self.get_cover_for_event(keys[index])

    # Input event key
    # Return the key frame at the middle of the frames
    def get_cover_for_event(self, key):
        paths = self.get_scene_paths(key)
        index = int(math.floor(len(paths) / 2.0))
        return paths[index]

    # Input the path of the entire image
    # Return the list of descriptors of the faces appeared in that image in array type
    # unique flag: return a list contains one face (if that image contains more than one faces)
    def get_face_descriptor(self, path, unique=False):
        image = cv2.imread(path)
        faces = self.DETECTOR.get_faces(image)
        face_descriptors = []
        for face in faces:
            face_descriptors.append(self.ENCODER.encode_face(face))
            if unique:
                return face_descriptors
        return face_descriptors

    # Input the path of the frame image
    # Return the descriptor of this scene image in array type
    def get_scene_descriptor(self, path):
        image = cv2.imread(path)
        return self.ENCODER.encode_scene(image)

    # Input two descriptors (must be of the same type - scene or face)
    # Return the float type measurement
    @staticmethod
    def compare_descriptor(descriptor_a, descriptor_b):
        return 0.5 * numpy.sum([((a - b) ** 2) / (a + b + 1e-10) for (a, b) in zip(descriptor_a, descriptor_b)])

