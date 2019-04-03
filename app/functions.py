import numpy as np
import pandas as pd
import random
from sklearn.preprocessing import MinMaxScaler

def build_input(dataframe):
    x_df = dataframe
    y_df = dataframe[['close']]
    x_scaler = MinMaxScaler(feature_range=(0, 1))
    y_scaler = MinMaxScaler(feature_range=(0, 1))
    x_pred_dataset = x_df.values
    y_pred_dataset = y_df.values
    x_scaled_data = x_scaler.fit_transform(x_pred_dataset)
    y_scaled_data = y_scaler.fit_transform(y_pred_dataset)
    x_pred_sixty, y_pred_sixty = [], []
    x_pred_thirty, y_pred_thirty = [], []
    x_pred_ten, y_pred_ten = [], []
    for i in range(60, len(dataframe)):
        x_pred_sixty.append(x_scaled_data[i-60:i, :])
        y_pred_sixty.append(y_scaled_data[i, :])
    x_pred_sixty, y_pred_sixty = np.array(x_pred_sixty), np.array(y_pred_sixty)

    for i in range(30, len(dataframe)):
        x_pred_thirty.append(x_scaled_data[i-30:i, :])
        y_pred_thirty.append(y_scaled_data[i, :])
    x_pred_thirty, y_pred_thirty = np.array(x_pred_thirty), np.array(y_pred_thirty)

    for i in range(10, len(dataframe)):
        x_pred_ten.append(x_scaled_data[i-10:i, :])
        y_pred_ten.append(y_scaled_data[i, :])
    x_pred_ten, y_pred_ten = np.array(x_pred_ten), np.array(y_pred_ten)

    current_sixty, current_thirty, current_ten = [], [], []
    for i in range(0, 60):
        current_sixty.append(x_scaled_data[i-60])
    x_current_sixty = np.array(current_sixty)
    x_current_sixty = np.reshape(x_current_sixty, (1,) + x_current_sixty.shape)

    for i in range(0, 30):
        current_thirty.append(x_scaled_data[i-30])
    x_current_thirty = np.array(current_thirty)
    x_current_thirty = np.reshape(x_current_thirty, (1,) + x_current_thirty.shape)

    for i in range(0, 10):
        current_ten.append(x_scaled_data[i-10])
    x_current_ten = np.array(current_ten)
    x_current_ten = np.reshape(x_current_ten, (1,) + x_current_ten.shape)

    return(x_pred_sixty, x_current_sixty, x_pred_thirty, x_current_thirty, x_pred_ten, x_current_ten, y_scaler)

def build_current_input(dataframe):
    x_df = dataframe
    y_df = dataframe[['close']]
    x_scaler = MinMaxScaler(feature_range=(0, 1))
    y_scaler = MinMaxScaler(feature_range=(0, 1))
    x_pred_dataset = x_df.values
    y_pred_dataset = y_df.values
    x_scaled_data = x_scaler.fit_transform(x_pred_dataset)
    y_scaled_data = y_scaler.fit_transform(y_pred_dataset)
    
    current_sixty, current_thirty, current_ten = [], [], []
    for i in range(0, 60):
        current_sixty.append(x_scaled_data[i-60])
    x_current_sixty = np.array(current_sixty)
    x_current_sixty = np.reshape(x_current_sixty, (1,) + x_current_sixty.shape)

    for i in range(0, 30):
        current_thirty.append(x_scaled_data[i-30])
    x_current_thirty = np.array(current_thirty)
    x_current_thirty = np.reshape(x_current_thirty, (1,) + x_current_thirty.shape)

    for i in range(0, 10):
        current_ten.append(x_scaled_data[i-10])
    x_current_ten = np.array(current_ten)
    x_current_ten = np.reshape(x_current_ten, (1,) + x_current_ten.shape)
    
    return(x_current_sixty, x_current_thirty, x_current_ten, y_scaler)
