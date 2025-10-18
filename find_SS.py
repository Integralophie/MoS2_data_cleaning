import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d
import os
import re
import math





def filter_noise(df):
    filtered_df = df[df['Id, V_D = 1.0'] > 1e-13]
    return filtered_df

def grab_V_I_0pt1(df):
    Vtg = df.index.to_numpy()
    Id_sample = df['Id, V_D = 0.4'].to_numpy()

    sigma = 5 # Standard deviation of the Gaussian kernel
    smoothed_Id = gaussian_filter1d(Id_sample, sigma)

    return Vtg, smoothed_Id

def find_first_Id_above_threshold(data_list, threshold):
    try:
        return next(index for index, value in enumerate(data_list) if value > threshold)
    except StopIteration:
        return -1

def find_SS(Vtg, smoothed_Id):

    Id_idx_small = find_first_Id_above_threshold(smoothed_Id,1e-10)
    print(f'Vtg = {Vtg[Id_idx_small]}, Id = {smoothed_Id[Id_idx_small]}')
    Id_idx_large = find_first_Id_above_threshold(smoothed_Id,1e-9)
    print(f'Vtg = {Vtg[Id_idx_large]}, Id = {smoothed_Id[Id_idx_large]}')
    SS = Vtg[Id_idx_large] - Vtg[Id_idx_small]

    # dIdVg = np.gradient(np.log10(smoothed_Id),Vtg)
    # max_index = np.nanargmax(dIdVg)
    # SS = 1/max(dIdVg)
# 
    return SS, Id_idx_large, Id_idx_small

def find_gm(df,max_loc):
    pass