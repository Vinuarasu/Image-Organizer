from PIL import Image
from PIL.ExifTags import TAGS
import exiftool
import os
import numpy as np
import cv2
import time
import shutil


Months = ["None", "Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"]
def GetExifData(Files):
    #exiftool.executable("exiftool.exe")
    with exiftool.ExifTool(executable_="D:\Work\Folder organizer\exiftool.exe") as e:
        fileinfo =[]
        for file in Files:
            data = []
            if (e.running):
                md = e.get_metadata(file)
                data.append(file)
                modifydate = md['File:FileModifyDate'] 
                st_time = time.strptime(modifydate, "%Y:%m:%d %H:%M:%S%z")
                data.append(st_time.tm_year)
                data.append(st_time.tm_mon)
                data.append(st_time.tm_mday)
                fileinfo.append(data)
                #print(st_time)
                #md = e.get_metadata_batch(imagename)
        e.terminate()
    return fileinfo

def GetFileList(root):
    file_list = []
    for root, dirs, files in os.walk(root):
        for f in files:
            file_list.append(os.path.join(root, f))
        #    print(os.path.join(root, f))  
    return file_list

def CreateDirectories(fileInfo):
    monthyear = []
    for info in fileInfo:
        monthyear.append('./Organized folder/' + str(info[1]) + '/' +  Months[info[2]])    
    umonthyear = np.unique(monthyear)
    for directory in umonthyear:
        if not os.path.exists(directory):
            os.makedirs(directory)
        else:
            print("enna da nadakuthu")
    return monthyear


if __name__ == "__main__":
    fileLocation = "./Unorganized folder"
    fileList = GetFileList(fileLocation)
    fileInfo = GetExifData(fileList)
    folders = CreateDirectories(fileInfo)
    for file, destfolder in zip(fileInfo, folders):
        if os.path.exists(file[0]):
            print("moving: ",file[0])
            shutil.move(file[0], destfolder)


    
        