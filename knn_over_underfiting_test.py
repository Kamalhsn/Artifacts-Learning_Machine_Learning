# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 20:23:40 2019

@author: Kamal
"""

# -*- coding: utf-8 -*-

import os
import nibabel as nib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from skimage import measure

dirName_under = r"F:\Oasis_data_new\Under";
dirName_fully = r"F:\Oasis_data_new\Fully";

def FileRead(file_path):
    nii = nib.load(file_path)
    data = nii.get_data()
    return data

def Nifti3Dto2D(Nifti3D):
    Nifti3DWOChannel = Nifti3D#[:,:,:,0] #Considering there is only one chnnel info
    Nifti2D = Nifti3DWOChannel.reshape(np.shape(Nifti3DWOChannel)[0], np.shape(Nifti3DWOChannel)[1] * np.shape(Nifti3DWOChannel)[2])
    return Nifti2D

def Nifti2Dto1D(Nifti2D):
    Nifti1D = Nifti2D.reshape(np.shape(Nifti2D)[0] * np.shape(Nifti2D)[1])
    return Nifti1D

def Nifti1Dto2D(Nifti1D, height):
    Nifti2D = Nifti1D.reshape(height,int(np.shape(Nifti1D)[0]/height))
    return Nifti2D

def Nifti2Dto3D(Nifti2D):
    Nifti3DWOChannel = Nifti2D.reshape(np.shape(Nifti2D)[0],np.shape(Nifti2D)[0],np.shape(Nifti2D)[1]//np.shape(Nifti2D)[0])
    return Nifti3DWOChannel

def FileSave(data, file_path):
    nii = nib.Nifti1Image(data, np.eye(4))
    nib.save(nii, file_path)
    
def normalize(x):
    min_val = np.min(x)
    max_val = np.max(x)
    x = (x-min_val) / (max_val-min_val)
    return x

def getListOfFiles(dirName): 
    listOfFile = os.listdir(dirName)
    allFiles = []
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles

def main_under():
    listOfFiles_under = getListOfFiles(dirName_under)
    oned_unsam = []
    listOfFiles_under = []
    for (dirpath, dirnames, filenames) in os.walk(dirName_under):
        listOfFiles_under += [os.path.join(dirpath, file) for file in filenames]
    for elem_under in listOfFiles_under:
        red_files_under = FileRead(elem_under)
        twod_under = Nifti3Dto2D(red_files_under)
        oned_under= normalize(Nifti2Dto1D(twod_under))
        oned_unsam.append(oned_under)
    oned_unsam = np.asarray(oned_unsam, dtype=np.float64, order='C')
    return oned_unsam
oned_unsam = main_under()

def main_fully():
    listOfFiles_fully = getListOfFiles(dirName_fully)
    oned_fulsam = []
    listOfFiles_fully = []
    for (dirpath, dirnames, filenames) in os.walk(dirName_fully):
        listOfFiles_fully += [os.path.join(dirpath, file) for file in filenames]
    for elem_fully in listOfFiles_fully:
        red_files_fully = FileRead(elem_fully)
        twod_fully = Nifti3Dto2D(red_files_fully)
        oned_fully= normalize(Nifti2Dto1D(twod_fully))
        oned_fulsam.append(oned_fully)
    oned_fulsam = np.asarray(oned_fulsam, dtype=np.float64, order='C')
    return oned_fulsam
oned_fulsam = main_fully()

artifacts = oned_unsam - oned_fulsam
print("Shape of the artifacts",artifacts.shape)
under_sampled_train,under_sampled_test, artifacts_train,artifacts_test = train_test_split(oned_unsam, artifacts, test_size=0, random_state=0)
print('split completed')
#K nearest neighbor
neigh = KNeighborsRegressor(n_neighbors=12)
neigh.fit(under_sampled_train , artifacts_train)
print('nearest neighbour fit completed')
data_predicted = neigh.predict(under_sampled_train)
print("Type of predicted data is : ",type(data_predicted))