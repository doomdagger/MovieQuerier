# from file_io.PathAnalysis import get_movie_name
# from file_io.FileOperation import clear_directory
#
# print path_manager.get_settings()
#
# # clear_directory(path_manager.get_settings()['RESOURCES_PATH'])
# # path_manager.init_resources()
#
# path_manager.check_resources()


# import cv2
# import numpy as np
# from matplotlib import pyplot as plt
#
# img = cv2.imread('/home/haoxiang/Desktop/1785.png')
#
# blur = cv2.GaussianBlur(img,(5,5),0)
#
# plt.subplot(121),plt.imshow(img),plt.title('Original')
# plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(blur),plt.title('Blurred')
# plt.xticks([]), plt.yticks([])
# plt.show()
#
# import cv2
#
# # load the image and show it
# image = cv2.imread('/home/haoxiang/Desktop/1785.png')
# cv2.imshow("original", image)
# cv2.waitKey(0)
#
# r = 100.0 / image.shape[1]
# dim = (100, int(image.shape[0] * r))
#
# # perform the actual resizing of the image and show it
# resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
# blur = cv2.GaussianBlur(resized, (5, 5), 0)
# cv2.imshow("blur", resized)
#
# cv2.waitKey(0)

# from image_io.PNG2GIF import generate_gif
# from image_io.PNG2GIF import generate_all_gif
# # generate_gif("/home/haoxiang/Desktop/MovieQuerier/resources/clip_information/test1/scenes/20", "/home/haoxiang/Desktop/MovieQuerier/resources/clip_information/test1/clips/20.gif")
# generate_all_gif("/home/haoxiang/Desktop/MovieQuerier/resources/clip_information/test1/scenes", "/home/haoxiang/Desktop/MovieQuerier/resources/clip_information/test1/clips/")

# from image_io.FaceDetector import FaceDetector
# import os
# import cv2
#
# image = cv2.imread("/home/haoxiang/Desktop/2.jpg")
#
# detector = FaceDetector()
# index = 0
# face_list = detector.get_faces(image)
#
# for face in face_list:
#     image_path = os.path.join("/home/haoxiang/Desktop", str(index)+".png")
#     cv2.imwrite(image_path, face)
#     index += 1
##########################


#
#
# face_detector.extract_faces("test1", path_manager)
# face_detector.extract_faces("test2", path_manager)
# face_detector.extract_faces("test3", path_manager)
# face_detector.extract_faces("test4", path_manager)
##########################
# from file_io.PathAnalysis import get_all_frames
# list = get_all_frames("/home/haoxiang/Desktop/MovieQuerier/resources/clip_information/test3/scenes/1")
# print list

# from video_io.MovementTracker import MovementTracker

# movement_tracker = MovementTracker()
# print movement_tracker.analysis_clip("/home/haoxiang/Desktop/MovieQuerier/resources/clip_information/test1/scenes/4")
# print movement_tracker.analysis_movie("test4", path_manager)


# from image_io.ImageOperation import modify_image
#
# image = cv2.imread("/home/haoxiang/Desktop/1792.png")
# modify_image(image)
# cv2.imshow("test", image)
# cv2.waitKey(0)


# import cv2
# from image_io.ImageOperation import get_brightness
# from image_io.ImageOperation import get_standard_derivation
# image = cv2.imread("/home/haoxiang/Desktop/192_0.png")
# print get_brightness(image)
# print get_standard_derivation(image)

# from file_io.PathManager import PathManager
# from image_io.FaceDetector import FaceDetector
#
# path_manager = PathManager()
# face_detector = FaceDetector(path_manager.get_cascade_file_path())
# face_detector.extract_faces("test3", path_manager)


# # from image_io.ImageComparator import mean_squared_distance
# # from image_io.ImageComparator import structural_distance
# # from image_io.ImageComparator import corner_based_similarity

# from image_io.ImageComparator import face_similarity
#

