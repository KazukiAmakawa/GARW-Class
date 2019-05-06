#=============================================================================
#
#       Group Attribute Random Walk Program
#       CUB_load.py
#
#       Copyright by KazukiAmakawa, all right reserved
#
#=======================================================
#
#       Intro
#       This file will load CUB dataset for bird classification
#
#=============================================================================


from __future__ import print_function

import torch
import numpy as np
import warnings
from PIL import Image
import scipy.io as sio
import os
import time
import parameter

device = parameter.device


def load_data(data_folder, target_size=(224, 224), bounding_box=True):
    X_train = []
    X_test = []
    y_train = []
    y_test = []
    images_file = data_folder+'/images.txt'
    label_file = data_folder+'/image_class_labels.txt'
    attributes_file = data_folder+'/attributes/image_attribute_labels.txt'
    class_attributes_file = data_folder+'/attributes/class_attribute_labels_continuous.txt'
    split_file = data_folder+'/train_test_split.txt'
    bb_file = data_folder+'/bounding_boxes.txt'
    attribute_name_file = data_folder+'/attributes.txt'
    processed_attribute_file = data_folder+'/processed_attributes.txt'
    
    # Part the image as train and test sets
    split_rf = open(split_file,'r')
    train_test_list = []
    train_idx = []
    test_idx = []
    i=0
    for line in split_rf.readlines():
        strs = line.strip().split(' ')
        train_test_list.append(strs[1])
        if(strs[1]=='1'):
            train_idx.append(i)
        else:
            test_idx.append(i)
        i+=1
    split_rf.close()

    # Read bounding box
    bb_rf = open(bb_file,'r')
    bb_list = []
    for line in bb_rf.readlines():
        strs = line.strip().split(' ')
        bb_list.append((float(strs[1]),float(strs[2]),float(strs[1])+float(strs[3])
            ,float(strs[2])+float(strs[4])))
    bb_rf.close()


    # Read image with bounding box
    i = 0
    images_rf = open(images_file,'r')
    for line in images_rf.readlines():
        strs = line.strip().split(' ')
        img = Image.open(data_folder+'/images/'+strs[1])
        if(bounding_box):
            img = img.crop(bb_list[int(strs[0])-1])
        img = img.resize(target_size)
        x = torch.Tensor(np.array(img)).to(device)
        if(train_test_list[int(strs[0])-1]=='1'):
            X_train.append(x)
        else:
            X_test.append(x)
        i += 1
        if(i%1000==0):
            print(i,' images load.')
    images_rf.close()


    # Read label
    label_rf = open(label_file,'r')
    for line in label_rf.readlines():
        strs = line.strip().split(' ')
        if(train_test_list[int(strs[0])-1]=='1'):
            y_train.append(int(strs[1])-1)
        else:
            y_test.append(int(strs[1])-1)
    label_rf.close()


    # Read attributes
    A_all = np.genfromtxt(processed_attribute_file, dtype=int, delimiter=' ')
    A_train = A_all[train_idx]
    A_test = A_all[test_idx]

    X_train = X_train
    X_test = X_test
    y_train = np.array(y_train)
    y_test = np.array(y_test)
    
    return (X_train, y_train, A_train), (X_test, y_test, A_test)



if __name__ == '__main__':
    (X_train, y_train, A_train), (X_test, y_test, A_test) = load_data("./Input/CUB_200_2011")


