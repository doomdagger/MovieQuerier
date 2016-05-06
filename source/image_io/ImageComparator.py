import cv2
import numpy

from source.image_io.ImageEncoder import ImageEncoder
# from skimage.measure import structural_similarity as ssim


def normalize(vector):
    lower_bound = min(vector)
    upper_bound = max(vector)

    normalized_vector = [(element - lower_bound) / (upper_bound + 1e-10) for element in vector]
    return normalized_vector


def face_similarity(image_a, image_b):
    height, width = image_a.shape[:2]
    image_b = cv2.resize(image_b, (width, height))

    vector_a = normalize(image_a.ravel())
    vector_b = normalize(image_b.ravel())

    measurement = 0.0
    for index in range(0, len(vector_a) - 1):
        measurement += (vector_a[index] - vector_b[index]) ** 2
    return measurement / (height * width)


def histogram_scene_similarity(image_a, image_b):
    encoder = ImageEncoder()
    descriptor_a = encoder.encode_scene(image_a)
    descriptor_b = encoder.encode_scene(image_b)

    return 0.5 * numpy.sum([((a - b) ** 2) / (a + b + 1e-10) for (a, b) in zip(descriptor_a, descriptor_b)])


def histogram_face_similarity(image_a, image_b):
    encoder = ImageEncoder()
    descriptor_a = encoder.encode_face(image_a)
    descriptor_b = encoder.encode_face(image_b)

    return 0.5 * numpy.sum([((a - b) ** 2) / (a + b + 1e-10) for (a, b) in zip(descriptor_a, descriptor_b)])


def reshape_and_gray(image_a, image_b):
    image_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
    image_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)

    height, width = image_a.shape[:]
    image_b = cv2.resize(image_b, (width, height))

    return image_a, image_b


def mean_squared_distance(image_a, image_b):
    image_a, image_b = reshape_and_gray(image_a, image_b)
    distance = numpy.sum((image_a.astype("float") - image_b.astype("float")) ** 2)
    distance /= float(image_a.shape[0] * image_a.shape[1])

    return distance


# def structural_distance(image_a, image_b):
#     image_a, image_b = reshape_and_gray(image_a, image_b)
#     return ssim(image_a, image_b)


def corner_based_similarity(image_a, image_b):
    image_a, image_b = reshape_and_gray(image_a, image_b)

    lk_parameters = dict(winSize=(15, 15),
                         maxLevel=2,
                         criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    feature_parameters = dict(maxCorners=500, qualityLevel=0.3, minDistance=7, blockSize=7)

    corners = cv2.goodFeaturesToTrack(image_a, **feature_parameters)
    new_corners, st, err = cv2.calcOpticalFlowPyrLK(image_a, image_b, corners, None, **lk_parameters)
    chk_corners, st, err = cv2.calcOpticalFlowPyrLK(image_b, image_a, new_corners, None, **lk_parameters)
    status = abs(new_corners - chk_corners).reshape(-1, 2).max(-1) < 1

    similarity = 0
    for flag in status:
        if flag:
            similarity += 1
    return similarity
