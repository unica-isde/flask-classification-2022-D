import os
from threading import Thread
from config import Configuration
import time

conf = Configuration()


def clean_uploads():
    """This function clean the "image_upload" folder."""
    for file in os.listdir(conf.upload_folder_path):
        os.remove(os.path.join(conf.upload_folder_path, file))


def __delete_file(filename):  # private function. Not meant to be used outside this file. Like at all.
    #  the following instruction is the reason. Calling this function in the main thread would block the software
    #  for many seconds.
    time.sleep(conf.delete_upload_delay)
    os.remove(os.path.join(conf.upload_folder_path, filename))


def delete_after_a_while(filename):
    """Delete the file with name "filename" after a time defined in the configuration file (delete_upload_delay)."""
    thread = Thread(target=__delete_file, args=(filename,))
    thread.start()