# import cv2
# from image_io.ImageComparator import histogram_face_similarity
# from image_io.ImageComparator import histogram_scene_similarity
#
# image_a = cv2.imread("/home/haoxiang/Desktop/1842.png")
# image_b = cv2.imread("/home/haoxiang/Desktop/65.png")
# print histogram_face_similarity(image_a, image_b)
# print histogram_scene_similarity(image_a, image_b)
# #
# from image_io.ImageOperation import remove_similar_faces
# remove_similar_faces("/home/haoxiang/Desktop/11")

# from image_io.ImageOperation import remove_similar_scenes
# remove_similar_scenes('/home/haoxiang/Desktop/MovieQuerier/resources/clip_information/test3/scenes/2')

# from file_io.PathAnalysis import transform_search_pool_path
# from file_io.FileOperation import write_image
#
# path = transform_search_pool_path('/home/haoxiang/Desktop/MovieQuerier/resources/clip_information/test3/scenes/2/20.png')
# print path
#
# write_image('/home/haoxiang/Desktop/1/1.png', image_a)
#
# from image_io.ImageOperation import build_face_pool_for_movie
#
# build_face_pool_for_movie("test2", path_manager)

# from file_io.PathAnalysis import get_last_directory_name
# print get_last_directory_name('/home/haoxiang/Desktop/MovieQuerier/resources/clip_information/test3/scenes/2')
from file_io.PathManager import PathManager
from database_io.DataLoader import DataLoader

