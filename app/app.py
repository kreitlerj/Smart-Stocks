# Dependencies
import pandas as pd
import numpy as np
import datetime
from datetime import datetime, timedelta
import requests
import json
# import alpha_vantage
# from config import apiKey
from flask import Flask, jsonify, render_template
# from sklearn.preprocessing import MinMaxScaler
# from keras.models import Sequential
# from keras.layers import Dense, Dropout, LSTM
# from keras.models import load_model

# initialize app
app = Flask(__name__)

# load in the models
# ten_day_model = load_model("models/model_ten_day.h5")
# thirty_day_model = load_model("models/model_thirty_day.h5")
# sixty_day_model = load_model("models/model_sixty_day.h5")

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


# @app.route("/ticker")
# def names():

@app.route("/data")
def data():
    data = {'sixty': {'2018-12-3': 4, '2018-12-4': 5, '2018-12-5': 3},
            'thirty': {'2018-12-3': 3, '2018-12-4': 3, '2018-12-5': 2},
            'ten': {'2018-12-3': 3.5, '2018-12-4': 2.5, '2018-12-5': 4},
            'actual': {'2018-12-3': 3, '2018-12-4': 4, '2018-12-5': 3.5}
    }

    return jsonify(data)

if __name__ == "__main__":
    app.run()
