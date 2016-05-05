import os
import cv2
import shutil


def clear_images(path, keep_one=False):
    assert (os.path.isdir(path)), "Clear images: Path is not valid."

    for target in os.listdir(path):
        sub_path = os.path.join(path, target)
        try:
            if os.path.isfile(sub_path) and target.endswith(".png"):
                if keep_one:
                    keep_one = False
                    continue
                os.unlink(sub_path)
        except Exception as e:
            print "Clear images: Error."
            print e


def clear_directory(path, recursive=True):
    assert (os.path.isdir(path)), "Clear directory: Path is not valid."

    for target in os.listdir(path):
        sub_path = os.path.join(path, target)

        try:
            if os.path.isfile(sub_path):
                os.unlink(sub_path)
            elif os.path.isdir(sub_path) and recursive:
                shutil.rmtree(sub_path)
        except Exception as e:
            print "Clear directory: Error."
            print e


def delete_file(path):
    assert (os.path.exists(path)), "Delete file: Path is not valid."
    os.remove(path)


def copy_file(path_from, path_to):
    assert (os.path.exists(path_from)), "Copy file: From path is not valid."
    assert (os.path.isdir(os.path.dirname(path_to))), "Copy file: To path is not valid."
    shutil.copyfile(path_from, path_to)


def move_file(path_from, path_to):
    copy_file(path_from, path_to)
    os.remove(path_from)


def write_image(path, image):
    if not os.path.isdir(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    cv2.imwrite(path, image)
