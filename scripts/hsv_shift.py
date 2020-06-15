#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 20:54:43 2020

@author: macbook
"""

import cv2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def shift_h(data, v_thresh, s_thresh):
    """Produces shifted H values for color segmentation
    Chroma h is returned from 0 - 179, neutral h are returned 200-255
    Inputs: data - array of pixel H, S, V values one entry per pixel
    Outputs: H, H120, H240
    """
    shifted_colors = []
    for i in range(0,len(data)):
        H = data[i][0]
        s = data[i][1]
        v = data[i][2]
        V_thres = 255*v_thresh
        S_thres = 255*s_thresh
        if (v > V_thres and s > S_thres):
            if H >= 120:
                H120 = H - 120
            else:
                H120 = H + 60
            if H >= 60:
                H240 = H - 60
            else:
                H240 = H + 120
        else:
            H = 200 + ((v/255)*55)
            H120 = H
            H240 = H
        shifted_colors.append([H,H120,H240])
    return pd.DataFrame(shifted_colors, columns=["H", "H120", "H240"])

def shift_h_df(data, v_thresh, s_thresh):
    """Produces shifted H values for color segmentation
    Inputs: data - dataframe of pixel H, S, V values one entry per pixel
    Outputs: H, H120, H240
    """
    shifted_colors = []
    for i in range(0,len(data)):
        H = data["h"][i]
        s = data["s"][i]
        v = data["v"][i]
        V_thres = 255*v_thresh
        S_thres = 255*s_thresh
        if (v > V_thres and s > S_thres):
            if H >= 120:
                H120 = H - 120
            else:
                H120 = H + 60
            if H >= 60:
                H240 = H - 60
            else:
                H240 = H + 120
        else:
            H = 200 + ((v/255)*55)
            H120 = H
            H240 = H
        shifted_colors.append([H,H120,H240])
    return pd.DataFrame(shifted_colors, columns=["H", "H120", "H240"])

def shift_h_df_remove(data, v_thresh, s_thresh):
    """Produces shifted H values for color segmentation
    Inputs: data - list of pixel H, S, V values one entry per pixel
    Outputs: H, H120, H240
    """
    shifted_colors = []
    for i in range(0,len(data)):
        H = data["h"][i]
        s = data["s"][i]
        v = data["v"][i]
        V_thres = 255*v_thresh
        S_thres = 255*s_thresh
        if (v > V_thres and s > S_thres):
            if H >= 120:
                H120 = H - 120
            else:
                H120 = H + 60
            if H >= 60:
                H240 = H - 60
            else:
                H240 = H + 120
            shifted_colors.append([H,H120,H240])
        else:
            pass
        
    return pd.DataFrame(shifted_colors, columns=["H", "H120", "H240"])

def shift_h_split(data, v_thresh , s_thresh):
    """
    splits the image pixels into neutrals and chroma based on thresholds

    Parameters
    ----------
    data : array of pixels
        an array of pixels from user data
    v_thresh : float
        the threshold for the values (blacks) from 0-1 0.3 is default.
    s_thresh : float
        the threshold for the saturation (whites) from 0-1, 0.3 is defualt.

    Returns
    -------
    shifted_colors : array of colors
    shifted_neutrals : TYPE
        DESCRIPTION.

    """
    shifted_colors = []
    shifted_neutrals = []
    for i in range(0,len(data)):
        H = data[i][0]
        s = data[i][1]
        v = data[i][2]
        V_thres = 255*v_thresh
        S_thres = 255*s_thresh
        if (v > V_thres and s > S_thres):
            label = "c"
            if H >= 120:
                H120 = H - 120
            else:
                H120 = H + 60
            if H >= 60:
                H240 = H - 60
            else:
                H240 = H + 120
            shifted_colors.append([H, H120, H240, s, v, label])        
        else:
            label = "n"
            H = H
            H120 = H + 200
            H240 = H + 200
            shifted_neutrals.append([H, H120, H240, s, v, label])
        
        
    return pd.DataFrame(shifted_colors, columns=['h','H120','H240','s','v','label']), pd.DataFrame(shifted_neutrals, columns=['h','H120','H240','s','v','label'])

def import_convert_pixelize(image_path):
    """
    imports image, shows the image and transforms into pixels

    Parameters
    ----------
    image_path : srt
        location of image

    Returns
    -------
    pixels : array
        single dimention array of pixel images.

    """
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    plt.imshow(img_rgb);
    #convert to pixels
    pixels = np.float32(img_HSV.reshape(-1, 3))
    return pixels