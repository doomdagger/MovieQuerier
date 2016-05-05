import cv2
import numpy

from file_io.PathAnalysis import get_key
from file_io.PathAnalysis import get_last_directory_name

from file_io.PathAnalysis import get_all_frames
from file_io.PathAnalysis import get_all_directories

from file_io.FileOperation import clear_images


class MovementTracker:
    def __init__(self):
        self.LK_PARAMETERS = dict(winSize=(15, 15),
                                  maxLevel=2,
                                  criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        self.FEATURE_PARAMETERS = dict(maxCorners=500, qualityLevel=0.3, minDistance=7, blockSize=7)
        self.LOWER_THRESHOLD = 1
        self.UPPER_THRESHOLD = 5
        self.LONG_TRACK_THRESHOLD = 5
        self.BOUNDARY_TRACK_THRESHOLD = 5

        self.SAMPLE_ALERT = 10
        self.SAMPLE_RATIO = 10

        self.BOUNDARY_VERTICAL = 1.0 / 4.0
        self.BOUNDARY_HORIZONTAL = 1.0 / 8.0

    def analysis_movie(self, movie_name, path_manager):
        movie_scene_path = path_manager.get_movie_workspace(movie_name)['SCENES']
        all_events_directories = get_all_directories(movie_scene_path)

        record = {}
        print "\tAnalyzing movement (total " + str(len(all_events_directories)) + "):"
        print_index = 1
        for event_directory in all_events_directories:
            event_index = get_last_directory_name(event_directory)
            record[get_key(movie_name, event_index)] = self.analysis_clip(event_directory)
            print "\t\tCurrently processed: " + str(print_index)
            print_index += 1
        return record

    def analysis_clip(self, clip_directory):
        frame_paths = get_all_frames(clip_directory)
        assert (len(frame_paths)), "Movie analysis: Directory contains no frames."

        pre_gray_frame = None

        frame_index = 0
        record_flag = True

        tracks = []
        scene_paths = []

        up_move = 0
        down_move = 0
        left_move = 0
        right_move = 0

        while frame_index < len(frame_paths):
            frame = cv2.imread(frame_paths[frame_index])
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            (height, width) = gray_frame.shape[:]
            mask = numpy.zeros_like(gray_frame)
            mask[
                round(height * self.BOUNDARY_VERTICAL):round(height * (1.0 - self.BOUNDARY_VERTICAL)),
                round(width * self.BOUNDARY_HORIZONTAL):round(width * (1.0 - self.BOUNDARY_HORIZONTAL))
            ] = 255

            if len(tracks) > 0:
                lst_track_points = numpy.float32([track[-1] for track in tracks]).reshape(-1, 1, 2)

                now_track_points, st, err = cv2.calcOpticalFlowPyrLK(pre_gray_frame, gray_frame, lst_track_points,
                                                                     None, **self.LK_PARAMETERS)

                chk_track_points, st, err = cv2.calcOpticalFlowPyrLK(gray_frame, pre_gray_frame, now_track_points,
                                                                     None, **self.LK_PARAMETERS)

                status = abs(lst_track_points - chk_track_points).reshape(-1, 2).max(-1) < 1
                new_tracks = []

                if all(flag is False for flag in status):
                    tracks = []
                else:
                    for old_track, (x, y), flag in zip(tracks, now_track_points.reshape(-1, 2), status):
                        if not flag:
                            continue

                        old_x, old_y = old_track[-1]
                        displacement = abs(old_x - x) + abs(old_y - y)
                        if displacement > self.LOWER_THRESHOLD or displacement < self.UPPER_THRESHOLD:
                            old_track.append((x, y))
                            new_tracks.append(old_track)
                            if old_x < x:
                                right_move += x - old_x
                            else:
                                left_move += old_x - x

                            if old_y < y:
                                down_move += y - old_y
                            else:
                                up_move += old_y - y

                    tracks = new_tracks

            if len(tracks) <= self.SAMPLE_ALERT or frame_index % self.SAMPLE_RATIO == 0:
                new_points = cv2.goodFeaturesToTrack(gray_frame, mask=mask, **self.FEATURE_PARAMETERS)

                if new_points is not None:
                    for x, y in numpy.float32(new_points).reshape(-1, 2):
                        tracks.append([(x, y)])

            if len(tracks) > 0:
                long_track = 0
                for track in tracks:
                    if len(track) > self.LONG_TRACK_THRESHOLD:
                        long_track += 1
                if long_track > self.BOUNDARY_TRACK_THRESHOLD and record_flag:
                    scene_paths.append(frame_paths[frame_index])
                    record_flag = False
                elif long_track < 2:
                    record_flag = True

            frame_index += 1
            pre_gray_frame = gray_frame

            if frame_index % 10 == 0:
                print "\t\t\t Analyse movement: Processed image " + str(frame_index) + " out of " + str(len(frame_paths))

        self.extract_scenes(clip_directory, scene_paths)
        return len(frame_paths), len(scene_paths), up_move, down_move, left_move, right_move

    @staticmethod
    def extract_scenes(clip_directory, scene_paths):
        images = []

        if len(scene_paths) == 0:
            clear_images(clip_directory, keep_one=True)
            return

        for scene_path in scene_paths:
            images.append(cv2.imread(scene_path))

        clear_images(clip_directory)

        for index in range(0, len(scene_paths)):
            cv2.imwrite(scene_paths[index], images[index])
