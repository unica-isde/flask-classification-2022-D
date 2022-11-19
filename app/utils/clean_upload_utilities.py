import os
from threading import Thread
from config import Configuration
import time

conf = Configuration()


def clean_uploads():
    for file in os.listdir(conf.upload_folder_path):
        os.remove(os.path.join(conf.upload_folder_path, file))


def __delete_file(filename):
    time.sleep(conf.delete_upload_delay)
    os.remove(os.path.join(conf.upload_folder_path, filename))


def delete_after_a_while(filename):
    thread = Thread(target=__delete_file, args=(filename,))
    thread.start()
