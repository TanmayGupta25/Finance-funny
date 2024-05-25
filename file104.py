import streamlit as st
import yfinance as yf
import pandas as pd
import requests

# Create a multi-page app
st.set_page_config(page_title="Financial Dashboard", page_icon=":chart:", layout="wide")

# Add a sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page", ["Commodities", "ETFs", "Underpriced Stocks", "Cryptocurrencies", "Financial Statement Analysis", "Portfolio Builder", "News and Insights"])

# Commodities page
if page == "Commodities":
    st.title("Commodities")
    commodity_tickers = ["GC=F", "CL=F", "NG=F"]
    commodity_names = ["Gold", "Crude Oil", "Natural Gas"]
    for ticker, name in zip(commodity_tickers, commodity_names):
        data = yf.download(ticker, period="1y")
        st.write(f"{name} Chart")
        st.line_chart(data["Close"])

# ETFs page
elif page == "ETFs":
    st.title("ETFs")
    etf_tickers = ["SPY", "QQQ", "DIA"]
    etf_names = ["S&P 500", "Nasdaq-100", "Dow Jones"]
    for ticker, name in zip(etf_tickers, etf_names):
        data = yf.download(ticker, period="1y")
        st.write(f"{name} Chart")
        st.line_chart(data["Close"])

# Underpriced Stocks page
elif page == "Underpriced Stocks":
    st.title("Underpriced Stocks")
    stock_tickers = ["AAPL", "GOOG", "MSFT", "AMZN", "FB"]
    pe_ratio_threshold = 20
    underpriced_stocks = []
    for stock in stock_tickers:
        data = yf.download(stock, period="1d")
        pe_ratio = data["PE Ratio"][-1]
        if pe_ratio < pe_ratio_threshold:
            underpriced_stocks.append((stock, pe_ratio))
    if underpriced_stocks:
        st.write("Underpriced Stocks:")
        for stock, pe_ratio in underpriced_stocks:
            st.write(f"{stock}: P/E Ratio = {pe_ratio:.2f}")
    else:
        st.write("No underpriced stocks found")

# Cryptocurrencies page
elif page == "Cryptocurrencies":
    st.title("Cryptocurrencies")
    crypto_tickers = ["BTC-USD", "ETH-USD"]
    crypto_names = ["Bitcoin", "Ethereum"]
    for ticker, name in zip(crypto_tickers, crypto_names):
        data = yf.download(ticker, period="1y")
        st.write(f"{name} Chart")
        st.line_chart(data["Close"])

# Financial Statement Analysis page
elif page == "Financial Statement Analysis":
    st.title("Financial Statement Analysis")
    ticker_input = st.text_input("Enter a ticker symbol")
    if ticker_input:
        ticker = yf.Ticker(ticker_input)
        st.write("Balance Sheet")
        st.write(ticker.balance_sheet)
        st.write("Income Statement")
        st.write(ticker.financials)
        st.write("Cash Flow Statement")
        st.write(ticker.cashflow)

# Portfolio Builder page
elif page == "Portfolio Builder":
    st.title("Portfolio Builder")
    stocks = []
    for i in range(5):  # Allow users to input up to 5 stocks
        stock_input = st.text_input(f"Enter stock {i+1} ticker symbol")
        if stock_input:
            stocks.append(stock_input)
    if stocks:
        portfolio_value = 0
        for stock in stocks:
            data = yf.download(stock, period="1d")
            portfolio_value += data["Close"][-1]  # Add the current price of each stock to the portfolio value
        st.write(f"Portfolio value: ${portfolio_value:.2f}")

# News and Insights page
elif page == "News and Insights":
    st.title("News and Insights")
    news_api_key = "YOUR_NEWS_API_KEY"  # Replace with your NewsAPI key
    news_response = requests.get(f"https://newsapi.org/v2/everything?q=finance&apiKey={news_api_key}")
    news_articles = news_response.json()["articles"]
    if news_articles:
        st.write("Financial News:")
        for article in news_articles:
            st.write(f"{article['title']}: {article['description']}")
    else:
        st.write("No news articles found")

# Run the app
if __name__ == "__main__":
    st.write("Financial Dashboard")
    