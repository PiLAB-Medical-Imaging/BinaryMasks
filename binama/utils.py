# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 10:38:40 2022

@author: DELINTE Nicolas
"""

import numpy as np


def fill(position: tuple, data, new_val: float):

    data_new = data.copy()
    init_val = int(data[position])

    voxelList = [position]

    while len(voxelList) > 0:

        voxel = voxelList[0]

        voxelList = getVoxels(voxel, data_new, init_val, voxelList)
        data_new[voxel] = int(new_val)
        voxelList = [y for y in voxelList if y != voxel]

    return data_new


def getVoxels(voxel, data, init_val, voxelList):

    (x, y, z) = voxel

    adjacentVoxelList = [(x+1, y, z), (x-1, y, z), (x, y+1, z),
                         (x, y-1, z), (x, y, z+1), (x, y, z-1)]

    for adja in adjacentVoxelList:
        if isInbound(adja, data):
            if data[adja] == init_val and data[voxel] == init_val:
                voxelList.append(adja)

    return voxelList


def isInbound(voxel, data):

    return voxel[0] < data.shape[0] and voxel[0] >= 0 and voxel[1] < data.shape[1] and voxel[1] >= 0 and voxel[2] < data.shape[2] and voxel[2] >= 0


def dilate3D(inputROI, repeat=1, square: bool = False):
    '''


    Parameters
    ----------
    ROI : 3D binary mask
    repeat : numbers of times the operation is repeated, default=1
    square : bool
        If True then element becomes 3x3 square

    Returns
    -------
    ROI : 3D binary mask dilated by a 3-wide cross kernel

    '''

    ROI = inputROI.copy()

    while repeat > 0:

        ROI_copy = ROI.copy()

        if square:
            ROI_copy = ROI

        for i in range(len(ROI.shape)):

            orderLeft = list(range(1, ROI.shape[i]))+[0]
            orderRight = [ROI.shape[i]-1]+list(range(0, ROI.shape[i]-1))

            for order in [orderLeft, orderRight]:

                if i == 0:
                    ROI += ROI_copy[order, :, :]
                elif i == 1:
                    ROI += ROI_copy[:, order, :]
                elif i == 2:
                    ROI += ROI_copy[:, :, order]

        ROI[ROI > 0] = 1
        repeat -= 1

    return ROI


def erode3D(inputROI, repeat=1):
    '''


    Parameters
    ----------
    ROI : 3D binary mask    
    repeat : numbers of times the operation is repeated, default=1

    Returns
    -------
    ROI : 3D binary mask eroded by a 3-wide cross kernel

    '''

    ROI = inputROI.copy()

    while repeat > 0:
        ROI_copy = ROI.copy()

        for i in range(len(ROI.shape)):

            orderLeft = list(range(1, ROI.shape[i]))+[0]
            orderRight = [ROI.shape[i]-1]+list(range(0, ROI.shape[i]-1))

            for order in [orderLeft, orderRight]:

                if i == 0:
                    ROI += ROI_copy[order, :, :]
                elif i == 1:
                    ROI += ROI_copy[:, order, :]
                elif i == 2:
                    ROI += ROI_copy[:, :, order]

        thresh = 7

        ROI[ROI < thresh] = 0
        ROI[ROI >= thresh] = 1
        repeat -= 1

    return ROI


def opening3D(ROI, repeat: int = 1):

    return dilate3D(erode3D(ROI, repeat=repeat), repeat=repeat)


def closing3D(ROI, repeat: int = 1):

    return erode3D(dilate3D(ROI, repeat=repeat), repeat=repeat)


def remove_inclusions(mask):

    from skimage.morphology import flood

    mask = mask.copy()
    mask_filled = flood(mask, (0, 0, 0))
    mask = np.where(mask_filled == 0, 1, mask)

    return mask


def convex_mask(mask):

    from skimage.morphology import flood

    mask = mask.copy()
    mask_filled = mask.copy()
    for x in range(mask.shape[0]):
        mask_filled[x, :, :] = flood(mask[x, :, :], (0, 0))
    mask = np.where(mask_filled == 0, 1, mask)

    mask_filled = mask.copy()
    for y in range(mask.shape[1]):
        mask_filled[:, y, :] = flood(mask[:, y, :], (0, 0))
    mask = np.where(mask_filled == 0, 1, mask)

    mask_filled = mask.copy()
    for z in range(mask.shape[2]):
        mask_filled[:, :, z] = flood(mask[:, :, z], (0, 0))
    mask = np.where(mask_filled == 0, 1, mask)

    return mask


def center_of_mass(mask):

    center = tuple([np.average(indices) for indices in np.where(mask == 1)])

    return center


def isolate_mass(mask, center):

    from skimage.morphology import flood

    center = tuple([int(point) for point in center])

    mask = flood(mask, center)
    mask_bis = np.zeros((mask.shape))
    mask_bis[mask] = 1

    return mask_bis


def clean_mask(mask):

    mask = convex_mask(mask)
    mask = isolate_mass(mask, center_of_mass(mask))

    return mask
