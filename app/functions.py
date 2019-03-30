# File to store python functions for the flask app
import pandas as pd
import numpy as np
import datetime
from datetime import datetime, timedelta
import requests
import json
import alpha_vantage
from alpha_vantage.timeseries import TimeSeries
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.models import load_model
from numpy import array

def one_year_data(stock_ticker): 
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    past_year = datetime.strftime(datetime.now() - timedelta(366), '%Y-%m-%d')
    

    url = "https://www.alphavantage.co/query?"
    query_url = f"{url}function=TIME_SERIES_DAILY&symbol={stock_ticker}&outputsize=full&apikey={JH6O3VJXUFU3WLSZ}" 

    response = requests.get(query_url).json() 

    df = pd.DataFrame(response["Time Series (Daily)"]) 

    df_transposed = df.T # or df1.transpose()

    df_filtered = df_transposed[yesterday : past_year] 

    df_filtered.rename(columns={'4. close':'close', '3. low':'low', '2. high':'high', '5. volume':'volume'}, inplace=True)
    
    df_filtered.drop('1. open', axis=1, inplace=True)
    
    df_filtered = df_filtered[["close", "low", "high", "volume"]]
    
    df_filtered.close = pd.to_numeric(df_filtered.close, errors='coerce')
    df_filtered.low = pd.to_numeric(df_filtered.low, errors='coerce')
    df_filtered.high = pd.to_numeric(df_filtered.high, errors='coerce')
    df_filtered.volume = pd.to_numeric(df_filtered.volume, errors='coerce')
    df_filtered.index = pd.to_datetime(df_filtered.index)
    df_filtered = df_filtered.sort_index(ascending=True)
    
    ten_day_model = load_model("ML/model_ten_day.h5")
    thirty_day_model = load_model("ML/model_thirty_day.h5")
    sixty_day_model = load_model("ML/model_sixty_day.h5")    
    
    #sixty day model
    dataset = df_filtered.values
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)
    X_test, y_test = [], []
    for i in range(60,len(dataset)):
        X_test.append(scaled_data[i-60:i,0:4])
        y_test.append(scaled_data[i,0])
    X_test, y_test = np.array(X_test), np.array(y_test)
    
    closing_price = sixty_day_model.predict(X_test)
    
    final = []
    for price in closing_price:
        final.append(np.pad(price, (0, 3), 'constant'))
    final_price = scaler.inverse_transform(final)
    close = []
    for price in final_price:
        close.append(price[0])
    
    valid_sixty_day = df_filtered[60:] 
    valid_sixty_day["predictions"] = close
    
    #thirty day model 
    dataset = df_filtered.values
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)
    X_test, y_test = [], []
    for i in range(30,len(dataset)):
        X_test.append(scaled_data[i-30:i,0:4])
        y_test.append(scaled_data[i,0])
    X_test, y_test = np.array(X_test), np.array(y_test)
    
    closing_price = thirty_day_model.predict(X_test)
    
    final = []
    for price in closing_price:
        final.append(np.pad(price, (0, 3), 'constant'))
    final_price = scaler.inverse_transform(final)
    close = []
    for price in final_price:
        close.append(price[0])
    
    valid_thirty_day = df_filtered[30:] 
    valid_thirty_day["predictions"] = close
    
    #ten day model
    dataset = df_filtered.values
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)
    X_test, y_test = [], []
    for i in range(11,len(dataset)):
        X_test.append(scaled_data[i-11:i-1,0:4])
        y_test.append(scaled_data[i,0])
    X_test, y_test = np.array(X_test), np.array(y_test)
    
    closing_price = ten_day_model.predict(X_test)
    
    final = []
    for price in closing_price:
        final.append(np.pad(price, (0, 3), 'constant'))
    final_price = scaler.inverse_transform(final)
    close = []
    for price in final_price:
        close.append(price[0])
    
    valid_ten_day = df_filtered[11:]  
    valid_ten_day["predictions"] = close
    
    #output to json
    valid_sixty_day = valid_sixty_day[-90:]
    valid_thirty_day = valid_thirty_day[-90:]
    valid_ten_day = valid_ten_day[-90:]  
    
    valid_sixty_day = valid_sixty_day.to_json(orient='index') 
    valid_thirty_day = valid_thirty_day.to_json(orient='index')
    valid_ten_day = valid_ten_day.to_json(orient='index')
    
    
    
    return valid_sixty_day, valid_thirty_day, valid_ten_day