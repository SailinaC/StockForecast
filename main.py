import streamlit as st
from datetime import date
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import yfinance as yf

# Constants
START_DATE = "2010-01-01"
CURRENT_DATE = date.today().strftime("%Y-%m-%d")

# App Title
st.title("Stock Price Prediction and Analysis App")

# Stock Selection
available_stocks = ('GOOG', 'AAPL', 'MSFT', 'GME', 'TSLA', 'AMZN', 'META', 'NFLX', 'BTC-USD', 'ETH-USD')
chosen_stock = st.selectbox('Choose a stock or cryptocurrency for forecasting', available_stocks)

# Prediction Horizon
forecast_years = st.slider('How many years of prediction?', 1, 5)
forecast_period = forecast_years * 365

# Data Loading Function
@st.cache_data
def fetch_stock_data(ticker):
    """
    Download historical stock data from Yahoo Finance for a specific ticker.
    
    Args:
    ticker (str): Stock ticker symbol or cryptocurrency (e.g., 'AAPL', 'GOOG', 'BTC-USD').
    
    Returns:
    DataFrame: Stock data with columns for date, open, high, low, close, etc.
    """
    data = yf.download(ticker, START_DATE, CURRENT_DATE)
    data.reset_index(inplace=True)
    return data

# Display Loading Status
loading_message = st.text("Fetching data, please wait...")
stock_data = fetch_stock_data(chosen_stock)
loading_message.text("Data loaded successfully!")

# Show Raw Data
st.subheader(f'Raw Data for {chosen_stock}')
st.write(stock_data.tail())

# Plot the Historical Data
def render_price_chart():
    """
    Renders a line chart showing historical stock prices (open and close) with a range slider.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Open'], mode='lines', name='Opening Price'))
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Close'], mode='lines', name='Closing Price'))
    
    fig.update_layout(
        title=f'{chosen_stock} Price History',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        xaxis_rangeslider_visible=True
    )
    
    st.plotly_chart(fig)

render_price_chart()

# Data Preparation for Prophet Forecasting
forecast_data = stock_data[['Date', 'Close']].rename(columns={"Date": "ds", "Close": "y"})

# Prophet Model
model = Prophet()
model.fit(forecast_data)
future_dates = model.make_future_dataframe(periods=forecast_period)
forecast_result = model.predict(future_dates)

# Display Forecasted Data
st.subheader(f'Forecasted Data for {forecast_years} year(s)')
st.write(forecast_result[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

# Forecast Plot
st.subheader(f'Forecast Plot for {forecast_years} year(s)')
forecast_chart = plot_plotly(model, forecast_result)
st.plotly_chart(forecast_chart)

# Forecast Components Plot
st.subheader("Forecast Components")
components_chart = model.plot_components(forecast_result)
st.write(components_chart)

# Extra Feature: Moving Averages
def calculate_moving_average(data, window_size):
    """
    Calculates a moving average over a specified window size.
    
    Args:
    data (DataFrame): Data containing 'Close' prices.
    window_size (int): The number of periods for calculating the moving average.
    
    Returns:
    Series: Moving average of the stock's closing prices.
    """
    return data['Close'].rolling(window=window_size).mean()

# Moving Averages Feature
st.subheader(f"Moving Averages for {chosen_stock}")
window_size = st.slider("Select Moving Average Window (days)", 10, 100, 50)
moving_avg = calculate_moving_average(stock_data, window_size)
stock_data['Moving Average'] = moving_avg

# Plot Moving Averages
fig_ma = go.Figure()
fig_ma.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Close'], mode='lines', name='Closing Price'))
fig_ma.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Moving Average'], mode='lines', name=f'{window_size}-Day Moving Average'))

fig_ma.update_layout(
    title=f'{chosen_stock} Moving Average',
    xaxis_title='Date',
    yaxis_title='Price (USD)',
    xaxis_rangeslider_visible=True
)

st.plotly_chart(fig_ma)
