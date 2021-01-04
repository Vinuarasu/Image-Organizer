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
                if(md['File:MIMEType'].split("/")[0] == "image"):
                    img = cv2.imread(file)
                    #print(file)
                    if(img.shape[0]>img.shape[1]):
                        img_ = cv2.resize(img, (200,100))[::4,::4,:].ravel()
                    else:
                        img_ = cv2.resize(img, (100,200))[::4,::4,:].ravel()
                else:
                    #print("Video")
                    img_ = ["Video"]
                data.append(img_)
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

def GetDirectories(fileInfo):
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
    destFolders = GetDirectories(fileInfo)
    for i, (fileinfo, destfolder) in enumerate(zip(fileInfo, destFolders)):
        ref_feature = fileinfo[4]
        if (i>1) and (ref_feature != "Video"):
            for i in range(i-1):
                feature = fileInfo[i][4]
                if (feature != "Video"):
                    sad = np.sum(abs((ref_feature - fileInfo)))
                    print(sad)



        if os.path.exists(fileinfo[0]):
            print("moving: ",fileinfo[0])
            shutil.move(fileinfo[0], destfolder)


    
        
