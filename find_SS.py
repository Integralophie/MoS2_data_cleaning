import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d
import os
import re
import math





def filter_noise(df):
    filtered_df = df[df['Id, V_D = 1.0'] > 5e-11]
    return filtered_df

def grab_V_I_0pt1(df):
    Vtg = df.index.to_numpy()
    Id_sample = df['Id, V_D = 1.0'].to_numpy()

    sigma = 2 # Standard deviation of the Gaussian kernel
    smoothed_Id = gaussian_filter1d(Id_sample, sigma)

    return Vtg, smoothed_Id

def find_first_Id_above_threshold(data_list, threshold):
    try:
        return next(index for index, value in enumerate(data_list) if value > threshold)
    except StopIteration:
        return -1

def find_SS(Vtg, smoothed_Id):

    '''
    needs edit
    '''

    Id_idx_small = find_first_Id_above_threshold(smoothed_Id,1e-10)
    print(f'Vtg = {Vtg[Id_idx_small]}, Id = {smoothed_Id[Id_idx_small]}')
    Id_idx_large = find_first_Id_above_threshold(smoothed_Id,1e-9)
    print(f'Vtg = {Vtg[Id_idx_large]}, Id = {smoothed_Id[Id_idx_large]}')
    SS = Vtg[Id_idx_large] - Vtg[Id_idx_small]
    
    dIdVg = np.gradient(np.log10(smoothed_Id),Vtg)
    SS_grad = 1/max(dIdVg)
    SS_grad_idx = np.nanargmax(dIdVg)

    # dIdVg = np.gradient(np.log10(smoothed_Id),Vtg)
    # max_index = np.nanargmax(dIdVg)
    # SS = 1/max(dIdVg)
# 
    return SS, Id_idx_large, Id_idx_small, SS_grad, SS_grad_idx


def find_SS_grad(Vtg, smoothed_Id):
    dIdVg = np.gradient(np.log10(smoothed_Id),Vtg)
    SS_grad = 1/max(dIdVg)
    SS_grad_idx = np.nanargmax(dIdVg)
    return SS_grad,smoothed_Id[SS_grad_idx],Vtg[SS_grad_idx],dIdVg[SS_grad_idx]


def find_gm(df,max_loc):
    pass



def find_Vth(df):
    Vtg = df.index.to_numpy()

    Vbg_val = []
    Vth_list = []
    for col in df.columns.to_list():
        Vbg_val.append(float(col[10:]))
        current_col = df[col].to_list()
        Id_idx = find_first_Id_above_threshold(current_col,1e-10)
        Vth_list.append(float(Vtg[Id_idx]))

    slope, intercept = np.polyfit(Vbg_val,Vth_list, 1)

    return slope



'''
10mV

'''


def filter_noise_voltage(df):

    filtered_df = df.iloc[140:462]

    return filtered_df


def find_SS_grad_4(filtered_df):
    Id_0p1 = filtered_df['Id, V_D = 0.1'].to_numpy()
    Id_0p4 = filtered_df['Id, V_D = 0.4'].to_numpy()
    Id_0p7 = filtered_df['Id, V_D = 0.7'].to_numpy()
    Id_1p0 = filtered_df['Id, V_D = 1.0'].to_numpy()
    Vtg = filtered_df.index.to_numpy()
    sigma = 0.5 # Standard deviation of the Gaussian kernel
    SS_4 = []
    for Id in [Id_0p1,Id_0p4,Id_0p7,Id_1p0]:
        smoothed_Id = gaussian_filter1d(Id, sigma)
        dIdVg = np.gradient(np.log10(smoothed_Id),Vtg)
        max_index = np.nanargmax(dIdVg)
        SS = 1/max(dIdVg)
        Vtg_ss = Vtg[np.nanargmax(dIdVg)]
        SS_4.append(float(SS))

    return SS_4, Vtg_ss