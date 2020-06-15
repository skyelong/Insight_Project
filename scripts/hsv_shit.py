#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 20:54:43 2020

@author: macbook
"""

import cv2
import pandas as pd

def shift_h(array, v_thresh, s_thresh):
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
    return shifted_colors

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
    return shifted_colors

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
        
    return shifted_colors