import logging
import os
import sys
import time
import uuid
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler


PATH = 'C:\\Users\\Oshino\\AppData\\Local\\Microsoft\\Windows\\Themes\\anime.theme'

def rename_pictures():
    for file in os.listdir('.'):
        suf = file.split('.')
        suf = suf[len(suf)-1].lower()
        if suf == 'png' or suf == 'jpg':
            os.rename(file, f'{uuid.uuid1()}.png')

def write_theme_file():
    i = 0
    linenum = 0
    fread = open('./temp.txt', 'r')
    fwrite = open(PATH, 'w')
    fappend = open(PATH, 'a')

    # Write all until ImagesRootPath
    for line in fread.readlines():
        fwrite.write(line)
        linenum += 1
        if line.split('=')[0] == 'ImagesRootPath':
            break

    # Write image files 
    for file in os.listdir('.'):
        start = linenum

        # Write the filename to the .theme file
        suf = file.split('.')
        if len(suf) > 1:
            suf = suf[len(suf)-1].lower()
        if suf == 'png' or suf == 'jpg':
            fread.seek(start)
            line = fread.readline()
            new_filename = f"\nItem{i}Path=C:\\Users\\Oshino\\Pictures\\wp\\{file}"
            fappend.write(new_filename)
            i += 1

    fread.close()
    fwrite.close()
    fappend.close()

    # Execute the anime.theme command
    os.system(PATH)

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_created(e):
        with open(PATH, 'a') as fa:
            new_filename = f'{uuid.uuid1()}.png'
            os.rename(e.src_path, new_filename)
            fa.write(new_filename)
        fa.close()
        os.system(PATH)

    @staticmethod
    def on_moved(e):
        write_theme_file()
    
    @staticmethod
    def on_deleted(e):
        write_theme_file()

if __name__ == "__main__":
    fs_event_handler = Handler()
    observer = Observer()

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    observer.schedule(fs_event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()