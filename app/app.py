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
from keras.models import load_model
from numpy import array
from functions import build_input
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

    #set error variables
    sixty_error = (valid['close'] - valid['sixty']).mean()
    thirty_error = (valid['close'] - valid['thirty']).mean()
    ten_error = (valid['close'] - valid['ten']).mean()

    #output to json
    valid = valid.to_json(orient='index')
    
    return valid

if __name__ == "__main__":
    app.run(debug=False)
