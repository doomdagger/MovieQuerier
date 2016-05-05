import cv2


class ImageEncoder:
    def __init__(self):
        self.SCENE_BINS = [8, 8, 8]
        self.FACE_BINS = [16, 16, 16]

    def encode_scene(self, image):
        histogram = cv2.calcHist(
            [image], [0, 1, 2], None,
            self.SCENE_BINS, [0, 256, 0, 256, 0, 256]
        )
        cv2.normalize(histogram, histogram)
        return histogram.flatten()

    def encode_face(self, image):
        histogram = cv2.calcHist(
            [image], [0, 1, 2], None,
            self.FACE_BINS, [0, 256, 0, 256, 0, 256]
        )
        cv2.normalize(histogram, histogram)
        return histogram.flatten()
