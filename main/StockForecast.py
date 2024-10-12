import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go

# Constants for the application
START_DATE = "2010-01-01"  # The start date for fetching historical stock data
CURRENT_DATE = date.today().strftime("%Y-%m-%d")  # Current date for the data fetch

# Custom CSS for sidebar
st.markdown(
    """
    <style>
    .css-1aumxhk {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        height: 100vh;
    }
    .sidebar-space {
        height: 100px;  /* Space above the information in the sidebar */
    }
    .sidebar-content {
        overflow-y: hidden;  /* Hide scrollbar */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for stock selection
st.sidebar.header("📊 StockForecast Options")

# Stock selection dropdown and prediction horizon slider in sidebar
chosen_stock = st.sidebar.selectbox(
    'Choose a stock for forecasting',
    ['', 'AAPL', 'MSFT', 'AMZN', 'GOOG', 'GOOGL', 'BRK-B', 'TSLA', 'META', 
     'NVDA', 'V', 'JPM', 'JNJ', 'WMT', 'PG', 'MA', 'HD', 'UNH', 'XOM', 
     'BAC', 'KO', 'PEP', 'LLY', 'AVGO', 'MRK', 'PFE', 'COST', 'DIS', 
     'ABBV', 'NFLX', 'CVX', 'ABT', 'CSCO', 'MCD', 'CRM', 'ACN', 'NEE', 
     'TMUS', 'TXN', 'LIN', 'DHR', 'PM', 'VZ', 'TMO', 'ORCL', 'ADBE', 
     'NKE', 'SCHW', 'WFC', 'UPS', 'AMGN', 'MDT', 'HON', 'INTC', 'MS', 
     'RTX', 'LOW', 'BMY', 'UNP', 'QCOM', 'ELV', 'SBUX', 'BA', 'GS', 
     'AMD', 'SPGI', 'DE', 'PLD', 'LMT', 'BLK', 'AXP', 'CVS', 'ISRG', 
     'AMT', 'BKNG', 'ZTS', 'SYK', 'GILD', 'USB', 'TJX', 'COP', 'TGT', 
     'F', 'CAT', 'MMC', 'MO', 'CCI', 'PNC', 'GE', 'EQIX', 'CI', 'ICE', 
     'ITW', 'NSC', 'MDLZ', 'CB', 'MMC', 'SO', 'DUK', 'GM', 'VRTX', 
     'SHW', 'TFC', 'MCO', 'NOW', 'HUM', 'CL', 'AON', 'CSX', 'KMB', 
     'PGR', 'WM', 'ADI', 'ROP', 'CDNS', 'EW', 'REGN', 'CME', 'MRNA', 
     'EOG', 'IDXX', 'FIS', 'TRV', 'AEP', 'PSA', 'FDX', 'FTNT', 'BSX', 
     'OXY', 'MSCI', 'KHC', 'ORLY', 'APD', 'HLT', 'CTAS', 'KR', 'WELL', 
     'DLR', 'EA', 'SRE', 'WMB', 'MTD', 'EBAY', 'ROST', 'CMG', 'RSG', 
     'CTSH', 'D', 'IQV', 'HCA', 'ZBH', 'PRU', 'HSY', 'MPC', 'DXCM', 
     'LRCX', 'SNPS', 'ANET', 'PH', 'CDW', 'STZ', 'FISV', 'NOC', 'EXC', 
     'MNST', 'TT', 'TEL', 'HPQ', 'WAT', 'BAX', 'GLW', 'VLO', 'ED', 
     'KEYS', 'EMR', 'CHD', 'ODFL', 'PAYC', 'BF-B', 'SYY', 'TTWO', 
     'K', 'CTVA', 'DTE', 'PPL', 'AFL', 'CMS', 'ATO', 'FTV', 'CTXS', 
     'SBAC', 'SWK', 'KMX', 'FMC', 'CPRT', 'DRI', 'MTCH', 'SPOT', 
     'BBY', 'ETSY', 'DISH', 'GPN', 'FE', 'TAP', 'ZBRA', 'AKAM', 
     'VTR', 'BLL', 'NVR', 'PKI', 'MKTX', 'HIG', 'VFC', 'MAS', 'WRB', 
     'XYL', 'CLX', 'NRG', 'ALLE', 'PFG', 'ROL', 'SIVB', 'RJF', 
     'NDSN', 'NTAP', 'PKG', 'BEN', 'LUMN', 'PWR', 'TRMB', 'UAL', 
     'RF', 'ZION', 'RCL', 'IRM', 'LKQ', 'CBOE', 'BRO', 'GL', 
     'TPR', 'WHR', 'CF', 'FFIV', 'PHM', 'HSIC', 'UHS', 'PBCT', 
     'TOL', 'J', 'CINF', 'MAS', 'WRK', 'LKQ', 'NI', 'DOV', 
     'JBHT', 'AEE', 'SEE', 'NDAQ', 'HBI', 'NUE', 'HRL', 'RSG', 
     'AMP', 'MHK', 'WY', 'TXT', 'AIV', 'AVTR']
)

forecast_years = st.sidebar.slider('How many years of prediction?', 1, 5)  # Slider for prediction years
forecast_period = forecast_years * 365  # Calculate total forecast period in days

# Main Title and Subtitle
st.markdown('<h1 style="text-align: center;">📊 StockForecast </h1>', unsafe_allow_html=True)
st.markdown('<h2 style="text-align: center;">Stock Prediction and Analysis Application 📈</h2>', unsafe_allow_html=True)

# Function to fetch historical stock data
@st.cache_data
def fetch_stock_data(ticker):
    data = yf.download(ticker, START_DATE, CURRENT_DATE)  # Fetch stock data
    data.reset_index(inplace=True)  # Reset index for easier manipulation
    return data

# Display data only if a stock is selected
if chosen_stock:
    stock_data = fetch_stock_data(chosen_stock)  # Fetch selected stock data

    # Display the last few rows of raw stock data
    st.subheader(f'📈 Raw Data for {chosen_stock}')
    st.write(stock_data.tail())

    # Function to render the price chart
    def render_price_chart():
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=stock_data['Date'],
            y=stock_data['Open'],
            mode='lines',
            name='Opening Price',
            line=dict(color='blue', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=stock_data['Date'],
            y=stock_data['Close'],
            mode='lines',
            name='Closing Price',
            line=dict(color='red', width=2, dash='dash')
        ))

        fig.update_layout(
            title=f'{chosen_stock} Price History',
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            xaxis_rangeslider_visible=True
        )

        st.plotly_chart(fig)  # Display the price chart

    render_price_chart()  # Call the function to render the price chart

    # Prepare data for the Prophet model
    forecast_data = stock_data[['Date', 'Close']].rename(columns={"Date": "ds", "Close": "y"})

    # Create and fit the Prophet model
    model = Prophet()
    model.fit(forecast_data)
    future_dates = model.make_future_dataframe(periods=forecast_period)  # Create future dates
    forecast_result = model.predict(future_dates)  # Generate forecast

    # Display the forecasted data
    st.subheader(f'🔮 Forecasted Data for {forecast_years} year(s)')
    st.write(forecast_result[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

    # Display the forecast plot
    st.subheader(f'📊 Forecast Plot for {forecast_years} year(s)')
    forecast_chart = plot_plotly(model, forecast_result)
    st.plotly_chart(forecast_chart)

    # Display forecast components plot
    st.subheader("📉 Forecast Components")
    components_chart = model.plot_components(forecast_result)
    st.write(components_chart)

# Moving Averages Feature
    def calculate_moving_average(data, window_size):
        return data['Close'].rolling(window=window_size).mean()

    st.subheader(f"📋 Moving Averages for {chosen_stock}")
    window_size = st.slider("Select Moving Average Window (days)", 10, 100, 50)
    moving_avg = calculate_moving_average(stock_data, window_size)
    stock_data['Moving Average'] = moving_avg

# Plot Moving Averages 
    fig_ma = go.Figure()
    fig_ma.add_trace(go.Scatter(
        x=stock_data['Date'],
        y=stock_data['Close'],
        mode='lines',
        name='Closing Price',
        line=dict(color='red', width=2)
    ))
    fig_ma.add_trace(go.Scatter(
        x=stock_data['Date'],
        y=stock_data['Moving Average'],
        mode='lines',
        name=f'{window_size}-Day Moving Average',
        line=dict(color='blue', width=2)
    ))

    fig_ma.update_layout(
        title=f'{chosen_stock} Moving Average',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        xaxis_rangeslider_visible=True,
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='white')
    )

    st.plotly_chart(fig_ma)


# sidebar additional info
with st.sidebar:
    st.markdown('<div class="sidebar-space"></div>', unsafe_allow_html=True)  # Adding space
    st.markdown("##### About StockForecast")
    st.write("""
    This app uses Prophet to forecast stock prices based on historical data from Yahoo Finance. 
    Predict the future of stocks and major cryptocurrencies!
    """)
    st.write("Created by **SailinaC**")
