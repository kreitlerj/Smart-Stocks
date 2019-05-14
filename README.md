
# Smart Stocks
### Using an LSTM Model To Predict Closing Stock Prices

#### -- Project Status: Active


## Goals:

-  Predict as accurately as possible the closing stock price for a given stock.
-  Fit three models on three different time intervals. Ten days, thirty days, and sixty days. 
-  Show model performance over test data so as to provide user with the basis of trust in the model.
-  Open the door for further development of a minute to minute stock prediction platform. 


![Screen Shot](images/AI_Stock.png)
      

## Why an LSTM Model and what is it?

- An LSTM Model is a recurrent neural network (RNN) and over time, RNNS have proved themselves as one of the most powerful models for processing sequential data. In our case this is time series data.
- LSTM introduces the concept of a  "memory cell", a unit of computation that replaces traditional artificial neurons in the hidden layer of the network. 
- With these memory cells, networks are able to effectively associate "memories" and input remote in time, therefore prove to be well suited to grasp structure of data dynamically over time with high prediction capacity.
- Obviously, this type of model sacrifices much interoperability and because of this a level of artistry in tuning is required. 
- It would therefore be impotant for the user in this particular instance to possibly develop an algorithmic trading strategy on top that takes in to account the models performance over time and whether it's predictions should be trusted based on other factors.   


### Technologies
* Python
* JavaScript
* Tensorflow, keras
* Pandas, jupyter
* HTML
* Bootstrap
* Flask

## Project Description
This project combines machine learning with a flask web app to demostrate to the end user how machine learning can be used to predict closing stock prices.  The three models use different time steps (60 day, 30 day, and 10 day) to predict end of day closing prices (if the market is still open).  Data is grabbed realtime from [Alpha Vantage](https://www.alphavantage.co/documentation/) and ran on the pre-trained models.  The predictions are then fed to JavaScript on the frontend to be presented to the end user.  Using Plotly.js, the user is presented with a line graph to show how well the models did over the last 90 days of trading.  Since the data is grabbed realtime, the user can select any stock by ticker symbol. The app is deployed on Heroku and can be found [here](https://smart-stocks.herokuapp.com/)
