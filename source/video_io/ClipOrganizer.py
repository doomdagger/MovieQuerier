import scenedetect

from file_io.FileOperation import write_image
from image_io.PNG2GIF import generate_all_clips


class ClipOrganizer:
    def __init__(self, video):
        self.VIDEO = video
        self.BOUNDARIES = []
        self.FRAME_THRESHOLD = int(video.get_video_information()['FRAMES']/20)
        self.DETECTOR = [scenedetect.detectors.ContentDetector(threshold=50, min_scene_len=self.FRAME_THRESHOLD)]
        self.CUT_FPS, _ = scenedetect.detect_scenes_file(
            self.VIDEO.get_path(), self.BOUNDARIES, self.DETECTOR
        )

        self.BOUNDARIES.insert(0, 0)
        self.BOUNDARIES.append(self.VIDEO.get_video_information()['FRAMES'])

    def __del__(self):
        del self.VIDEO

    def get_frame_boundaries(self):
        return self.BOUNDARIES

    def get_millisecond_boundaries(self):
        return [(1000.0 * boundary) / float(self.CUT_FPS) for boundary in self.BOUNDARIES]

    def get_timestamp_boundaries(self):
        millisecond_boundaries = self.get_millisecond_boundaries()
        return [scenedetect.timecodes.get_string(boundary) for boundary in millisecond_boundaries]

    def extract_frames(self, movie_name, path_manager):
        event_index = 1
        frame_index = 0

        print "\tExtracting frames (total " + str(len(self.BOUNDARIES) - 1) + "):"
        while True:
            frame = self.VIDEO.next_frame()
            if frame is None:
                break
            if frame_index == self.BOUNDARIES[event_index]:
                print "\t\tCurrently processed: " + str(event_index)
                event_index += 1
            write_image(
                path_manager.get_raw_frame_path(movie_name, event_index, frame_index),
                frame
            )
            frame_index += 1
            if frame_index % 20 == 0:
                print "\t\t\t Extraction: Processed image " + str(frame_index)
        self.VIDEO.reset()

    @staticmethod
    def generate_clips(movie_name, path_manager, video_info):
        scenes_path = path_manager.get_movie_workspace(movie_name)['SCENES']
        clips_path = path_manager.get_movie_workspace(movie_name)['CLIPS']
        generate_all_clips(scenes_path, clips_path, video_info)
