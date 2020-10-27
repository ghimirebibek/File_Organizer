from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os,shutil
import json
import time

# Add the paths to your folders below. the varibles below are created taking Downloads folder into consideration.

folder_to_track = ""
Image_folder = ""
Audio_folder = ""
Documents_folder = ""
Video_folder = ""
Programs_folder = ""
Misc_folder = ""


class MyHandler(FileSystemEventHandler):
    def on_created(self,event):
        for file in os.listdir(folder_to_track):
            if "." in file:
                file_size = -1

                while file_size != os.path.getsize(folder_to_track):
                        file_size = os.path.getsize(folder_to_track)
                        time.sleep(1)


                src = folder_to_track + "/" + file
                x = file.split(".")  
                if x[1].lower() == 'jpg' or x[1].lower() == 'jpeg' or x[1].lower() == 'png':
                    print("image file located")
                    shutil.move(src, Image_folder)
                elif x[1].lower() == 'mp3' or x[1].lower() == 'mp4':
                    print("audio file located")
                    shutil.move(src, Audio_folder)
                elif x[1].lower() == 'avi' or x[1].lower() == 'mov':
                    print("video file located")
                    shutil.move(src, Video_folder)
                elif x[1].lower() == 'exe':
                    print("executable file located")
                    shutil.move(src, Programs_folder)
                elif x[1].lower() == 'docs' or x[1].lower() == 'txt' or x[1].lower() == 'pdf' or x[1].lower() == 'docx':
                    print("document located")
                    shutil.move(src, Documents_folder)
                elif x[1].lower() == 'tmp':
                    print("temporary file located")
                    Observer()
                    
                else:
                    shutil.move(src, Misc_folder)

 
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()

try:
    while True:
        time.sleep(2)
except KeyboardInterrupt:
    observer.stop()
observer.join()
