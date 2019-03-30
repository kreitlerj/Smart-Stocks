# Dependencies
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
# from keras.models import Sequential
# from keras.layers import Dense, Dropout, LSTM
from keras.models import load_model
from numpy import array
# from functions import one_year_data
import tensorflow as tf
global graph,model
graph = tf.get_default_graph()

# initialize app
app = Flask(__name__)

# load in the models
ten_day_model = load_model("models/model_ten_day.h5")
thirty_day_model = load_model("models/model_thirty_day.h5")
sixty_day_model = load_model("models/model_sixty_day.h5")

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("dashboard.html")

# @app.route("/dashboard")
# def dashboard():
#     return render_template("dashboard.html")

@app.route("/data_table")
def data_table():
    return render_template("data_table.html")

@app.route("/current/<stock>")
def stock_chart(stock):
    url = "https://www.alphavantage.co/query?"
    query_url = f"{url}function=&symbol={stock}&outputsize=full&apikey=JH6O3VJXUFU3WLSZ"

# @app.route("/ticker")
# def names():

@app.route("/data/<stock>")
def data(stock):
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    past_year = datetime.strftime(datetime.now() - timedelta(366), '%Y-%m-%d')
    

    url = "https://www.alphavantage.co/query?"
    query_url = f"{url}function=TIME_SERIES_DAILY&symbol={stock}&outputsize=full&apikey=JH6O3VJXUFU3WLSZ" 

    response = requests.get(query_url).json() 

    df = pd.DataFrame(response["Time Series (Daily)"]) 

    df_transposed = df.T # or df1.transpose()

    df_filtered = df_transposed[yesterday : past_year] 

    df_filtered.rename(columns={'1. open': 'open', '4. close':'close', '3. low':'low', '2. high':'high', '5. volume':'volume'}, inplace=True)
    
    
    
    df_filtered.open = pd.to_numeric(df_filtered.open, errors='coerce')
    df_filtered.close = pd.to_numeric(df_filtered.close, errors='coerce')
    df_filtered.low = pd.to_numeric(df_filtered.low, errors='coerce')
    df_filtered.high = pd.to_numeric(df_filtered.high, errors='coerce')
    df_filtered.volume = pd.to_numeric(df_filtered.volume, errors='coerce')
    df_filtered.index = pd.to_datetime(df_filtered.index)
    df_filtered = df_filtered.sort_index(ascending=True)
    valid = df_filtered   
    df_filtered = df_filtered.drop('open', axis=1)
    df_filtered = df_filtered[["close", "low", "high", "volume"]]
    
    #sixty day model
    dataset = df_filtered.values
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)
    X_test, y_test = [], []
    for i in range(60,len(dataset)):
        X_test.append(scaled_data[i-60:i,0:4])
        y_test.append(scaled_data[i,0])
    X_test, y_test = np.array(X_test), np.array(y_test)
    
    with graph.as_default():
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
    valid_sixty_day = valid_sixty_day["predictions"]
    
    #thirty day model 
    dataset = df_filtered.values
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)
    X_test, y_test = [], []
    for i in range(30,len(dataset)):
        X_test.append(scaled_data[i-30:i,0:4])
        y_test.append(scaled_data[i,0])
    X_test, y_test = np.array(X_test), np.array(y_test)
    
    with graph.as_default():
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
    valid_thirty_day = valid_thirty_day["predictions"]
    
    #ten day model
    dataset = df_filtered.values
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)
    X_test, y_test = [], []
    for i in range(10,len(dataset)):
        X_test.append(scaled_data[i-10:i,0:4])
        y_test.append(scaled_data[i,0])
    X_test, y_test = np.array(X_test), np.array(y_test)
    
    with graph.as_default():
        closing_price = ten_day_model.predict(X_test)
    
    final = []
    for price in closing_price:
        final.append(np.pad(price, (0, 3), 'constant'))
    final_price = scaler.inverse_transform(final)
    close = []
    for price in final_price:
        close.append(price[0])
    
    valid_ten_day = df_filtered[10:]  
    valid_ten_day["predictions"] = close
    valid_ten_day = valid_ten_day["predictions"]
    
    #output to json
    valid_sixty_day = valid_sixty_day[-90:]
    valid_thirty_day = valid_thirty_day[-90:]
    valid_ten_day = valid_ten_day[-90:]
    valid = valid[-90:]
    valid['sixty'] = valid_sixty_day
    valid['thirty'] = valid_thirty_day
    valid['ten'] = valid_ten_day
    sixty_error = (valid['close'] - valid['sixty']).mean()
    thirty_error = (valid['close'] - valid['thirty']).mean()
    ten_error = (valid['close'] - valid['ten']).mean()

    
    valid = valid.to_json(orient='index')
    # response = {}
    # response['valid'] = valid
    # response['predictions'] = {'sixty': sixty_day_pred, 'thirty': thirty_day_pred, 'ten': ten_day_pred}
    # response['error'] = {'sixty': sixty_error, 'thirty': thirty_error, 'ten': ten_error}
    
    return valid

if __name__ == "__main__":
    app.run(debug=False)
