"""
NIfTI brain tissue masks: coronal slices, histogram thresholds,
connected-component pruning (largest blob), and binary masks for
whole brain / white matter / grey matter.

Voxel counts over slices approximate volumes; helpers support the
Alzheimer’s longitudinal grey-matter ratio comparison in the notebook.
"""
import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import scipy.ndimage as sn


def scan_slices1(filename, slice_level):  #for report
    img = nib.load(filename)  #loading the patient file
    example_file = img.get_fdata()
    Slice = example_file[:, :,
                         slice_level]  #slicing on the xz plane at y=slice_level
    Slice_ = Slice.astype(int)
    return Slice_


def brain_threshold(filename, slice_level):
    img = nib.load(filename)
    example_file = img.get_fdata()
    Slice = example_file[:, :, slice_level]
    Slice_ = Slice.astype(int)
    thres = get_threshold_values(Slice_)[1]
    x_thres = Slice_ > thres

    mask = x_thres.astype(
        int
    )  #doesn't seem to do anything other than plot a threshold scan so maybe we can leave this out later :/
    return mask



def blob_sizes(filename, threshold, slice_level):  #for report
    thres = threshold
    img = nib.load(filename)
    example_file = img.get_fdata()
    Slice = example_file[:, :, slice_level]
    Slice_ = Slice.astype(int)
    x_thres = Slice_ > thres
    (x_labels, n) = sn.label(x_thres)
    print("number of blobs:", n)
    sizes = sn.sum(x_thres, x_labels, range(1, n + 1))
    print(sizes)
    max1 = max(sizes)
    idx = np.argmax(sizes)
    # get the index of the largest blob

    return (max1)


def brain_area(filename, slice_level):
    Slice_ = scan_slices1(filename, slice_level)
    thres = get_threshold_values(Slice_)[1]
    x_thres = Slice_ > thres                                    #thresholding

    (x_labels, n) = sn.label(x_thres)
    sizes = sn.sum(x_thres, x_labels, range(1, n + 1))          #finding size of largest blob size
    max1 = max(sizes)
    return (max1)


def brain_volume(filename):
    miny = 0
    img = nib.load(filename)
    area_list = []  #empty list to put areas into
    for y in range(miny, img.shape[2]):  #iterating the brain_area along the y-axis = volume!
        area_list.append(brain_area(filename, miny))  #add area to list
        miny = miny + 1  #go to next slice above
    return (sum(area_list))

def get_whole_brain(Slice_):
    threshold2, threshold = get_threshold_values(Slice_)
    thres = threshold
    x_thres = Slice_ > thres
    import scipy.ndimage as sn
    (x_labels, n) = sn.label(x_thres)
    sizes = sn.sum(x_thres, x_labels, range(1, n + 1))

    max1 = max(sizes)
    idx = np.argmax(sizes)
    for i in range(len(x_labels)):
        for k in range(len(x_labels[i])):
            if x_labels[i][k] != idx + 1:
                x_thres[i][k] = 0
    return x_thres

def get_white_matter(Slice_):
    threshold2, threshold = get_threshold_values(Slice_)
    thres = threshold
    x_thres = Slice_ > thres
    import scipy.ndimage as sn
    (x_labels, n) = sn.label(x_thres)
    sizes = sn.sum(x_thres, x_labels, range(1, n + 1))

    max1 = max(sizes)
    idx = np.argmax(sizes)
    for i in range(len(x_labels)):
        for k in range(len(x_labels[i])):
            if x_labels[i][k] != idx + 1:
                x_thres[i][k] = 0
    m_img = ((x_thres) * Slice_)
    thres = threshold2
    m_img = m_img > thres

    return m_img


def get_grey_matter(Slice_):
    threshold2, threshold = get_threshold_values(Slice_)
    thres = threshold
    x_thres = Slice_ > thres
    (x_labels, n) = sn.label(x_thres)
    sizes = sn.sum(x_thres, x_labels, range(1, n + 1))

    max1 = max(sizes)
    idx = np.argmax(sizes)
    for i in range(len(x_labels)):
        for k in range(len(x_labels[i])):
            if x_labels[i][k] != idx + 1:
                x_thres[i][k] = 0
    m_img = ((x_thres) * Slice_)
    thres = threshold2
    m_img = m_img > thres

    a = np.subtract(x_thres.astype(int), m_img.astype(int))

    return a

def area(slice):
    size = 0
    for i in range(len(slice)):
        for k in range(len(slice[i])):
            if slice[i][k] == 1:
                size = size + 1
    return size


def grey_matter_volume(filename):
    img = nib.load(filename)
    example_file = img.get_fdata()
    total_size = 0
    for z in range(img.shape[2]):
        Slice = example_file[:, :, z]
        Slice_ = Slice.astype(int)
        size = area(get_grey_matter(Slice_))
        total_size = total_size + size  #add area to list
    return total_size

def grey_matter_change(grey_matter_volume1, grey_matter_volume2, brain_volume1,
                       brain_volume2):
    ratio_bef = 100 * (grey_matter_volume1) / (brain_volume1)
    ratio_aft = 100 * (grey_matter_volume2) / (brain_volume2)
    change = '{:.2f}'.format(ratio_bef - ratio_aft)
    output = ("decrease in volume of grey matter is " + change + '%')
    return output


def histogram(slice):
    slice_data = slice.ravel()
    import numpy as np
    import pandas as pd
    df = pd.DataFrame(slice_data)
    for i in range(25):
        df.loc[df[0] == i] = None

    fig = plt.figure()
    ax = fig.add_subplot()
    bars = ax.hist(df[0], bins=np.arange(0, 177, 1))


def get_threshold_values(slice):
    slice_data = slice.ravel()
    import numpy as np
    import pandas as pd
    df = pd.DataFrame(slice_data)
    for i in range(25):
        df.loc[df[0] == i] = None

    values = df[0].value_counts().index
    threshold1 = values[0]
    i = 0
    threshold2 = values[i]
    while threshold1 - threshold2 < 10:
        i = i + 1
        try:
            threshold2 = values[i]
        except:
            threshold2 = 40
            break
    threshold_values = (threshold1, threshold2)
    return threshold_values
