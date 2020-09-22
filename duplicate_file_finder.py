import wx
import cv2 as cv
import os
import numpy as np
import hashlib
import shutil

pth = os.path.dirname(os.path.abspath('__file__'))
# temp file for initial image handling
img_pth = os.path.join(pth, "tmp_img.png")
# Folders, subfolders for processed images
all_cats = os.getcwd() + '/Cats'
raw_cats = all_cats + '/raw_cats'
dead_cats = all_cats + '/dead_cats'
temp_cats = all_cats + '/temp_cats'     #For testing

current_dir = dead_cats


 
import hashlib, os, optparse, sys

#define a function to calculate md5checksum for a given file:
def md5(f):
    """takes one file f as an argument and calculates md5checksum for that file"""
    md5Hash=hashlib.md5()
    with open(f,'rb') as f:
        for chunk in iter(lambda: f.read(4096),b""):
            md5Hash.update(chunk)
    return md5Hash.hexdigest()

#define our main function:
def rm_dup():
    """relies on the md5 function above to remove duplicate files"""
    md5_dict={}
    print('Working...')
    print()
    for root, _, files in os.walk(current_dir):#the os.walk function allows checking subdirectories too...
        for f in files:
            filePath=os.path.join(root,f)
            md5Hash=md5(filePath)
            size=os.path.getsize(filePath)
            fileComb=str(md5Hash)+str(size)
            if fileComb in md5_dict:
                md5_dict[fileComb].append(filePath)
            else:
                md5_dict.update({fileComb:[filePath]})
    for key in md5_dict:
        for item in md5_dict[key]:
            while md5_dict[key].count(item)>0:
                md5_dict[key].remove(item)
    for k in list(md5_dict):
        if not md5_dict[k]:
            del md5_dict[k]
    print("Done! Following files will be deleted:\n")
    for key in md5_dict:
        for item in md5_dict[key]:
            print(item)
    pic_num = len([f for f in os.listdir(dead_cats) if os.path.isfile(
            os.path.join(dead_cats, f))])
    print(f"\nfound {len(md5_dict)} duplicates out of {pic_num} files")
    if input("\nEnter (y)es to confirm operation or anything else to abort: ").lower() not in ("y", "yes"):
        sys.exit("\nOperation cancelled by user. Exiting...")

    print("Deleting...")
    c=0
    for key in md5_dict:
        for item in md5_dict[key]:
            os.remove(item)
            md5_dict[key].remove(item)
            c += 1
    
    print(f'Done! Found and deleted {c} files...')

if __name__=='__main__':
   
    rm_dup()