import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go

START_DATE = "2010-01-01"
CURRENT_DATE = date.today().strftime("%Y-%m-%d")

st.sidebar.header("📊 StockForecast Options")

chosen_stock = st.sidebar.selectbox(
    'Choose a stock for forecasting',
    ['', 'AAPL', 'MSFT', 'AMZN', 'GOOG', 'GOOGL', 'BRK-B', 'TSLA', 'META', 'NVDA', 'V', 'JPM', 'JNJ', 
    'WMT', 'PG', 'MA', 'HD', 'UNH', 'XOM', 'BAC', 'KO', 'PEP', 'LLY', 'AVGO', 'MRK', 'PFE', 
    'COST', 'DIS', 'ABBV', 'NFLX', 'CVX', 'ABT', 'CSCO', 'MCD', 'CRM', 'ACN', 'NEE', 'TMUS', 
    'TXN', 'LIN', 'DHR', 'PM', 'VZ', 'TMO', 'ORCL', 'ADBE', 'NKE', 'SCHW', 'WFC', 'UPS', 'AMGN', 
    'MDT', 'HON', 'INTC', 'MS', 'RTX', 'LOW', 'BMY', 'UNP', 'QCOM', 'ELV', 'SBUX', 'BA', 'GS', 
    'AMD', 'SPGI', 'DE', 'PLD', 'LMT', 'BLK', 'AXP', 'CVS', 'ISRG', 'AMT', 'BKNG', 'ZTS', 'SYK', 
    'GILD', 'USB', 'TJX', 'COP', 'TGT', 'F', 'CAT', 'MMC', 'MO', 'CCI', 'PNC', 'GE', 'EQIX', 
    'CI', 'ICE', 'ITW', 'NSC', 'MDLZ', 'CB', 'MMC', 'SO', 'DUK', 'GM', 'VRTX', 'SHW', 'TFC', 
    'MCO', 'NOW', 'HUM', 'CL', 'AON', 'CSX', 'KMB', 'PGR', 'WM', 'ADI', 'ROP', 'CDNS', 'EW', 
    'REGN', 'CME', 'MRNA', 'EOG', 'IDXX', 'FIS', 'TRV', 'AEP', 'PSA', 'FDX', 'FTNT', 'BSX', 
    'OXY', 'MSCI', 'KHC', 'ORLY', 'APD', 'HLT', 'CTAS', 'KR', 'WELL', 'DLR', 'EA', 'SRE', 'WMB', 
    'MTD', 'EBAY', 'ROST', 'CMG', 'RSG', 'CTSH', 'D', 'IQV', 'HCA', 'ZBH', 'PRU', 'HSY', 'MPC', 
    'DXCM', 'LRCX', 'SNPS', 'ANET', 'PH', 'CDW', 'STZ', 'FISV', 'NOC', 'EXC', 'MNST', 'TT', 
    'TEL', 'HPQ', 'WAT', 'BAX', 'GLW', 'VLO', 'ED', 'KEYS', 'EMR', 'CHD', 'ODFL', 'PAYC', 'BF-B', 
    'SYY', 'TTWO', 'K', 'CTVA', 'DTE', 'PPL', 'AFL', 'CMS', 'ATO', 'FTV', 'CTXS', 'SBAC', 'SWK', 
    'KMX', 'FMC', 'CPRT', 'DRI', 'MTCH', 'SPOT', 'BBY', 'ETSY', 'DISH', 'GPN', 'FE', 'TAP', 'ZBRA', 
    'AKAM', 'VTR', 'BLL', 'NVR', 'PKI', 'MKTX', 'HIG', 'VFC', 'MAS', 'WRB', 'XYL', 'CLX', 'NRG', 
    'ALLE', 'PFG', 'ROL', 'SIVB', 'RJF', 'NDSN', 'NTAP', 'PKG', 'BEN', 'LUMN', 'PWR', 'TRMB', 
    'UAL', 'RF', 'ZION', 'RCL', 'IRM', 'LKQ', 'CBOE', 'BRO', 'GL', 'TPR', 'WHR', 'CF', 'FFIV', 
    'PHM', 'HSIC', 'UHS', 'PBCT', 'TOL', 'J', 'CINF', 'MAS', 'WRK', 'LKQ', 'NI', 'DOV', 'JBHT', 
    'AEE', 'SEE', 'NDAQ', 'HBI', 'NUE', 'HRL', 'RSG', 'AMP', 'MHK', 'WY', 'TXT', 'AIV', 'AVTR']
)

if 'forecast_years' not in st.session_state:
    st.session_state.forecast_years = 1

forecast_years = st.sidebar.slider('How many years of prediction?', 1, 5, value=st.session_state.forecast_years)

st.sidebar.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)

st.sidebar.markdown("##### About StockForecast")
st.sidebar.write("""
This app uses Prophet to forecast stock prices based on historical data from Yahoo Finance. Predict the future of stocks and major cryptocurrencies!
""")
st.sidebar.write("Created by **SailinaC**")

@st.cache_data
def fetch_stock_data(ticker):
    data = yf.download(ticker, START_DATE, CURRENT_DATE)
    data.reset_index(inplace=True)
    return data

if chosen_stock:
    stock_data = fetch_stock_data(chosen_stock)

    st.subheader(f'📈 Raw Data for {chosen_stock}')
    st.write(stock_data.tail())

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
            xaxis_rangeslider_visible=True,
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='white')
        )

        st.plotly_chart(fig)

    render_price_chart()

    forecast_data = stock_data[['Date', 'Close']].rename(columns={"Date": "ds", "Close": "y"})

    model = Prophet()
    model.fit(forecast_data)
    future_dates = model.make_future_dataframe(periods=forecast_years * 365)
    forecast_result = model.predict(future_dates)

    st.subheader(f'🔮 Forecasted Data for {forecast_years} year(s)')
    st.write(forecast_result[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

    fig_forecast = plot_plotly(model, forecast_result)
    fig_forecast.update_layout(
        title=f'{chosen_stock} Price Forecast',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig_forecast)

    # Moving Average
    window_size = st.sidebar.selectbox('Select Moving Average Window Size:', [5, 10, 20, 50, 100, 200])

    stock_data['Moving Average'] = stock_data['Close'].rolling(window=window_size).mean()

    fig_ma = go.Figure()
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
