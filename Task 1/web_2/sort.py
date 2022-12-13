import sys
import os
import shutil
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count


video_folder = ["avi", "mp4", "mov", "mkv", "gif"]
audio_folder = ["mp3", "ogg", "wav", "amr", "m4a", "wma"]
image_folder = ["jpeg", "png", "jpg", "svg"]
doc_folder = ["doc", "docx", "txt", "pdf", "xlsx", "pptx", "html", "scss", "css", "map"]
arch_folder = ["zip", "gz", "tar", "rar"]


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
    all_folder = []
    folders = [video_folder, audio_folder, image_folder, doc_folder, arch_folder]
    for fold in folders:
        all_folder.extend(fold)
    if file_ending not in all_folder:
        return True
    return False


def chek_error(handler):
    def wrapper(*args, **kwargs):
        try:
            handler(*args, **kwargs)
        except (shutil.ReadError):
            print(
                "Unfamiliar format. Archive, cannot be unpacked. Import an additional library."
            )

    return wrapper


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
    map = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "e",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "y",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "h",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "sch",
        "ъ": "",
        "ы": "y",
        "ь": "",
        "э": "e",
        "ю": "yu",
        "я": "ya",
        "і": "i",
        "є": "e",
        "ї": "i",
        "А": "A",
        "Б": "B",
        "В": "V",
        "Г": "G",
        "Д": "D",
        "Е": "E",
        "Ё": "E",
        "Ж": "h",
        "З": "Z",
        "И": "I",
        "Й": "Y",
        "К": "K",
        "Л": "L",
        "М": "M",
        "Н": "N",
        "О": "O",
        "П": "P",
        "Р": "R",
        "С": "S",
        "Т": "T",
        "У": "U",
        "Ф": "F",
        "Х": "H",
        "Ц": "Ts",
        "Ч": "Ch",
        "Ш": "Sh",
        "Щ": "Sch",
        "Ъ": "",
        "Ы": "Y",
        "Ь": "",
        "Э": "E",
        "Ю": "Yu",
        "Я": "Ya",
        "І": "I",
        "Є": "E",
        "Ї": "I",
    }

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

    video_path = os.path.join(main_path, "video")
    if not os.path.exists(video_path):
        os.makedirs(video_path)

    audio_path = os.path.join(main_path, "audio")
    if not os.path.exists(audio_path):
        os.makedirs(audio_path)

    images_path = os.path.join(main_path, "images")
    if not os.path.exists(images_path):
        os.makedirs(images_path)

    documents_path = os.path.join(main_path, "documents")
    if not os.path.exists(documents_path):
        os.makedirs(documents_path)

    archives_path = os.path.join(main_path, "archives")
    if not os.path.exists(archives_path):
        os.makedirs(archives_path)

    other_path = os.path.join(main_path, "other")
    if not os.path.exists(other_path):
        os.makedirs(other_path)

    return (
        video_path,
        audio_path,
        images_path,
        documents_path,
        archives_path,
        other_path,
    )


def file_handler(file):
    file_name_divide = file.split(".")
    file_ending = ""
    if len(file_name_divide) > 1:
        file_ending = file_name_divide[-1]
        return file_ending
    return None


def moving_video_file(main_path, video_path):
    for file in os.listdir(main_path):
        file_path = os.path.join(main_path, file)
        new_path = os.path.join(video_path, normalize(file))
        if find_video_file(file):
            os.replace(file_path, new_path)


def moving_audio_file(main_path, audio_path):
    for file in os.listdir(main_path):
        file_path = os.path.join(main_path, file)
        new_path = os.path.join(audio_path, normalize(file))
        if find_audio_file(file):
            os.replace(file_path, new_path)


def moving_image_file(main_path, images_path):
    for file in os.listdir(main_path):
        file_path = os.path.join(main_path, file)
        new_path = os.path.join(images_path, normalize(file))
        if find_image_file(file):
            os.replace(file_path, new_path)


def moving_document_file(main_path, documents_path):
    for file in os.listdir(main_path):
        file_path = os.path.join(main_path, file)
        new_path = os.path.join(documents_path, normalize(file))
        if find_doc_file(file):
            os.replace(file_path, new_path)


@chek_error
def moving_archive_file(main_path, archives_path):
    for file in os.listdir(main_path):
        file_path = os.path.join(main_path, file)
        new_path = os.path.join(archives_path, normalize(file))
        if find_arch_file(file):
            shutil.move(file_path, new_path)
            shutil.unpack_archive(
                new_path, os.path.join(archives_path, file.rstrip(file.split(".")[-1]))
            )


def moving_other_file(main_path, other_path):
    for file in os.listdir(main_path):
        file_path = os.path.join(main_path, file)
        new_path = os.path.join(other_path, normalize(file))
        if os.path.isfile(file_path):
            if find_other_file(file):
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


def fast_moving(
    video_path, audio_path, images_path, documents_path, archives_path, other_path
):
    thread1 = Thread(target=moving_video_file, args=(main_path, video_path))
    thread2 = Thread(target=moving_audio_file, args=(main_path, audio_path))
    thread3 = Thread(target=moving_image_file, args=(main_path, images_path))
    thread4 = Thread(target=moving_document_file, args=(main_path, documents_path))
    thread5 = Thread(target=moving_archive_file, args=(main_path, archives_path))
    thread6 = Thread(target=moving_other_file, args=(main_path, other_path))

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
    (
        video_path,
        audio_path,
        images_path,
        documents_path,
        archives_path,
        other_path,
    ) = path_handler()
    around_dir(main_path)

    fast_moving(
        video_path, audio_path, images_path, documents_path, archives_path, other_path
    )
    del_empty_dirs(main_path)
