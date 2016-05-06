import os

from .FileOperation import clear_directory
from source.database_io.DataLoader import DataLoader


class PathManager:
    def __init__(self, root_path=None):
        if not root_path:
            self._forbidden_project_path = os.path.dirname(os.getcwd())
        else:
            self._forbidden_project_path = root_path

        self.RESOURCES_PATH = os.path.join(self._forbidden_project_path, "resources")
        self.RAW_VIDEO_PATH = os.path.join(self.RESOURCES_PATH, "raw_videos")
        self.CLIP_INFO_PATH = os.path.join(self.RESOURCES_PATH, "clip_information")

        self.INFO_CPICKLE = os.path.join(self.CLIP_INFO_PATH, "info.cpickle")
        self.SCENE_CPICKLE = os.path.join(self.CLIP_INFO_PATH, "scene.cpickle")
        self.ACTOR_CPICKLE = os.path.join(self.CLIP_INFO_PATH, "actor.cpickle")
        self.SPEED_CPICKLE = os.path.join(self.CLIP_INFO_PATH, "speed.cpickle")

    def get_settings(self):
        return {
            'RESOURCES_PATH': self.RESOURCES_PATH,
            'RAW_VIDEO_PATH': self.RAW_VIDEO_PATH,
            'CLIP_INFO_PATH': self.CLIP_INFO_PATH,

            'INFO_CPICKLE': self.INFO_CPICKLE,
            'SCENE_CPICKLE': self.SCENE_CPICKLE,
            'ACTOR_CPICKLE': self.ACTOR_CPICKLE,
            'SPEED_CPICKLE': self.SPEED_CPICKLE
        }

    def check_resources(self):
        assert (os.path.isdir(self.RESOURCES_PATH)), "Path: Resources directory is not valid."
        assert (os.path.isdir(self.RAW_VIDEO_PATH)), "Path: Raw video directory is not valid."
        assert (os.path.isdir(self.CLIP_INFO_PATH)), "Path: Clip information directory is not valid."

        if os.path.exists(self.INFO_CPICKLE):
            assert (os.path.exists(self.INFO_CPICKLE)), "Path: Information file path is not valid."
            assert (os.path.exists(self.SCENE_CPICKLE)), "Path: Scene file path is not valid."
            assert (os.path.exists(self.ACTOR_CPICKLE)), "Path: Actor file path is not valid."
            assert (os.path.exists(self.SPEED_CPICKLE)), "Path: Speed file path is not valid."
        else:
            print "Path: Not found database files and will create new ones."

    def init_resources(self):
        if not os.path.isdir(self.RESOURCES_PATH):
            os.makedirs(self.RESOURCES_PATH)
        if not os.path.isdir(self.RAW_VIDEO_PATH):
            os.makedirs(self.RAW_VIDEO_PATH)
        if not os.path.isdir(self.CLIP_INFO_PATH):
            os.makedirs(self.CLIP_INFO_PATH)

        if not os.path.exists(self.INFO_CPICKLE):
            open(self.INFO_CPICKLE, 'w+').close()
            DataLoader.init_database(self.INFO_CPICKLE)
        if not os.path.exists(self.SCENE_CPICKLE):
            open(self.SCENE_CPICKLE, 'w+').close()
            DataLoader.init_database(self.SCENE_CPICKLE)
        if not os.path.exists(self.ACTOR_CPICKLE):
            open(self.ACTOR_CPICKLE, 'w+').close()
            DataLoader.init_database(self.ACTOR_CPICKLE)
        if not os.path.exists(self.SPEED_CPICKLE):
            open(self.SPEED_CPICKLE, 'w+').close()
            DataLoader.init_database(self.SPEED_CPICKLE)

    def get_raw_movie_path(self, movie_name):
        return os.path.join(self.RAW_VIDEO_PATH, movie_name + '.mov')

    def get_movie_workspace(self, movie_name):
        return {
            'ROOT': os.path.join(self.CLIP_INFO_PATH, movie_name),
            'CLIPS': os.path.join(self.CLIP_INFO_PATH, movie_name, 'clips'),
            'SCENES': os.path.join(self.CLIP_INFO_PATH, movie_name, 'scenes'),
            'ACTORS': os.path.join(self.CLIP_INFO_PATH, movie_name, 'actors'),
            'FACE_POOL': os.path.join(self.CLIP_INFO_PATH, movie_name, 'face_pool'),
            'SEARCH_POOL': os.path.join(self.CLIP_INFO_PATH, movie_name, 'search_pool')
        }

    def check_movie_workspace(self, movie_name):
        movie_paths = self.get_movie_workspace(movie_name)

        movie_root = movie_paths['ROOT']
        movie_clips = movie_paths['CLIPS']
        movie_scenes = movie_paths['SCENES']
        movie_actors = movie_paths['ACTORS']
        movie_face_pool = movie_paths['FACE_POOL']
        movie_search_pool = movie_paths['SEARCH_POOL']

        assert (os.path.isdir(movie_root)), "Movie path: Movie root path is not valid."
        assert (os.path.isdir(movie_clips)), "Movie Path: Movie clips path is not valid."
        assert (os.path.isdir(movie_scenes)), "Movie Path: Movie scenes path is not valid."
        assert (os.path.isdir(movie_actors)), "Movie Path: Movie actors path is not valid."
        assert (os.path.isdir(movie_face_pool)), "Movie Path: Movie face pool path is not valid."
        assert (os.path.isdir(movie_search_pool)), "Movie Path: Movie search pool path is not valid."

    def init_movie_workspace(self, movie_name):
        movie_paths = self.get_movie_workspace(movie_name)

        movie_root = movie_paths['ROOT']
        movie_clips = movie_paths['CLIPS']
        movie_scenes = movie_paths['SCENES']
        movie_actors = movie_paths['ACTORS']
        movie_face_pool = movie_paths['FACE_POOL']
        movie_search_pool = movie_paths['SEARCH_POOL']

        if not os.path.isdir(movie_root):
            os.makedirs(movie_root)
        else:
            clear_directory(movie_root)

        os.makedirs(movie_clips)
        os.makedirs(movie_scenes)
        os.makedirs(movie_actors)
        os.makedirs(movie_face_pool)
        os.makedirs(movie_search_pool)

    def get_raw_frame_path(self, movie_name, event_index, frame_index):
        event_directory = os.path.join(self.CLIP_INFO_PATH, movie_name, 'scenes', str(event_index))
        if not os.path.isdir(event_directory):
            os.makedirs(event_directory)
        return os.path.join(event_directory, str(frame_index) + ".png")

    def get_cascade_file_path(self):
        return os.path.join(self._forbidden_project_path, "source", "image_io", "haarcascade_frontalface_default.xml")

    def get_face_path(self, movie_name, event_index, frame_index, face_index):
        face_directory = os.path.join(self.CLIP_INFO_PATH, movie_name, 'actors', str(event_index))
        if not os.path.isdir(face_directory):
            os.makedirs(face_directory)
        return os.path.join(face_directory, str(frame_index) + "_" + str(face_index) + ".png")