# info = {'FRAMES': 2761, 'PATH': '/home/haoxiang/Desktop/test2.mov', 'WIDTH': 848, 'FPS': 23.976023976023978, 'HEIGHT': 360}
# boundaries = ['00:00:00.000', '00:00:00.166', '00:00:07.090', '00:00:08.967', '00:00:09.759', '00:00:11.011',
#               '00:00:12.012', '00:00:14.556', '00:00:16.349', '00:00:20.645', '00:00:36.703', '00:00:38.788',
#               '00:00:39.497', '00:00:40.373', '00:00:43.918', '00:00:46.880', '00:00:47.589', '00:00:48.214',
#               '00:00:49.382', '00:00:54.137', '00:00:54.846', '00:00:56.598', '00:00:59.017', '00:01:02.520',
#               '00:01:05.440', '00:01:07.609', '00:01:10.153', '00:01:14.240', '00:01:14.783', '00:01:16.409',
#               '00:01:20.580', '00:01:23.208', '00:01:24.459', '00:01:27.045', '00:01:29.297', '00:01:31.049',
#               '00:01:32.967', '00:01:35.386', '00:01:38.348', '00:01:39.682', '00:01:40.850', '00:01:44.646',
#               '00:01:45.313', '00:01:46.272', '00:01:49.025', '00:01:50.443', '00:01:50.985', '00:01:55.156']
# scene_frame = {'test2_34': 54, 'test2_35': 42, 'test2_36': 46, 'test2_37': 58, 'test2_30': 100, 'test2_31': 63,
#                'test2_32': 30, 'test2_33': 62, 'test2_38': 71, 'test2_39': 32, 'test2_1': 4, 'test2_2': 166,
#                'test2_3': 45, 'test2_4': 19, 'test2_5': 30, 'test2_6': 24, 'test2_7': 61, 'test2_8': 43, 'test2_9': 103,
#                'test2_46': 13, 'test2_44': 66, 'test2_42': 16, 'test2_47': 100, 'test2_43': 23, 'test2_27': 98,
#                'test2_26': 61, 'test2_25': 52, 'test2_24': 70, 'test2_23': 84, 'test2_22': 58, 'test2_21': 42,
#                'test2_20': 17, 'test2_41': 91, 'test2_29': 39, 'test2_28': 13, 'test2_45': 34, 'test2_40': 28,
#                'test2_18': 28, 'test2_19': 114, 'test2_12': 17, 'test2_13': 21, 'test2_10': 385, 'test2_11': 50,
#                'test2_16': 17, 'test2_17': 15, 'test2_14': 85, 'test2_15': 71}
# speed = {'test2_34': (54, 2, 154.77180480957031, 431.38552856445312, 764.89564514160156, 85.566299438476562),
#          'test2_35': (42, 1, 271.06733703613281, 281.16932678222656, 236.09553527832031, 370.8236083984375),
#          'test2_36': (46, 2, 226.19130706787109, 58.782432556152344, 210.83563232421875, 110.74699401855469),
#          'test2_37': (58, 2, 58.511871337890625, 39.73681640625, 157.21839141845703, 263.65921020507812),
#          'test2_30': (100, 5, 522.31163787841797, 241.33845520019531, 575.96986389160156, 198.15883636474609),
#          'test2_31': (63, 2, 899.59176254272461, 148.44570922851562, 24.613922119140625, 729.92410278320312),
#          'test2_32': (30, 1, 4.93756103515625, 6.6434555053710938, 23.026824951171875, 76.291351318359375),
#          'test2_33': (62, 2, 524.69124603271484, 301.53522491455078, 524.5203857421875, 834.68363952636719),
#          'test2_38': (71, 3, 355.31108856201172, 60.136039733886719, 157.62190246582031, 539.48763275146484),
#          'test2_39': (32, 1, 180.12000274658203, 657.58164978027344, 22.366943359375, 1436.8684692382812),
#          'test2_1': (4, 0, 2.05157470703125, 0.6890716552734375, 8.571044921875, 0),
#          'test2_2': (166, 14, 900.056884765625, 204.92119598388672, 4720.9363708496094, 343.97544860839844),
#          'test2_3': (45, 1, 99.731849670410156, 173.3868408203125, 1046.5516662597656, 133.18939208984375),
#          'test2_4': (19, 0, 5.0040130615234375, 0.22968292236328125, 5.1751708984375, 27.0914306640625),
#          'test2_5': (30, 1, 2.0873641967773438, 5.8693466186523438, 8.3826446533203125, 7.3431854248046875),
#          'test2_6': (24, 2, 31.160430908203125, 65.456130981445312, 69.221527099609375, 64.543701171875),
#          'test2_7': (61, 2, 69.301170349121094, 110.41194915771484, 67.342620849609375, 60.8310546875),
#          'test2_8': (43, 1, 101.80511474609375, 79.23736572265625, 107.1331787109375, 73.44598388671875),
#          'test2_45': (34, 1, 100.8118896484375, 11.348953247070312, 3.69976806640625, 126.614013671875),
#          'test2_46': (13, 1, 10.421066284179688, 15.372421264648438, 3.36993408203125, 10.12091064453125),
#          'test2_44': (66, 2, 389.20272827148438, 117.12340545654297, 978.69227600097656, 965.43804931640625),
#          'test2_42': (16, 0, 136.58372497558594, 80.055091857910156, 349.44184112548828, 106.09188842773438),
#          'test2_47': (100, 3, 488.52204132080078, 858.98495483398438, 1845.0528106689453, 82.248123168945312),
#          'test2_9': (103, 4, 397.97628021240234, 694.24040222167969, 613.36499786376953, 605.24082183837891), 'test2_43': (23, 1, 14.547920227050781, 6.9580078125, 183.40034484863281, 0.454742431640625), 'test2_27': (98, 3, 1557.7474365234375, 5131.4943161010742, 3138.0162353515625, 2205.633056640625), 'test2_26': (61, 2, 190.66339111328125, 449.14435577392578, 568.10940551757812, 355.80245971679688), 'test2_25': (52, 1, 246.14712524414062, 772.66084289550781, 1257.7440185546875, 65.0892333984375), 'test2_24': (70, 3, 1175.8788833618164, 2806.3232078552246, 2495.0010299682617, 2317.9371204376221), 'test2_23': (84, 3, 758.35970306396484, 417.31131744384766, 2434.9304046630859, 477.35577392578125), 'test2_22': (58, 2, 872.2240047454834, 399.84823417663574, 942.37321472167969, 695.98440551757812), 'test2_21': (42, 1, 91.909835815429688, 26.029510498046875, 50.42718505859375, 179.27641296386719), 'test2_20': (17, 1, 413.16220855712891, 440.2340087890625, 209.84500122070312, 675.55157470703125), 'test2_41': (91, 4, 148.36608123779297, 361.1495361328125, 747.02154541015625, 364.7607421875), 'test2_29': (39, 1, 330.34086608886719, 997.33106994628906, 472.96159362792969, 403.98858642578125), 'test2_28': (13, 0, 8.130584716796875, 28.736007690429688, 0.17498779296875, 29.4559326171875), 'test2_40': (28, 1, 29.26513671875, 6.3108978271484375, 1.8574981689453125, 253.6446533203125), 'test2_18': (28, 1, 17.872413635253906, 764.59992218017578, 69.16650390625, 88.458206176757812), 'test2_19': (114, 4, 804.96721649169922, 209.6278076171875, 609.69142913818359, 437.26837921142578), 'test2_12': (17, 0, 98.229354858398438, 0, 118.13650512695312, 0), 'test2_13': (21, 1, 10.202857971191406, 0.05084228515625, 7.525726318359375, 4.213714599609375), 'test2_10': (385, 12, 1789.6760787963867, 5236.0790176391602, 9862.1717720031738, 4155.9580764770508), 'test2_11': (50, 1, 2773.5534272193909, 15.269218444824219, 56.345184326171875, 4441.7691650390625), 'test2_16': (17, 0, 11.940834045410156, 478.52922821044922, 326.36544799804688, 6.0676345825195312), 'test2_17': (15, 0, 184.93821716308594, 0, 29.17095947265625, 0), 'test2_14': (85, 1, 1041.7076950073242, 460.57587432861328, 710.6326904296875, 532.87286376953125), 'test2_15': (71, 1, 460.83077239990234, 254.16820526123047, 493.00666809082031, 318.118896484375)}

