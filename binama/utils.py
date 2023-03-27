# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 10:38:40 2022

@author: DELINTE Nicolas
"""

import numpy as np
from warnings import warn
from skimage.morphology import flood
from scipy.ndimage import binary_dilation, binary_erosion


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

    cond = (voxel[0] < data.shape[0] and voxel[0] >= 0 and
            voxel[1] < data.shape[1] and voxel[1] >= 0 and
            voxel[2] < data.shape[2] and voxel[2] >= 0)

    return cond


def dilation(mask, repeat: int = 1, element: str = 'cross'):
    '''
    Applies the 'dilation' morphological operation to a binary mask.

    Parameters
    ----------
    mask : 3D array
        3D array of size (x,y,z) containing a binary mask.
    repeat : int, optional
        Numbers of times the operation is repeated. The default is 1.
    element : str, optional
        Either 'cross' or 'square'. The default is 'cross'.

    Returns
    -------
    3D array
        3D array of size (x,y,z) containing a dilated binary mask.

    '''

    n_dim = len(mask.shape)
    # Create a structuring element based on the chosen element shape
    if element == 'cross':
        struct_element = np.zeros((3,)*n_dim)
        for d in range(n_dim):
            idc = tuple([slice(None) if d == i else 1 for i in range(n_dim)])
            struct_element[idc] = 1

    elif element == 'square':
        struct_element = np.ones([3]*n_dim)

    # Dilate the mask using the structuring element
    dilated_mask = mask.copy()
    dilated_mask = binary_dilation(dilated_mask, structure=struct_element,
                                   iterations=repeat)

    return dilated_mask*1


def dilate3D(inputROI, repeat=1, square: bool = False):
    '''
    Deprecated

    Parameters
    ----------
    ROI : 3D array
        3D array of size (x,y,z) containing a binary mask.
    repeat : numbers of times the operation is repeated, default=1
    square : bool
        If True then element becomes 3x3 square

    Returns
    -------
    ROI : 3D binary mask dilated by a 3-wide cross kernel

    '''

    warn('This function is deprecated, please use dilation() instead.',
         DeprecationWarning, stacklevel=1)

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


def erosion(mask, repeat: int = 1, element: str = 'cross'):
    '''
    Applies the 'erosion' morphological operation to a binary mask.

    Parameters
    ----------
    mask : 3D array
        3D array of size (x,y,z) containing a binary mask.
    repeat : int, optional
        Numbers of times the operation is repeated. The default is 1.
    element : str, optional
        Either 'cross' or 'square'. The default is 'cross'.

    Returns
    -------
    3D array
        3D array of size (x,y,z) containing an eroded binary mask.

    '''

    n_dim = len(mask.shape)
    # Create a structuring element based on the chosen element shape
    if element == 'cross':
        struct_element = np.zeros((3,)*n_dim)
        for d in range(n_dim):
            idc = tuple([slice(None) if d == i else 1 for i in range(n_dim)])
            struct_element[idc] = 1

    elif element == 'square':
        struct_element = np.ones([3]*n_dim)

    # Dilate the mask using the structuring element
    dilated_mask = mask.copy()
    dilated_mask = binary_erosion(dilated_mask, structure=struct_element,
                                  iterations=repeat)

    return dilated_mask*1


def erode3D(inputROI, repeat=1):
    '''
    Deprecated

    Parameters
    ----------
    ROI : 3D array
        3D array of size (x,y,z) containing a binary mask.
    repeat : numbers of times the operation is repeated, default=1

    Returns
    -------
    ROI : 3D binary mask eroded by a 3-wide cross kernel

    '''

    warn('This function is deprecated, please use erosion() instead.',
         DeprecationWarning, stacklevel=1)

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
    '''
    Applies the opening morphological operation on a binary mask.

    Parameters
    ----------
    ROI : 3D array
        3D array of size (x,y,z) containing a binary mask.
    repeat : int, optional
        Numbers of times the operation is repeated. The default is 1.

    Returns
    -------
    ROI : 3D array
        3D binary mask opened by a 3-wide cross kernel

    '''

    return dilate3D(erode3D(ROI, repeat=repeat), repeat=repeat)


def closing3D(ROI, repeat: int = 1):

    return erode3D(dilate3D(ROI, repeat=repeat), repeat=repeat)


def remove_inclusions(mask):
    '''


    Parameters
    ----------
    mask : 3D array
        3D array of size (x,y,z) containing a binary mask.

    Returns
    -------
    mask : 3D array
        3D array of size (x,y,z) containing a binary mask.

    '''

    mask = mask.copy()
    mask = np.pad(mask, pad_width=1, mode='constant', constant_values=0)
    mask_filled = flood(mask, (0,)*len(mask.shape))
    mask = np.where(mask_filled == 0, 1, mask)
    mask = mask[tuple(slice(1, dim - 1) for dim in mask.shape)]

    return mask


def convex_mask(mask):
    '''


    Parameters
    ----------
    mask : 3D array
        3D array of size (x,y,z) containing a binary mask.

    Returns
    -------
    mask : 3D array
        3D array of size (x,y,z) containing a binary mask.

    '''

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
    '''


    Parameters
    ----------
    mask : 3D array
        3D array of size (x,y,z) containing a binary mask.

    Returns
    -------
    center : TYPE
        DESCRIPTION.

    '''

    center = tuple([np.average(indices) for indices in np.where(mask == 1)])

    return center


def isolate_mass(mask, center, strict: bool = False):
    '''
    Return the region of connected 1s at tne center point.

    Parameters
    ----------
    mask : 3D array
        3D array of size (x,y,z) containing a binary mask.
    center : TYPE
        DESCRIPTION.
    strict : bool, optional
        If True, only direct contact is considered as a conenction.
        The default is False.

    Returns
    -------
    mask_bis : 3D array
        3D array of size (x,y,z) containing a binary mask.

    '''

    center = tuple([int(point) for point in center])

    if strict:
        connectivity = 1
    else:
        connectivity = None

    mask = flood(mask, center, connectivity=connectivity)
    mask_bis = np.zeros((mask.shape))
    mask_bis[mask] = 1

    return mask_bis


def find_largest_volume(mask, strict: bool = False):
    '''
    Isolates the largest region of connected 1s in a mask. The number of regions
    increases computation time. Pre-cleaning is advised (remove noise and small
    regions).

    Parameters
    ----------
    mask : 3D array
        3D array of size (x,y,z) containing a binary mask.
    strict : bool, optional
        If True, only direct contact is considered as a conenction.
        The default is False.

    Returns
    -------
    out : 3D array
        3D array of size (x,y,z) containing a binary mask.

    '''

    idx = np.argwhere(mask)

    m = mask.copy()

    volList = []
    idxList = []

    if strict:
        connectivity = 1
    else:
        connectivity = None

    while idx.shape[0] > 0:

        fm = flood(m, tuple(idx[0]), connectivity=connectivity)
        volList.append(np.sum(fm))
        idxList.append(tuple(idx[0]))

        m[fm == 1] = 0
        idx = np.argwhere(m)

    out = flood(mask, idxList[volList.index(max(volList))],
                connectivity=connectivity)

    return out


def fuse_masks(mask1, mask2):
    '''
    Generates a mask containing the overlapping regions of the two masks as well
    as the connected pixels, in either mask.

    Parameters
    ----------
    mask1 : 3D array
        3D array of size (x,y,z) containing a binary mask.
    mask2 : 3D array
        3D array of size (x,y,z) containing a binary mask.

    Returns
    -------
    fuse : 3D array
        3D array of size (x,y,z) containing a binary mask.

    '''

    mask = mask1+mask2

    m = mask.copy()
    fuse = np.zeros(mask.shape)

    idx = np.argwhere(m == 2)

    idxList = []

    while idx.shape[0] > 0:

        fm = flood(m, tuple(idx[0]), tolerance=1)
        idxList.append(tuple(idx[0]))

        m[fm == 1] = 0
        idx = np.argwhere(m == 2)

    for idx in idxList:
        fuse += flood(mask, tuple(idx), tolerance=1)

    return fuse


def clean_mask(mask, strict: bool = False):
    '''


    Parameters
    ----------
    mask : 3D array
        3D array of size (x,y,z) containing a binary mask.
    strict : bool, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    mask : 3D array
        3D array of size (x,y,z) containing a binary mask.

    '''

    mask = np.pad(mask, pad_width=1, mode='constant', constant_values=0)
    mask = convex_mask(mask)
    mask = isolate_mass(mask, center_of_mass(mask), strict=strict)
    mask = mask[tuple(slice(1, dim - 1) for dim in mask.shape)]

    return mask
