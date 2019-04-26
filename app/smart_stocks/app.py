# Dependencies
import os
import pandas as pd
import numpy as np
import datetime
from datetime import datetime, timedelta
import requests
import json
import alpha_vantage
from alpha_vantage.timeseries import TimeSeries
from flask import Flask, jsonify, render_template
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
from numpy import array
import tensorflow as tf
import random
global graph,model,current_sixty_pred,current_thirty_pred,current_ten_pred,sixty_error,thirty_error,ten_error
graph = tf.get_default_graph()

# initialize app
app = Flask(__name__)

# load in the models
ten_day_model = load_model(os.path.join(os.path.dirname(__file__), 'models/model_ten_day.h5'))
thirty_day_model = load_model(os.path.join(os.path.dirname(__file__), 'models/model_thirty_day.h5'))
sixty_day_model = load_model(os.path.join(os.path.dirname(__file__), 'models/model_sixty_day.h5'))

# declare variables
predictions = 0

# Build functions
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

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

    
@app.route("/current/<stock>")
def stock_chart(stock):
    url = "https://www.alphavantage.co/query?"
    query_url = f"{url}function=TIME_SERIES_INTRADAY&symbol={stock}&interval=5min&apikey=JH6O3VJXUFU3WLSZ" 
    response = requests.get(query_url).json() 
    df = pd.DataFrame(response["Time Series (5min)"])
    data = df.iloc[:, 0]
    current_data = data.to_json(orient='index')
    return (current_data)



@app.route("/data/<stock>")
def data(stock):
    #yesterday = datetime.strftime(datetime.now() '%Y-%m-%d')
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    past_year = datetime.strftime(datetime.now() - timedelta(366), '%Y-%m-%d')
    

    url = "https://www.alphavantage.co/query?"
    query_url = f"{url}function=TIME_SERIES_DAILY&symbol={stock}&outputsize=full&apikey=JH6O3VJXUFU3WLSZ" 

    response = requests.get(query_url).json() 

    df = pd.DataFrame(response["Time Series (Daily)"]) 

    df_transposed = df.T # or df1.transpose()

    df_filtered = df_transposed[yesterday : past_year] 

    #format the input dataframe
    df_filtered.rename(columns={'1. open': 'open', '4. close':'close', '3. low':'low', '2. high':'high', '5. volume':'volume'}, inplace=True)
    df_filtered.open = pd.to_numeric(df_filtered.open, errors='coerce')
    df_filtered.close = pd.to_numeric(df_filtered.close, errors='coerce')
    df_filtered.low = pd.to_numeric(df_filtered.low, errors='coerce')
    df_filtered.high = pd.to_numeric(df_filtered.high, errors='coerce')
    df_filtered.volume = pd.to_numeric(df_filtered.volume, errors='coerce')
    df_filtered.index = pd.to_datetime(df_filtered.index)
    df_filtered = df_filtered.sort_index(ascending=True)
    df_filtered = df_filtered[["open", "close", "low", "high", "volume"]]
    
    #build the inputs for the models
    x_sixty, current_sixty, x_thirty, current_thirty, x_ten, current_ten, y_scalar = build_input(df_filtered)

    #run the models
    with graph.as_default():
        closing_price_sixty = sixty_day_model.predict(x_sixty)
        current_sixty_pred = sixty_day_model.predict(current_sixty)
        closing_price_thirty = thirty_day_model.predict(x_thirty)
        current_thirty_pred = thirty_day_model.predict(current_thirty)
        closing_price_ten = ten_day_model.predict(x_ten)
        current_ten_pred = ten_day_model.predict(current_ten)
    
    #scalar the outputs
    closing_price_sixty = y_scalar.inverse_transform(closing_price_sixty)
    current_sixty_pred = y_scalar.inverse_transform(current_sixty_pred)
    closing_price_thirty = y_scalar.inverse_transform(closing_price_thirty)
    current_thirty_pred = y_scalar.inverse_transform(current_thirty_pred)
    closing_price_ten = y_scalar.inverse_transform(closing_price_ten)
    current_ten_pred = y_scalar.inverse_transform(current_ten_pred)
    
    #build dataframe to compare predictions
    valid_sixty_day = closing_price_sixty[-90:]
    valid_thirty_day = closing_price_thirty[-90:]
    valid_ten_day = closing_price_ten[-90:]
    valid = df_filtered[-90:]
    valid['sixty'] = valid_sixty_day
    valid['thirty'] = valid_thirty_day
    valid['ten'] = valid_ten_day
    
    predictions = pd.DataFrame([{"open": 0, "close": 0, "low": 0, "high": 0, "volume": 0,
                                "sixty": current_sixty_pred[0][0],
                                "thirty": current_thirty_pred[0][0],
                                "ten": current_ten_pred[0][0]}], index=[datetime.now()])
    print(predictions)
    response = valid.append(predictions)
    response = response.to_json(orient='index')
    
    return response

if __name__ == "__main__":
    app.run(debug=False)
