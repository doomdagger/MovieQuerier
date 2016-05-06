import cv2
import cPickle

from source.file_io.PathAnalysis import get_key
from source.file_io.PathAnalysis import get_all_frames
from source.file_io.PathAnalysis import get_all_directories
from source.file_io.PathAnalysis import get_last_directory_name

from source.image_io.ImageEncoder import ImageEncoder


class DataLoader:
    def __init__(self, movie_name, path_manager):
        self.MOVIE_NAME = movie_name
        self.ENCODER = ImageEncoder()

        self.INFO_DB = path_manager.get_settings()['INFO_CPICKLE']
        self.SCENE_DB = path_manager.get_settings()['SCENE_CPICKLE']
        self.ACTOR_DB = path_manager.get_settings()['ACTOR_CPICKLE']
        self.SPEED_DB = path_manager.get_settings()['SPEED_CPICKLE']
        self.DBS = [self.INFO_DB, self.SCENE_DB, self.ACTOR_DB, self.SPEED_DB]

        self.FACE_POOL = path_manager.get_movie_workspace(movie_name)['FACE_POOL']
        self.SEARCH_POOL = path_manager.get_movie_workspace(movie_name)['SEARCH_POOL']

    @staticmethod
    def init_database(db_path):
        db = {}
        db_file = open(db_path, 'w')
        db_file.write(cPickle.dumps(db))
        db_file.close()

    def load_data(self, movement_record, video_info, boundaries):
        print "\tStoring movie information..."
        info_db = DataLoader.parse_movie_information(self.MOVIE_NAME, video_info, boundaries)
        self.merge_movie_information(info_db)
        print "\tStoring speed information..."
        speed_db = DataLoader.parse_speed_information(movement_record)
        self.merge_speed_information(speed_db)
        print "\tStoring scene information..."
        self.merge_scene_information()
        print "\tStoring actor information..."
        self.merge_actor_information()

    def check_movie_information(self):
        db_file = open(self.INFO_DB, 'r')
        db = cPickle.load(db_file)
        db_file.close()

        print len(db)

    def check_speed_information(self):
        db_file = open(self.SPEED_DB, 'r')
        db = cPickle.load(db_file)
        db_file.close()

        print len(db)

    def check_scene_information(self):
        db_file = open(self.SCENE_DB, 'r')
        db = cPickle.load(db_file)
        db_file.close()

        print len(db)

    def check_actor_information(self):
        db_file = open(self.ACTOR_DB, 'r')
        db = cPickle.load(db_file)
        db_file.close()

        print len(db)

    def load_info_data(self):
        db_file = open(self.INFO_DB, 'r')
        db = cPickle.load(db_file)
        db_file.close()
        return db

    def load_scene_data(self):
        db_file = open(self.SCENE_DB, 'r')
        db = cPickle.load(db_file)
        db_file.close()
        return db

    def load_actor_data(self):
        db_file = open(self.ACTOR_DB, 'r')
        db = cPickle.load(db_file)
        db_file.close()
        return db

    def load_speed_data(self):
        db_file = open(self.SPEED_DB, 'r')
        db = cPickle.load(db_file)
        db_file.close()
        return db

    @staticmethod
    def parse_movie_information(movie_name, video_info, boundaries):
        fps = video_info['FPS']
        width = video_info['WIDTH']
        height = video_info['HEIGHT']

        info = {}
        clip_number = len(boundaries)
        for index in range(1, clip_number):
            info[get_key(movie_name, index)] = (fps, width, height, boundaries[index - 1], boundaries[index])
        return info

    def merge_movie_information(self, info):
        db_file = open(self.INFO_DB, 'r')
        db = cPickle.load(db_file)
        db_file.close()

        for key, value in info.iteritems():
            db[key] = value

        db_file = open(self.INFO_DB, 'w')
        db_file.write(cPickle.dumps(db))
        db_file.close()

    @staticmethod
    def parse_speed_information(movement_record):
        speed = {}
        for key, (frames, cuts, up_move, down_move, left_move, right_move) in movement_record.iteritems():
            speed[key] = (frames, 100 * float(cuts)/frames,
                          (up_move + down_move + left_move + right_move) / (frames * 4))
        return speed

    def merge_speed_information(self, speed):
        db_file = open(self.SPEED_DB, 'r')
        db = cPickle.load(db_file)
        db_file.close()

        for key, value in speed.iteritems():
            db[key] = value

        db_file = open(self.SPEED_DB, 'w')
        db_file.write(cPickle.dumps(db))
        db_file.close()

    def merge_scene_information(self):
        db_file = open(self.SCENE_DB, 'r')
        db = cPickle.load(db_file)
        db_file.close()

        for event_directory in get_all_directories(self.SEARCH_POOL):
            event_index = get_last_directory_name(event_directory)
            event_scene_codes = []

            for scene in get_all_frames(event_directory):
                image = cv2.imread(scene)
                code = self.ENCODER.encode_scene(image)
                event_scene_codes.append(code)

            db[get_key(self.MOVIE_NAME, event_index)] = event_scene_codes

        db_file = open(self.SCENE_DB, 'w')
        db_file.write(cPickle.dumps(db))
        db_file.close()

    def merge_actor_information(self):
        db_file = open(self.ACTOR_DB, 'r')
        db = cPickle.load(db_file)
        db_file.close()

        for event_directory in get_all_directories(self.FACE_POOL):
            event_index = get_last_directory_name(event_directory)
            event_face_codes = []

            for face in get_all_frames(event_directory):
                image = cv2.imread(face)
                code = self.ENCODER.encode_face(image)
                event_face_codes.append(code)

            db[get_key(self.MOVIE_NAME, event_index)] = event_face_codes

        db_file = open(self.ACTOR_DB, 'w')
        db_file.write(cPickle.dumps(db))
        db_file.close()
