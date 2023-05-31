import os
import time


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def wait_download(path, name, max_time=1200):
    file_downloading = True
    t = 0

    while file_downloading:
        if name in os.listdir(path):
            file_downloading = False
        else:
            time.sleep(1)
            t += 1
            if t > max_time:
                raise TimeoutError(f'Download didn\'t finish after {str(max_time)} seconds')
    print(f'{name} ready to upload.')
