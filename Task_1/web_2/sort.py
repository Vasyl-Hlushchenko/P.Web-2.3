import sys
import os
import shutil
from threading import Thread
from data import *


def chek_error(handler):
    def wrapper(*args, **kwargs):
        try:
            handler(*args, **kwargs)
        except (shutil.ReadError):
            print(
                "Unfamiliar format. Archive, cannot be unpacked. Import an additional library."
            )

    return wrapper


def find_video_file(file):
    file_ending = file_handler(file)
    if file_ending in video_folder:
        return True
    return False


def find_audio_file(file):
    file_ending = file_handler(file)
    if file_ending in audio_folder:
        return True
    return False


def find_image_file(file):
    file_ending = file_handler(file)
    if file_ending in image_folder:
        return True
    return False


def find_doc_file(file):
    file_ending = file_handler(file)
    if file_ending in doc_folder:
        return True
    return False


def find_arch_file(file):
    file_ending = file_handler(file)
    if file_ending in arch_folder:
        return True
    return False


def find_other_file(file):
    file_ending = file_handler(file)
    if file_ending not in all_ending_folder:
        path_to_file = os.path.join(main_path, file)
        if os.path.isfile(path_to_file):
            return True
        return False


def get_main_path():
    main_path = ""
    args = sys.argv
    if len(args) == 1:
        main_path = input("Enter path to your folder: ")
    else:
        main_path = args[1]
    while True:
        if not os.path.exists(main_path):
            if main_path:
                print(f"{main_path} not exist")
            main_path = input("Enter path to your folder: ")
        else:
            if os.path.isdir(main_path):
                break
            else:
                print(f"{main_path} this is not a folder")
                main_path = ""
    return main_path


def normalize(file):
    lists = file.split(".")
    name_file = ".".join(lists[0:-1])
    new_name = ""
    for el in name_file:
        if el in map:
            new_name += map[el]
        elif (
            (ord("A") <= ord(el) <= ord("Z"))
            or (ord("a") <= ord(el) <= ord("z"))
            or el.isdigit()
        ):
            new_name += el
        else:
            new_name += "_"
    return new_name + "." + lists[-1]


def path_handler():
    for elem in handler:
        new_folder = os.path.join(main_path, elem)
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
    return None


def file_handler(file):
    file_name_divide = file.split(".")
    file_ending = ""
    if len(file_name_divide) > 1:
        file_ending = file_name_divide[-1]
        return file_ending
    return None


@chek_error
def moving_file(value, find_function):
    for file in os.listdir(main_path):
        file_path = os.path.join(main_path, file)
        new_path = os.path.join(os.path.join(main_path, value), normalize(file))
        if find_function(file):
            if value == "archives":
                shutil.move(file_path, new_path)
                shutil.unpack_archive(
                    new_path,
                    os.path.join(
                        os.path.join(main_path, value), file.rstrip(file.split(".")[-1])
                    ),
                )
            else:
                os.replace(file_path, new_path)


def around_dir(main_path):
    for dir in os.listdir(main_path):
        dir_path = os.path.join(main_path, dir)
        if os.path.isdir(dir_path):
            for file in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file)
                if os.path.isdir(file_path):
                    around_dir(file_path)
                else:
                    shutil.move(file_path, main_path)


def del_empty_dirs(main_path):
    for dir in os.listdir(main_path):
        dirs_path = os.path.join(main_path, dir)
        if os.path.isdir(dirs_path):
            del_empty_dirs(dirs_path)
            if not os.listdir(dirs_path):
                os.rmdir(dirs_path)
    return None


def fast_moving():
    thread1 = Thread(target=moving_file, args=("video", find_video_file))
    thread2 = Thread(target=moving_file, args=("audio", find_audio_file))
    thread3 = Thread(target=moving_file, args=("images", find_image_file))
    thread4 = Thread(target=moving_file, args=("documents", find_doc_file))
    thread5 = Thread(target=moving_file, args=("archives", find_arch_file))
    thread6 = Thread(target=moving_file, args=("other", find_other_file))

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    thread6.join()


if __name__ == "__main__":
    main_path = get_main_path()
    path_handler()
    around_dir(main_path)
    fast_moving()
    del_empty_dirs(main_path)
