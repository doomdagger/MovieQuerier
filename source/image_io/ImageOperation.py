import cv2

from source.file_io.FileOperation import write_image
from source.file_io.FileOperation import delete_file
from source.file_io.FileOperation import clear_images
from source.file_io.PathAnalysis import get_all_frames
from source.file_io.PathAnalysis import get_all_directories
from source.file_io.PathAnalysis import transform_face_pool_path
from source.file_io.PathAnalysis import transform_search_pool_path

from source.image_io.ImageComparator import face_similarity
from source.image_io.ImageComparator import histogram_face_similarity
from source.image_io.ImageComparator import histogram_scene_similarity


def get_brightness(image):
    return image.mean()


def get_standard_derivation(image):
    return image.std()


def modify_image(image):
    r_channel = image[:, :, 2]
    r_modified = cv2.equalizeHist(r_channel)

    g_channel = image[:, :, 1]
    g_modified = cv2.equalizeHist(g_channel)

    b_channel = image[:, :, 0]
    b_modified = cv2.equalizeHist(b_channel)

    image[:, :, 2] = r_modified
    image[:, :, 1] = g_modified
    image[:, :, 0] = b_modified

    return image


def build_search_pool_for_movie(movie_name, path_manager):
    movie_scene_path = path_manager.get_movie_workspace(movie_name)['SCENES']
    all_event_directories = get_all_directories(movie_scene_path)

    print "\tBuilding search pool (total " + str(len(all_event_directories)) + "):"
    print_index = 1
    for event_directory in all_event_directories:
        build_search_pool_for_event(event_directory)
        print "\t\tCurrently processed: " + str(print_index)
        print_index += 1


def build_search_pool_for_event(directory):
    all_scene_paths = get_all_frames(directory)

    scenes = []
    unique_scene_paths = []

    frame_index = 0
    all_indexes_string = " out of " + str(len(all_scene_paths))
    for scene_path in all_scene_paths:
        unique_flag = True
        target = cv2.imread(scene_path)

        if get_brightness(target) < 10:
            continue

        for scene in scenes:
            if histogram_scene_similarity(scene, target) < 0.2:
                unique_flag = False
                break

        if unique_flag:
            scenes.append(target)
            unique_scene_paths.append(transform_search_pool_path(scene_path))

        frame_index += 1
        if frame_index % 5 == 0:
            print "\t\t\t Build search pool: Processed image " + str(frame_index) + all_indexes_string

    for index in range(0, len(scenes)):
        write_image(unique_scene_paths[index], scenes[index])


def build_face_pool_for_movie(movie_name, path_manager):
    movie_face_path = path_manager.get_movie_workspace(movie_name)['ACTORS']
    all_face_directories = get_all_directories(movie_face_path)

    print "\tBuilding face pool (total " + str(len(all_face_directories)) + "):"
    print_index = 1
    for face_directory in all_face_directories:
        build_face_pool_for_event(face_directory)
        print "\t\tCurrently processed: " + str(print_index)
        print_index += 1


def build_face_pool_for_event(directory):
    all_face_paths = get_all_frames(directory)

    faces = []
    unique_face_paths = []

    frame_index = 0
    all_indexes_string = " out of " + str(len(all_face_paths))
    for face_path in all_face_paths:
        unique_flag = True
        target = cv2.imread(face_path)

        if get_brightness(target) < 10:
            continue

        for face in faces:
            if histogram_face_similarity(face, target) < 0.3:
                unique_flag = False
                delete_file(face_path)
                break

        if unique_flag:
            faces.append(target)
            unique_face_paths.append(transform_face_pool_path(face_path))

        frame_index += 1
        if frame_index % 5 == 0:
            print "\t\t\t Build face pool: Processed image " + str(frame_index) + all_indexes_string

    for index in range(0, len(faces)):
        write_image(unique_face_paths[index], faces[index])


def remove_similar_faces(directory):
    all_face_paths = get_all_frames(directory)

    faces = []
    unique_face_paths = []

    frame_index = 0
    all_indexes_string = " out of " + str(len(all_face_paths))
    for face_path in all_face_paths:
        unique_flag = True
        target = cv2.imread(face_path)

        for face in faces:
            if face_similarity(face, target) < 0.15:
                unique_flag = False
                break

        if unique_flag:
            faces.append(target)
            unique_face_paths.append(face_path)

        frame_index += 1
        if frame_index % 5 == 0:
            print "\t\t\t Remove redundant faces: Processed image " + str(frame_index) + all_indexes_string

    clear_images(directory)
    for index in range(0, len(faces)):
        cv2.imwrite(unique_face_paths[index], faces[index])

