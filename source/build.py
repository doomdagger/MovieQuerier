import os
import argparse

from database_io.DataLoader import DataLoader

from file_io.FileOperation import copy_file
from file_io.PathManager import PathManager
from file_io.PathAnalysis import get_movie_name

from image_io.FaceDetector import FaceDetector
from image_io.ImageOperation import build_face_pool_for_movie
from image_io.ImageOperation import build_search_pool_for_movie

from video_io.VideoLoader import VideoLoader
from video_io.ClipOrganizer import ClipOrganizer
from video_io.MovementTracker import MovementTracker

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("-m", "--movie", required=True, help="The path to the movie")

arguments = vars(argument_parser.parse_args())
assert (arguments["movie"] is not None), "Build: Must provide movie path."
assert (os.path.exists(arguments["movie"])), "Build: Movie path is not valid."

movie_path = arguments["movie"]
movie_name = get_movie_name(movie_path)

print "Analyzing Movie: " + movie_name + "..."

path_manager = PathManager()
path_manager.init_resources()
path_manager.check_resources()

print "Workspace is ready..."

copy_file(movie_path, path_manager.get_raw_movie_path(movie_name))
movie_path = path_manager.get_raw_movie_path(movie_name)

print "Step 1/10: Raw video has been moved to local resources..."

path_manager.init_movie_workspace(movie_name)
path_manager.check_movie_workspace(movie_name)

print "Step 2/10: Movie local workspace has been build..."

video = VideoLoader(movie_path)
clip_organizer = ClipOrganizer(video)

print "Step 3/10: Event boundary has been analyzed..."

clip_organizer.extract_frames(movie_name, path_manager)

print "Step 4/10: Raw frames has been extracted..."

clip_organizer.generate_clips(movie_name, path_manager, video.get_video_information())

print "Step 5/10: Even clips have been generated..."

build_search_pool_for_movie(movie_name, path_manager)

print "Step 6/10: Search pool has been built..."

face_detector = FaceDetector(path_manager.get_cascade_file_path())
face_detector.extract_faces(movie_name, path_manager)

print "Step 7/10: Faces have been detected..."

build_face_pool_for_movie(movie_name, path_manager)

print "Step 8/10: Face pool has been built..."

face_detector.remove_redundancy(movie_name, path_manager)

print "Step 9/10: Redundant faces have been removed..."

movement_tracker = MovementTracker()
movement_record = movement_tracker.analysis_movie(movie_name, path_manager)

print "Step 10/10: Movement information has been generated, and redundancy scene images have been removed..."

print "Storing all information..."

data_loader = DataLoader(movie_name, path_manager)
data_loader.load_data(
    movement_record,
    video.get_video_information(),
    clip_organizer.get_timestamp_boundaries(),
)

print "All information has been processed and stored..."
print "Movie " + movie_name + " has been successfully analyzed."
