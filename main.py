from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os,shutil
import time

# import winreg as reg

# code to get the path of Downloads folder
# a = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
# b = "{374DE290-123F-4565-9164-39C4925E467B}"
# key = reg.OpenKey(reg.HKEY_CURRENT_USER, a, 0, reg.KEY_ALL_ACCESS)
# path = reg.QueryValueEx(key, b)
# path = str(path[0])
# reg.CloseKey(key)
folder_to_track = ""
print (folder_to_track)

# code to create Image folder, Audio folder, Video folder, Programs folder, Documents folder, Misc folder in Downloads folder if they don't exist
if not os.path.exists(os.path.join(folder_to_track, "Downloaded Images")):
    print ("Creating Downloaded Images folder")
    os.mkdir(os.path.join(folder_to_track, "Downloaded Images"))
if not os.path.exists(os.path.join(folder_to_track, "Downloaded Audio")):
    print ("Creating Downloaded Audio folder")
    os.mkdir(os.path.join(folder_to_track, "Downloaded Audio"))
if not os.path.exists(os.path.join(folder_to_track, "Downloaded Video")):
    print ("Creating Downloaded Video folder")
    os.mkdir(os.path.join(folder_to_track, "Downloaded Video"))
if not os.path.exists(os.path.join(folder_to_track, "Downloaded Programs")):
    print ("Creating Downloaded Programs folder")
    os.mkdir(os.path.join(folder_to_track, "Downloaded Programs"))
if not os.path.exists(os.path.join(folder_to_track, "Downloaded Documents")):
    print ("Creating Downloaded Documents folder")
    os.mkdir(os.path.join(folder_to_track, "Downloaded Documents"))
if not os.path.exists(os.path.join(folder_to_track, "Downloaded Misc")):
    print ("Creating Downloaded Misc folder")
    os.mkdir(os.path.join(folder_to_track, "Downloaded Misc"))



Image_folder = os.path.join(folder_to_track, "Downloaded Images")
Audio_folder = os.path.join(folder_to_track, "Downloaded Audio")
Documents_folder = os.path.join(folder_to_track, "Downloaded Documents") 
Video_folder = os.path.join(folder_to_track, "Downloaded Video") 
Programs_folder = os.path.join(folder_to_track, "Downloaded Programs")
Misc_folder = os.path.join(folder_to_track, "Downloaded Misc")


class MyHandler(FileSystemEventHandler):
    ImageCount = 0
    AudioCount = 0
    VideoCount = 0
    ProgramsCount = 0
    DocumentsCount = 0
    MiscCount = 0
    TempCount = 0
    print ("loading...")
    for file in os.listdir(folder_to_track):
        if "." in file:
            file_size = -1

            while file_size != os.path.getsize(folder_to_track):
                    file_size = os.path.getsize(folder_to_track)
                    time.sleep(1)


            src = folder_to_track + "/" + file
            x = file.split(".")  
            if x[1].lower() == 'jpg' or x[1].lower() == 'jpeg' or x[1].lower() == 'png':
                ImageCount += 1
                shutil.move(src, Image_folder)
            elif x[1].lower() == 'mp3' or x[1].lower() == 'mp4':
                AudioCount += 1
                shutil.move(src, Audio_folder)
            elif x[1].lower() == 'avi' or x[1].lower() == 'mov':
                VideoCount += 1
                shutil.move(src, Video_folder)
            elif x[1].lower() == 'exe':
                ProgramsCount += 1
                shutil.move(src, Programs_folder)
            elif x[1].lower() == 'docs' or x[1].lower() == 'txt' or x[1].lower() == 'pdf' or x[1].lower() == 'doc' or x[1].lower() == 'docx' or x[1].lower() == 'pptx' or x[1].lower() == 'xlsx' or x[1].lower() == 'ppt' or x[1].lower() == 'xls':
                DocumentsCount += 1
                shutil.move(src, Documents_folder)
            elif x[1].lower() == 'tmp':
                TempCount += 1
                Observer()
                
            else:
                MiscCount += 1
                shutil.move(src, Misc_folder)
    
    print ("Images: " + str(ImageCount))
    print ("Audio: " + str(AudioCount))
    print ("Video: " + str(VideoCount))
    print ("Programs: " + str(ProgramsCount))
    print ("Documents: " + str(DocumentsCount))
    print ("Misc: " + str(MiscCount))
    print ("Temp: " + str(TempCount))
    print ("Total: " + str(ImageCount + AudioCount + VideoCount + ProgramsCount + DocumentsCount + MiscCount + TempCount))
    print ("-------------------------")


 
MyHandler()
