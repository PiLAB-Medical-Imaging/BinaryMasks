# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 13:36:34 2022

@author: nicol
"""

import os
from binama.utils import *

if __name__ == '__main__':

    import nibabel as nib

    os.chdir('..')

    data_file = 'data/sampleSubject_brain_mask.nii.gz'
    img = nib.load(data_file)
    mask = img.get_fdata()

    mask = clean_mask(mask)

    center = center_of_mass(mask)
    print('Center of mass : ', center)

    out = nib.Nifti1Image(mask, img.affine)
    out.to_filename('data/sampleSubject_brain_mask_cleaned.nii.gz')
