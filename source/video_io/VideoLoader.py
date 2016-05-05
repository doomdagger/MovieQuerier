import os
import cv2


class VideoLoader:
    def __init__(self, path):
        assert (os.path.exists(path)), "Video Loader: Video path is not valid."
        assert (path.endswith(".mov")), "Video Loader: Video is not in mov format."

        self.PATH = path
        self.STREAM = cv2.VideoCapture(self.PATH)

        self.FPS = self.STREAM.get(cv2.CAP_PROP_FPS)
        self.FRAMES = int(self.STREAM.get(cv2.CAP_PROP_FRAME_COUNT))
        self.HEIGHT = int(self.STREAM.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.WIDTH = int(self.STREAM.get(cv2.CAP_PROP_FRAME_WIDTH))

    def __del__(self):
        self.STREAM.release()

    def get_path(self):
        return self.PATH

    def get_video_information(self):
        return {
            'PATH': self.PATH,
            'FPS': self.FPS,
            'FRAMES': self.FRAMES,
            'HEIGHT': self.HEIGHT,
            'WIDTH': self.WIDTH,
        }

    def reset(self):
        self.STREAM.release()
        self.STREAM = cv2.VideoCapture(self.PATH)

    def next_frame(self):
        if self.STREAM.isOpened():
            flag, frame = self.STREAM.read()
            if flag:
                return frame
        return None
