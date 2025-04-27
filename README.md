# Market Pulse - Stock Analysis & Prediction Web App

**Market Pulse** is a web application that allows users to analyze stock data and make predictions using machine learning models. The app fetches real-time stock data, performs technical analysis (like RSI and SMA), and predicts future stock prices using a Random Forest model. It also integrates the latest stock news and provides a user-friendly interface powered by Streamlit.

## Features

- **Stock Data Analysis**: Fetch and analyze stock data using the Alpha Vantage API.
- **Technical Indicators**: Calculate and display technical indicators like RSI and SMA for a given stock.
- **Stock Price Prediction**: Predict future stock prices using a trained Random Forest model.
- **Latest Stock News**: Fetch the latest news articles related to the selected stock.
- **Dark Mode**: Toggle between light and dark mode for a better user experience.
- **Interactive Interface**: Built with Streamlit for an interactive web interface.

## Prerequisites

Make sure you have the following installed on your local machine:

- **Python** 3.8+
- **pip** (Python package installer)

You will also need to create API keys for the following services:

- **Alpha Vantage API**: [Get your API Key here](https://www.alphavantage.co/support/#api-key)
- **NewsAPI**: [Get your API Key here](https://newsapi.org/)

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/yourusername/market-pulse.git
    cd market-pulse
    ```

2. Install the required Python dependencies using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

3. Update the following variables in `app.py` with your own API keys:

    - `alpha_vantage_api_key = "YOUR_ALPHA_VANTAGE_API_KEY"`
    - `news_api_key = "YOUR_NEWS_API_KEY"`

## Usage

1. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

2. Open your web browser and go to the URL shown in the terminal (typically `http://localhost:8501`).

3. Select a stock from the dropdown and explore its stock data, technical indicators, prediction, and latest news.

## Folder Structure

```plaintext
market_pulse/
│
├── app.py              # Main app file (Streamlit interface)
├── requirements.txt    # List of dependencies
└── assets/             # Static files like images, etc.
