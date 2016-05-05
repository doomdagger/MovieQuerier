import os
import cv2

from file_io.PathAnalysis import get_all_frames
from file_io.PathAnalysis import get_all_directories
from file_io.PathAnalysis import get_last_directory_name


def generate_clip(directory, copy_to_path, width, height):
    assert (os.path.isdir(directory)), "PNG to AVI: Path is not valid."

    writer = cv2.VideoWriter(copy_to_path, cv2.cv.FOURCC('M', 'J', 'P', 'G'), 20, (width, height), True)

    frame_index = 0
    all_indexes_string = " out of " + str(len(get_all_frames(directory)))
    for path in get_all_frames(directory):
        frame = cv2.imread(path)
        writer.write(frame)

        frame_index += 1
        if frame_index % 20 == 0:
            print "\t\t\t Generate clips: Processed image " + str(frame_index) + all_indexes_string
    writer.release()


def generate_all_clips(root_directory, copy_to_directory, video_info):
    assert (os.path.isdir(root_directory)), "PNG to AVI: Path is not valid."
    assert (os.path.isdir(copy_to_directory)), "PNG to AVI: Path is not valid."

    directories = get_all_directories(root_directory)
    print "\tGenerating AVIs (total " + str(len(directories)) + "):"
    event_index = 1
    for directory in directories:
        avi_name = get_last_directory_name(directory) + ".avi"
        copy_to_path = os.path.join(copy_to_directory, avi_name)
        generate_clip(directory, copy_to_path, video_info['WIDTH'], video_info['HEIGHT'])
        print "\t\tCurrently processed: " + str(event_index)
        event_index += 1