# path_manager = PathManager()
# data_loader = DataLoader("test2", path_manager)
# data_loader.check_movie_information()
# data_loader.check_speed_information()
# data_loader.check_scene_information()
# data_loader.check_actor_information()

# import os
# import argparse
#
# from file_io.FileOperation import copy_file
# from file_io.PathManager import PathManager
# from file_io.PathAnalysis import get_movie_name
#
# from image_io.FaceDetector import FaceDetector
# from image_io.ImageOperation import build_face_pool_for_movie
# from image_io.ImageOperation import build_search_pool_for_movie
#
# from video_io.VideoLoader import VideoLoader
# from video_io.ClipOrganizer import ClipOrganizer
# from video_io.MovementTracker import MovementTracker
#
# path_manager = PathManager()
# video = VideoLoader("/home/haoxiang/Desktop/test2.mov")
# clip_organizer = ClipOrganizer(video)
# event_frame_number = clip_organizer.extract_frames("test2", path_manager)
# movement_tracker = MovementTracker()
# movement_record = movement_tracker.analysis_movie("test2", path_manager)
#
# print video.get_video_information()
# print clip_organizer.get_frame_boundaries()
# print clip_organizer.get_millisecond_boundaries()
# print clip_organizer.get_timestamp_boundaries()
# print event_frame_number
# print movement_record

# from interface import Interface
from file_io.PathAnalysis import get_movie_event

