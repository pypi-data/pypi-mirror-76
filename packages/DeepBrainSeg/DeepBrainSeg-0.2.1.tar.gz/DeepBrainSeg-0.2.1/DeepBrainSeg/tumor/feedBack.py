#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# author: Avinash Kori
# contact: koriavinash1@gmail.com
# MIT License

# Copyright (c) 2020 Avinash Kori

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import torch
import pandas as pd
import numpy as np
from tqdm import tqdm
from torch.autograd import Variable
from torchvision import transforms

from .dataGenerator import nii_loader, get_patch
from ..helpers import utils

from tqdm import tqdm


def __get_whole_tumor__(data):
    return (data > 0)*(data < 4)

def __get_tumor_core__(data):
    return np.logical_or(data == 1, data == 3)

def __get_enhancing_tumor__(data):
    return data == 3

def _get_dice_score_(prediction, ground_truth):

    masks = (__get_whole_tumor__, __get_tumor_core__, __get_enhancing_tumor__)
    p     = np.uint8(prediction)
    gt    = np.uint8(ground_truth)
    wt, tc, et = [2*np.sum(func(p)*func(gt)) / (np.sum(func(p)) + np.sum(func(gt))+1e-6) for func in masks]
    return wt, tc, et


def GenerateCSV3D(model, 
                dataset_path, 
                logs_root, 
                iteration = 0, 
                device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")):
    """
        Function is generate feedback csv which will be used 
        in hardminning and data generator
        custom function
        
    """
    model.eval()

    brainRegion = []; backgroundRegion = []; 
    ETRegion = []; TCRegion = []; WTRegion = []
    ETDice = []; TCDice = []; WTDice = []
    path = []; coordinate = []; 


    def _GenerateSegmentation_(spath, vol, seg, size = 64, nclasses = 5):
        """
        output of 3D tiramisu model (tir3Dnet)

        N = patch size during inference
        """

        shape = vol['t1'].shape # to exclude batch_size
        final_prediction = np.zeros((nclasses, shape[0], shape[1], shape[2]))
        x_min, x_max, y_min, y_max, z_min, z_max = 0, shape[0], 0, shape[1], 0, shape[2]
        x_min, x_max, y_min, y_max, z_min, z_max = x_min, min(shape[0] - size, x_max), y_min, min(shape[1] - size, y_max), z_min, min(shape[2] - size, z_max)

        with torch.no_grad():
            for x in tqdm(range(x_min, x_max, size//2)):
                for y in range(y_min, y_max, size//2):
                    for z in range(z_min, z_max, size//2):

                        data, mask = get_patch(vol, seg, coordinate = (x, y, z), size = size)
                        data = Variable(torch.from_numpy(data).unsqueeze(0)).to(device).float()
                        pred = torch.nn.functional.softmax(model(data).detach().cpu())
                        pred = pred.data.numpy()

                        final_prediction[:, x:x + size, y:y + size, z:z + size] = pred[0]

                        # Logs update
                        pred = np.argmax(pred[0], axis=0)
                        wt, tc, et = _get_dice_score_(pred, mask)
                        # print(np.unique(pred), np.unique(mask), pred.shape, mask.shape)
                        coordinate.append((x, y, z))
                        path.append(spath)
                        backgroundRegion.append(np.mean(mask == 0))
                        WTRegion.append(np.mean(__get_whole_tumor__(mask)))
                        ETRegion.append(np.mean(__get_enhancing_tumor__(mask)))
                        TCRegion.append(np.mean(__get_tumor_core__(mask)))
                        brainRegion.append(np.mean(mask > 0))
                        ETDice.append(et); WTDice.append(wt); TCDice.append(tc)
                        
                        # print(ETDice[-1], WTDice[-1], TCDice[-1], WTRegion[-1], ETRegion[-1])

        final_prediction = utils.convert5class_logitsto_4class(final_prediction)
        final_prediction = np.argmax(final_prediction, axis=0).reshape((shape[0], shape[1],shape[2]))

        return final_prediction


    if iteration == 0:
        subjects = [sub for sub in os.listdir(dataset_path) if not os.path.isfile(os.path.join(dataset_path, sub))]
        training_subjects = subjects[:int(.8*len(subjects))]
        validation_subjects = subjects[int(.8*len(subjects)):]
        data_splits = [training_subjects, validation_subjects]
    else :
        training_subjects = pd.read_csv(os.path.join(logs_root, 'csv/training.csv'))['path'].values
        training_subjects = [sub.split('/')[-1] for sub in training_subjects]
        data_splits = [np.unique(training_subjects)]


    for i, subjects in enumerate(data_splits):
        for subject in tqdm(subjects):
            print(subject)
            spath = {}
            subject_path = os.path.join(dataset_path, subject)
            spath['flair'] = os.path.join(subject_path, subject + '_flair.nii.gz')
            spath['t1ce']  = os.path.join(subject_path, subject + '_t1ce.nii.gz')
            spath['seg']   = os.path.join(subject_path, subject + '_seg.nii.gz')
            spath['t1']    = os.path.join(subject_path, subject + '_t1.nii.gz')
            spath['t2']    = os.path.join(subject_path, subject + '_t2.nii.gz')
            spath['mask']  = os.path.join(subject_path, 'mask.nii.gz')

            vol, seg, affine = nii_loader(spath)
            predictions = _GenerateSegmentation_(subject_path, vol, seg, size = 64, nclasses = 5)
            utils.save_volume(predictions, affine, os.path.join(subject_path, 'DeepBrainSeg_Prediction_iteration_{}'.format(iteration)))


        dataFrame = pd.DataFrame()
        dataFrame['path'] = path
        dataFrame['ETRegion'] = ETRegion
        dataFrame['TCRegion'] = TCRegion
        dataFrame['WTRegion'] = WTRegion
        dataFrame['brain']    = brainRegion
        dataFrame['ETdice'] = ETDice
        dataFrame['WTdice'] = WTDice
        dataFrame['TCdice'] = TCDice
        dataFrame['background'] = backgroundRegion
        dataFrame['coordinate'] = coordinate
        
        if iteration == 0: csv_root = os.path.join(logs_root, 'csv')
        else: csv_root = os.path.join(logs_root, 'csv/iteration_{}'.format(iteration))

        os.makedirs(csv_root, exist_ok=True)

        if i == 0: save_path = os.path.join(csv_root, 'training.csv')
        else: save_path = os.path.join(csv_root, 'validation.csv')

        dataFrame.to_csv(save_path)
        
    if iteration == 0:
        return os.path.join(csv_root, 'training.csv'), os.path.join(csv_root, 'validation.csv')
    else:
        return save_path


if __name__ == '__main__':
    T3Dnclasses = 5
    from os.path import expanduser
    home = expanduser("~")
    ckpt_tir3D    = os.path.join(home, '.DeepBrainSeg/BestModels/Tramisu_3D_FC57_best_acc.pth.tar')

    from .models.modelTir3D import FCDenseNet57
    Tir3Dnet = FCDenseNet57(T3Dnclasses)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    ckpt = torch.load(ckpt_tir3D, map_location=device)
    Tir3Dnet.load_state_dict(ckpt['state_dict'])
    print ("================================== TIRNET3D Loaded =================================")
    Tir3Dnet = Tir3Dnet.to(device)

    GenerateCSV(Tir3Dnet, '../../sample_volume/brats', '../../Logs/')
