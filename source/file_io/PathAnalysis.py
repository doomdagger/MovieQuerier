import os
import glob
import ntpath


def get_key(movie_name, event_index):
    return movie_name + '_' + str(event_index)


def get_movie_event(key):
    words = key.rsplit('_', 1)
    assert (len(words) == 2), "Parse key: Key error."
    return words[0], words[1]


def get_frame_name(path):
    file_name = ntpath.basename(path)
    extension_index = file_name.rfind('.')
    return file_name[:extension_index]


def get_movie_name(path):
    file_name = ntpath.basename(path)
    extension_index = file_name.rfind('.')
    return file_name[:extension_index]


def get_last_directory_name(path):
    return os.path.basename(os.path.normpath(path))


def get_all_frames(path):
    all_frames = []
    match_pattern = os.path.join(path, "*.png")
    for frame_path in glob.glob(match_pattern):
        all_frames.append(frame_path)
    all_frames.sort()
    return all_frames


def get_all_clips(path):
    all_clips = []
    match_pattern = os.path.join(path, "*.mp4")
    for GIF_path in glob.glob(match_pattern):
        all_clips.append(GIF_path)
    all_clips.sort()
    return all_clips


def get_all_movies(path):
    all_movies = []
    match_pattern = os.path.join(path, "*.mov")
    for movie_path in glob.glob(match_pattern):
        all_movies.append(movie_path)
    all_movies.sort()
    return all_movies


def get_all_directories(path):
    all_directories = []
    for target in os.listdir(path):
        if target[0] is '.':
            continue
        directory_path = os.path.join(path, target)
        try:
            if os.path.isdir(directory_path):
                all_directories.append(directory_path)
        except Exception as e:
            print e
    all_directories.sort()
    return all_directories


def transform_face_pool_path(path):
    face_pool_path = path[::-1]
    face_pool_path = face_pool_path.replace('srotca', "loop_ecaf", 1)
    face_pool_path = face_pool_path[::-1]
    return face_pool_path


def transform_search_pool_path(path):
    search_pool_path = path[::-1]
    search_pool_path = search_pool_path.replace('senecs', "loop_hcraes", 1)
    search_pool_path = search_pool_path[::-1]
    return search_pool_path