# interface = Interface("D:\\MovieQuerier")
# print interface._get_settings()
# print interface._get_movie_workspace("thefirstmondayinmay-tlr1_h480p")
# print interface.get_all_movie_names()
# print interface.get_raw_movie_path("thefirstmondayinmay-tlr1_h480p")
# print interface.get_all_keys("thefirstmondayinmay-tlr1_h480p")
# print len(interface.get_all_clip_paths("thefirstmondayinmay-tlr1_h480p"))
# print get_movie_event('thefirstmondayinmay-tlr1_h480p_1')
# print interface.get_face_paths('thefirstmondayinmay-tlr1_h480p_2')
# print interface.get_scene_paths('test2_24')
# print interface.get_clip_path('thefirstmondayinmay-tlr1_h480p_1')
# print len(interface.get_scene_descriptor("/home/haoxiang/Desktop/1670_0.png"))
# a = interface.get_scene_descriptor("/home/haoxiang/Desktop/95.png")
# b = interface.get_scene_descriptor("/home/haoxiang/Desktop/1157.png")
# print interface.compare_descriptor(a, b)
# a = interface.get_face_descriptor("/home/haoxiang/Desktop/1.jpg", unique=True)
# b = interface.get_face_descriptor("/home/haoxiang/Desktop/1670_0.png")
# print interface.compare_descriptor(a, b)
#
# from image_io.PNG2GIF import generate_clip
# generate_clip('D:\\MovieQuerier\\resources\\clip_information\\thefirstmondayinmay-tlr1_h480p\\scenes\\4\\',
#              'D:\\MovieQuerier\\resources\\clip_information\\thefirstmondayinmay-tlr1_h480p\\scenes\\4\\test.avi',
#               848, 480)


# from file_io.PathAnalysis import get_all_frames
# from imutils.video import VideoStream
# import numpy as np
# import argparse
# import imutils
# import time
# import cv2
#
# writer = cv2.VideoWriter(
#     'D:\\MovieQuerier\\resources\\clip_information\\thefirstmondayinmay-tlr1_h480p\\scenes\\4\\test.avi',
#     cv2.cv.FOURCC('M', 'J', 'P', 'G'), 20, (848, 480), True)
# for path in get_all_frames('D:\\MovieQuerier\\resources\\clip_information\\thefirstmondayinmay-tlr1_h480p\\scenes\\4'):
#     frame = cv2.imread(path)
#     writer.write(frame)
# writer.release()

# from file_io.PathManager import PathManager
# from image_io.ImageOperation import build_search_pool_for_movie
#
# path_manager = PathManager()
# build_search_pool_for_movie("thefirstmondayinmay-tlr1_h480p", path_manager)

# from video_io.VideoLoader import VideoLoader
# from video_io.ClipOrganizer import ClipOrganizer
# from file_io.PathAnalysis import get_all_movies
# from file_io.PathAnalysis import get_movie_name
# from file_io.FileOperation import copy_file
#
# all_movie = get_all_movies('D:\\MovieQuerier\\data')
# for movie in all_movie:
#     name = get_movie_name(movie)
#     holder = VideoLoader(movie)
#     orginazer = ClipOrganizer(holder)
#     boundaries = len(orginazer.get_frame_boundaries())
#     print boundaries
#     if boundaries > 7:
#         copy_file(movie, 'D:\\MovieQuerier\\good\\' + name + ".mov")

# import cPickle
#
# db_file = open("/home/lihe/Desktop/resources/clip_information/info.cpickle", 'r')
# db = cPickle.load(db_file)
# db_file.close()
# print db

from interface import Interface

interface = Interface("/home/lihe/Desktop/MovieQuerier")
# print len(interface.get_scene_data())
# print len(interface.get_actor_data())
# print len(interface.get_info_data())
# print interface.get_speed_data()
# print interface.get_info_data()

a = interface.get_scene_descriptor("/home/lihe/Desktop/1366.png")
b = interface.get_scene_descriptor("/home/lihe/Desktop/1142.png")
print interface.compare_descriptor(a, b)

test = interface.get_scene_data()
print len(test["45years-tlr1_h480p_6"])
for index in test["45years-tlr1_h480p_6"]:
    print interface.compare_descriptor(a, index)
