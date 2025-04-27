import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import streamlit as st

# Page config
st.set_page_config(
    page_title="Market Pulse",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar toggle
# Theme Toggle
# Theme Toggle
theme = st.sidebar.selectbox("🎨 Choose Theme", ("Dark", "Light"))

# Apply Themes
if theme == "Dark":
    st.markdown(
        """
        <style>
        /* App background and text */
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #0e1117;
            color: #ffffff;
        }
        /* Input fields and text areas */
        input, textarea, select, div[data-baseweb="select"] {
            background-color: #262730 !important;
            color: #ffffff !important;
            border: 1px solid #ffffff !important;
        }
        /* Input placeholders */
        input::placeholder, textarea::placeholder {
            color: #9e9e9e !important;
        }
        
        div[data-baseweb="menu"] {
            background-color: #1a1b23 !important; /* Updated background color */
            color: #ffffff!important;
            border: 1px solid #ffffff !important;
        }
        /* Individual dropdown options */
        div[data-baseweb="option"] {
            background-color: #1a1b23 !important;
            color: #ffffff !important;
        }
        /* When hovering over dropdown options */
        div[data-baseweb="option"]:hover {
            background-color: #1a1b23 !important;
            color: #ffffff !important;
        }
        /* Selectbox Dropdown header */
        div[data-baseweb="select"] >div {
            background-color: #1a1b23 !important;
            color: #00008B !important;
        }
        /* Buttons */
        button {
            background-color: #262730 !important;
            color: #ffffff !important;
        }
        /* Metric Cards */
        div[data-testid="metric-container"] {
            background-color: #262730;
            color: #ffffff;
            border: 1px solid #ffffff;
            border-radius: 10px;
            padding: 10px;
        }
        /* Headers */
        h1, h2, h3, h4, h5, h6, p, label, div {
            color: #ffffff !important;
        }
        /* Expander */
        details {
            background-color: #262730;
            color: #ffffff;
            border-radius: 10px;
            padding: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    plotly_theme = "plotly_dark"




else:
    st.markdown(
        """
        <style>
        /* App background and text */
        .stApp {
            background-color: #ffffff;
            color: #000000;
        }
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #ffffff;
            color: #000000;
        }
        /* Inputs and selects */
        input, textarea, select, div[data-baseweb="select"] > div {
            background-color: #f0f2f6 !important;
            color: #000000 !important;
            border: 1px solid #000000 !important;
        }
        /* Dropdown options */
        div[data-baseweb="menu"] > div {
            background-color: #f0f2f6 !important;
            color: #000000 !important;
        }
        /* Button */
        button {
            background-color: #f0f2f6 !important;
            color: #000000 !important;
        }
        /* Metric Cards */
        div[data-testid="metric-container"] {
            background-color: #f0f2f6;
            color: #000000;
            border: 1px solid #000000;
            border-radius: 10px;
            padding: 10px;
        }
        /* Headers */
        h1, h2, h3, h4, h5, h6, p, label, div {
            color: #000000 !important;
        }
        /* Expander */
        details {
            background-color: #f0f2f6;
            color: #000000;
            border-radius: 10px;
            padding: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    plotly_theme = "plotly_white"


# Custom CSS for Login Page
st.markdown(
    """
    <style>
    .login-container {
        max-width: 400px;
        padding: 2rem;
        margin: 0 auto;
        border: 1px solid #ddd;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .login-title {
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

import sqlite3
import streamlit as st

# SQLite Database Configuration
DATABASE_FILE = "users.db"

# Function to connect to SQLite database
def connect_db():
    return sqlite3.connect(DATABASE_FILE)

# Function to initialize the database
def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Authentication Functions
def authenticate(username, password):
    """Check if the username and password are valid."""
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT name FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return True, result[0]  # Return True and the user's name
    return False, None

def register_user(username, password, name):
    """Register a new user."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO users (username, password, name) VALUES (?, ?, ?)"
        cursor.execute(query, (username, password, name))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Handle duplicate username
        cursor.close()
        conn.close()
        return False

def login_page():
    """Display the login page and handle authentication."""

    st.markdown("<h2 class='login-title'>🔒 Stock App Login</h2>", unsafe_allow_html=True)
    
    # Tabs for Login and Register
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            auth_status, name = authenticate(username, password)
            if auth_status:
                st.session_state.authenticated = True
                st.session_state.current_user = name
                st.success("Login successful! Redirecting...")
            else:
                st.error("Invalid username/password")
    
    with tab2:
        new_username = st.text_input("Choose a Username", key="reg_username")
        new_password = st.text_input("Choose a Password", type="password", key="reg_password")
        new_name = st.text_input("Your Full Name", key="reg_name")
        
        if st.button("Register"):
            if new_username and new_password and new_name:
                if register_user(new_username, new_password, new_name):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Registration failed. Username might already exist.")
            else:
                st.error("Please fill in all fields.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()  # Stop execution to prevent access to the rest of the app
# Check Authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Show login page if not authenticated
if not st.session_state.authenticated:
    login_page()



# Add logout button to sidebar
# Modified logout button and welcome message
# Add logout button to sidebar
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout"):
    st.session_state.authenticated = False
    if 'current_user' in st.session_state:
        del st.session_state.current_user
    st.success("Logged out successfully! Redirecting to login page...")

# Show welcome message only if user is logged in
if 'current_user' in st.session_state:
    st.sidebar.markdown(f"### 👋 Welcome, {st.session_state.current_user}!")

# [Rest of your code remains unchanged...]
st.markdown(
    """
    <style>
    .sidebar .block-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .sidebar .stButton>button {
        width: 100%;
        padding: 10px;
        border-radius: 5px;
        background-color: #f0f2f6;
        border: 1px solid #ccc;
        text-align: left;
        font-size: 16px;
        color: #000;
    }
    .sidebar .stButton>button:hover {
        background-color: #e2e6ea;
        border-color: #bbb;
    }
    .sidebar .stMarkdown {
        margin-bottom: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# API Key and other original code continues...
API_KEY = "25BJR00EJM20NL4H"

# Stock Symbols
companies = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "Google (GOOGL)": "GOOGL",
    "Amazon (AMZN)": "AMZN",
    "Tesla (TSLA)": "TSLA",
    "Meta (META)": "META",
    "Netflix (NFLX)": "NFLX",
    "Nvidia (NVDA)": "NVDA",
    "IBM (IBM)": "IBM",
    "Intel (INTC)": "INTC"
}

# Fetch Stock Data Function
def get_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEY}&outputsize=full"
    response = requests.get(url)
    return response.json()

# Initialize session state
# Sidebar Navigation
st.sidebar.title("📌 Navigation")
st.sidebar.markdown("---")  # Adds a horizontal line for separation

# Sidebar Sections as Blocks
if st.sidebar.button("🏠 Home"):
    st.session_state.page = "🏠 Home"
if st.sidebar.button("📊 Stock Market Dashboard"):
    st.session_state.page = "📊 Stock Market Dashboard"
if st.sidebar.button("🚨 Price Alert"):
    st.session_state.page = "🚨 Price Alert"
if st.sidebar.button("🔄 Stock Comparison"):
    st.session_state.page = "🔄 Stock Comparison"
if st.sidebar.button("📊 Top Gainers & Losers"):  
    st.session_state.page = "📊 Top Gainers & Losers"


# Set default page if not set
if "page" not in st.session_state:
    st.session_state.page = "📊 Stock Market Dashboard"

# Additional Information Section
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ Information")
st.sidebar.info("""
This app provides real-time stock market data, price alerts, and advanced stock comparison tools. 
Use the navigation above to explore different features.
""")

# API Information Section
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔑 API Information")
st.sidebar.info("""
Data is fetched using the Alpha Vantage API. 
For more details, visit [Alpha Vantage](https://www.alphavantage.co/).
""")

# Contact Information Section
st.sidebar.markdown("---")
st.sidebar.markdown("### 📧 Contact")
st.sidebar.info("""
For any queries or feedback, please contact us at:
- Email: stockpulse@gmail.com
- Phone: +91 7013727704
""")

# Footer Section
st.sidebar.markdown("---")
st.sidebar.markdown("### 📅 Last Updated")
st.sidebar.info("""
Date: 2025-03-03  
Version: 4.1.9
""")
# Home Page
if st.session_state.page == "🏠 Home":
    # Add this at the top with other imports
    from datetime import datetime

    # NewsAPI Configuration (Get your free API key from https://newsapi.org/)
    NEWS_API_KEY = "e2d4e597c657407b9c1dee3a880cd670"  # Replace with your actual key

    def fetch_news():
        """Fetch financial news from NewsAPI"""
        url = f"https://newsapi.org/v2/everything?q=stocks&apiKey={NEWS_API_KEY}&sortBy=publishedAt&language=en"
        try:
            response = requests.get(url)
            news_data = response.json()
            return news_data.get('articles', [])[:6]  # Get first 6 articles
        except Exception as e:
            st.error(f"Error fetching news: {str(e)}")
            return []

    # Update the Home Page section
    st.markdown(
        """
        <style>
        .main-header {
            text-align: center;
            padding: 4rem 1rem;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            border-radius: 15px;
            margin-bottom: 2rem;
        }
        
        .news-card {
            background: #ffffff;  /* White background */
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
            margin-bottom: 1.5rem;
            overflow: hidden;
        }
        
        .news-card:hover {
            transform: translateY(-5px);
        }
        
        .news-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
        }
        
        .news-content {
            padding: 1.5rem;
        }
        
        .news-source {
            display: flex;
            align-items: center;
            gap: 8px;
            color: #666;  /* Medium gray for source text */
            margin-bottom: 0.5rem;
        }
        
        .source-logo {
            width: 20px;
            height: 20px;
            border-radius: 4px;
        }

        .news-content h4 {
            color: #1e3c72;  /* Dark blue for article titles */
            margin-bottom: 0.5rem;
        }

        .news-content p {
            color: #444;  /* Dark gray for article descriptions */
            line-height: 1.4;
        }

        .feature-card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 1.5rem;
            text-align: center;
            transition: transform 0.2s;
        }

        .feature-card:hover {
            transform: translateY(-5px);
        }

        .feature-card h3 {
            color: #1e3c72;  /* Dark blue for feature titles */
            margin-bottom: 0.5rem;
        }

        .feature-card p {
            color: #444;  /* Dark gray for feature descriptions */
        }

        .why-choose-us {
            background: #f8f9fa;  /* Light gray background */
            padding: 2rem;
            border-radius: 12px;
        }

        .why-choose-us h4 {
            color: #1e3c72;  /* Dark blue for section titles */
            margin-bottom: 0.5rem;
        }

        .why-choose-us p {
            color: #444;  /* Dark gray for section text */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Main Header
    st.markdown(
        '<div class="main-header">'
        '<h1 style="font-size: 3.5rem; margin-bottom: 1rem;">📈 Market Pulse</h1>'
        '<p style="font-size: 1.2rem; opacity: 0.9;">Your Gateway to Real-Time Financial Intelligence</p>'
        '</div>',
        unsafe_allow_html=True
    )

    # App Features Grid
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                """
                <div class="feature-card">
                <h3>📊 Live Market Data</h3>
                <p>Real-time stock prices, charts, and technical indicators</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                """
                <div class="feature-card">
                <h3>🚨 Smart Alerts</h3>
                <p>Custom price alerts and AI-powered market insights</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                """
                <div class="feature-card">
                <h3>📰 Market News</h3>
                <p>Curated financial news from trusted sources</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Real-Time News Section
    st.markdown("---")
    st.subheader("📰 Latest Market News")
    
    news_articles = fetch_news()
    
    if news_articles:
        cols = st.columns(2)
        for idx, article in enumerate(news_articles):
            with cols[idx % 2]:
                published_at = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%b %d, %Y %H:%M')
                
                st.markdown(
                    f"""
                    <a href="{article['url']}" target="_blank" style="text-decoration: none; color: inherit;">
                    <div class="news-card">
                        <img src="{article['urlToImage'] or 'https://source.unsplash.com/featured/?finance,news'}" class="news-image">
                        <div class="news-content">
                            <div class="news-source">
                                <img src="https://logo.clearbit.com/{article['source']['name'].lower().replace(' ', '')}.com" 
                                     class="source-logo" 
                                     onerror="this.style.display='none'">
                                <span>{article['source']['name']} • {published_at}</span>
                            </div>
                            <h4>{article['title']}</h4>
                            <p>{article['description'] or ''}</p>
                        </div>
                    </div>
                    </a>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.warning("Unable to fetch news at this moment. Please try again later.")

    # Additional Sections
    st.markdown("---")
    with st.container():
        st.subheader("📈 Why Choose Market Pulse?")
        st.markdown("""
        <div class="why-choose-us">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
                <div>
                    <h4>💡 Intelligent Analytics</h4>
                    <p>AI-powered market predictions and trend analysis powered by machine learning models</p>
                </div>
                <div>
                    <h4>🔔 Real-Time Alerts</h4>
                    <p>Customizable price alerts and breaking news notifications</p>
                </div>
                <div>
                    <h4>🌐 Global Coverage</h4>
                    <p>Track markets across multiple exchanges worldwide</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
# Stock Market Dashboard
elif st.session_state.page == "📊 Stock Market Dashboard":
    st.title("📊 Stock Market Dashboard")
    
    selected_company = st.selectbox("📌 Select a Company", list(companies.keys()))

    if st.button("🔍 Fetch Stock Data"):
        stock_data = get_stock_data(companies[selected_company])

        if "Time Series (5min)" in stock_data:
            df = pd.DataFrame.from_dict(stock_data["Time Series (5min)"], orient="index").astype(float)
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()
            df.columns = ["Open", "High", "Low", "Close", "Volume"]
            st.session_state.stock_data = df
        else:
            st.warning(f"⚠ Could not fetch data for {selected_company}.")
    
    if "stock_data" in st.session_state:
        df = st.session_state.stock_data
        current_price = df["Close"].iloc[-1]
        highest_price = df["High"].max()
        starting_price = df["Open"].iloc[0]

        st.subheader(f"📈 {selected_company} Stock Details")
        st.info(f"💰 Current Price: ${current_price:.2f}")
        st.success(f"📈 Highest Price: ${highest_price:.2f}")
        st.warning(f"🔽 Starting Price: ${starting_price:.2f}")

        # Intraday Graph
        fig = px.line(df, x=df.index, y="Close", title="📊 Intraday Stock Prices", 
                     labels={"Close": "Stock Price"}, template="plotly_dark")
        st.plotly_chart(fig)

        # Investment Calculator
        num_stocks = st.number_input("🛒 Enter number of stocks to buy", min_value=1, step=1)
        total_cost = num_stocks * current_price
        st.info(f"💰 Total Investment: ${total_cost:.2f}")

        if st.button("📊 Fetch Profit/Loss and Future Prediction"):
            # Prepare data for SVM
            df['Time'] = (df.index - df.index[0]).total_seconds() / 3600  # Convert time to hours
            X = df[['Time']]
            y = df['Close']
            
            # Train-test split (80:20)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Scale the data
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train SVM model
            svm_model = SVR(kernel='rbf')
            svm_model.fit(X_train_scaled, y_train)
            
            # Predict future prices
            future_hours = np.arange(df['Time'].max() + 1, df['Time'].max() + 24, 1).reshape(-1, 1)
            future_hours_scaled = scaler.transform(future_hours)
            predicted_prices = svm_model.predict(future_hours_scaled)
            
            # Create future dataframe
            future_times = pd.date_range(start=df.index[-1], periods=len(future_hours), freq="H")
            future_df = pd.DataFrame({"Time": future_times, "Predicted Price": predicted_prices})
            
            # Plot predictions
            st.subheader("📈 Future Stock Price Prediction (SVM Model)")
            fig_pred = px.line(future_df, x="Time", y="Predicted Price", 
                             title="📈 Predicted Stock Prices (Next 24 Hours)", 
                             template="plotly_dark")
            st.plotly_chart(fig_pred)
            
            # Profit/Loss Calculation
            future_price = predicted_prices[-1]
            future_value = num_stocks * future_price
            profit_loss = future_value - total_cost
            profit_loss_percentage = (profit_loss / total_cost) * 100

            if profit_loss > 0:
                st.success(f"📈 Profit: ${profit_loss:.2f} ({profit_loss_percentage:.2f}%)")
                st.info(f"💡 Recommendation: Consider selling when price reaches ${future_price:.2f}")
            else:
                st.error(f"📉 Loss: ${abs(profit_loss):.2f} ({abs(profit_loss_percentage):.2f}%)")
                st.warning("💡 Recommendation: Do not invest at this time")




# Price Alert Section
# Price Alert Section
elif st.session_state.page == "🚨 Price Alert":
    st.title("🚨 Price Alert")

    if "alerts" not in st.session_state:
        st.session_state.alerts = []

    # Set Alert
    st.subheader("🔔 Set Price Alert")
    selected_company = st.selectbox("📌 Choose a Company", list(companies.keys()))
    alert_price = st.number_input("💰 Enter Alert Price", min_value=0.0, format="%.2f")
    user_email = st.text_input("📧 Enter your Email ID", placeholder="yourname@example.com")

    if st.button("✅ Set Alert"):
        if user_email:
            st.session_state.alerts.append({
                "company": selected_company,
                "symbol": companies[selected_company],
                "alert_price": alert_price,
                "email": user_email
            })
            st.success(f"🚀 Alert set for {selected_company} at ${alert_price:.2f}. You will be notified at {user_email}.")
        else:
            st.error("❌ Please enter a valid Email ID.")

    # Active Alerts
    st.subheader("📋 Active Alerts")
    if st.session_state.alerts:
        for i, alert in enumerate(st.session_state.alerts):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{i + 1}. {alert['company']} - Alert at ${alert['alert_price']:.2f} (Email: {alert['email']})")
            with col2:
                if st.button(f"❌ Clear {i+1}"):
                    st.session_state.alerts.pop(i)
                    st.experimental_rerun()
    else:
        st.info("No active alerts.")

    # Check Alerts
    st.subheader("🔍 Check Alerts")
    if st.button("🔔 Check Alerts Now"):
        for alert in st.session_state.alerts:
            stock_data = get_stock_data(alert["symbol"])
            if "Time Series (5min)" in stock_data:
                df = pd.DataFrame.from_dict(stock_data["Time Series (5min)"], orient="index").astype(float)
                if "Close" in df.columns:
                    current_price = df["Close"].iloc[-1]
                    if current_price >= alert["alert_price"]:
                        st.success(f"🚨 {alert['company']} Alert Triggered! Current: ${current_price:.2f}")
                        # Here, you can add an email notification system using SMTP or a third-party API.
                    else:
                        st.info(f"⏳ {alert['company']} at ${current_price:.2f} (Target: ${alert['alert_price']:.2f})")
                else:
                    st.warning(f"⚠ Missing data for {alert['company']}")
            else:
                st.warning(f"⚠ Couldn't fetch data for {alert['company']}")
# Stock Comparison Section (Updated)
elif st.session_state.page == "🔄 Stock Comparison":
    st.title("🔄 Advanced Stock Comparison")

    company_list = list(companies.keys())
    
    # Dynamic stock selection
    stock1 = st.selectbox("📌 Select First Company", company_list, key="stock1")
    stock2 = st.selectbox("📌 Select Second Company", 
                         [c for c in company_list if c != stock1], 
                         key="stock2")

    if st.button("🔍 Compare Stocks"):
        stock1_data = get_stock_data(companies[stock1])
        stock2_data = get_stock_data(companies[stock2])

        if "Time Series (5min)" in stock1_data and "Time Series (5min)" in stock2_data:
            # Process data
            df1 = pd.DataFrame(stock1_data["Time Series (5min)"]).T.astype(float)
            df2 = pd.DataFrame(stock2_data["Time Series (5min)"]).T.astype(float)
            df1.index = pd.to_datetime(df1.index)
            df2.index = pd.to_datetime(df2.index)
            
            # Price Comparison
            comparison_df = pd.DataFrame({
                stock1: df1["4. close"],
                stock2: df2["4. close"]
            }).sort_index()

            st.subheader("📊 Price Trend Comparison")
            fig = px.line(comparison_df, template="plotly_dark", 
                         title="Hourly Price Movement Comparison")
            st.plotly_chart(fig)

            # Advanced Analysis
            st.subheader("📈 Actionable Insights")
            
            # Correlation Analysis with Strategy Implications
            correlation = comparison_df[stock1].corr(comparison_df[stock2])
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Correlation Coefficient", f"{correlation:.2f}")
            with col2:
                if correlation > 0.8:
                    st.success("Strong Positive Correlation")
                    st.write("💡 Strategy: Consider pairs trading or sector-based investing")
                elif correlation < -0.8:
                    st.warning("Strong Negative Correlation")
                    st.write("💡 Strategy: Potential hedging opportunity")
                else:
                    st.info("Weak Correlation")
                    st.write("💡 Strategy: Good for portfolio diversification")

            # Volatility Analysis with Risk Assessment
            st.subheader("📉 Volatility Comparison")
            vol1 = comparison_df[stock1].pct_change().std() * 100
            vol2 = comparison_df[stock2].pct_change().std() * 100
            vol_df = pd.DataFrame({
                "Stock": [stock1, stock2],
                "Volatility": [vol1, vol2]
            })
            fig_vol = px.bar(vol_df, x="Stock", y="Volatility", 
                            color="Stock", template="plotly_dark",
                            title="Price Volatility (Standard Deviation of Daily Returns)")
            st.plotly_chart(fig_vol)

            if vol1 > vol2:
                st.warning(f"{stock1} is {vol1/vol2:.1f}x more volatile than {stock2}")
                st.write("💡 Consider: Higher risk/reward potential in", stock1)
            else:
                st.info(f"{stock2} is {vol2/vol1:.1f}x more volatile than {stock1}")
                st.write("💡 Consider:", stock2, "might offer better short-term trading opportunities")

            # Momentum Analysis with Trend Insights
            st.subheader("🚀 Momentum Analysis")
            momentum1 = (comparison_df[stock1].iloc[-1] / comparison_df[stock1].iloc[0] - 1) * 100
            momentum2 = (comparison_df[stock2].iloc[-1] / comparison_df[stock2].iloc[0] - 1) * 100
            mom_df = pd.DataFrame({
                "Stock": [stock1, stock2],
                "Momentum": [momentum1, momentum2]
            })
            fig_momentum = px.bar(mom_df, x="Stock", y="Momentum", 
                                 color="Stock", template="plotly_dark",
                                 title="Percentage Change Over Period")
            st.plotly_chart(fig_momentum)

            if momentum1 > momentum2:
                st.success(f"{stock1} shows stronger upward momentum")
                st.write("💡 Consider: Potential buying opportunity in", stock1)
            else:
                st.warning(f"{stock2} demonstrates better recent performance")
                st.write("💡 Consider: Investigate", stock2, "for potential investments")

            # Final Recommendations
            st.subheader("💡 Investment Recommendations")
            if correlation > 0.7 and abs(momentum1 - momentum2) > 5:
                st.success("Pairs Trading Opportunity")
                st.write("- Buy the outperforming stock")
                st.write("- Short the underperforming stock")
            elif vol1 > 5 and vol2 > 5:
                st.warning("High Volatility Alert")
                st.write("- Consider options strategies")
                st.write("- Implement stop-loss orders")
            else:
                st.info("Diversification Opportunity")
                st.write("- Consider balanced portfolio allocation")

        else:
            st.warning("⚠ Failed to fetch comparison data")

# Top Gainer & Loser Section
elif st.session_state.page == "📊 Top Gainers & Losers":
    st.title("📈 Top Gainer & Loser")

    gainers = {}
    losers = {}
    for company, symbol in companies.items():
        stock_data = get_stock_data(symbol)
        
        # Check if data is fetched successfully and contains the required key
        if stock_data and "Time Series (5min)" in stock_data:
            df = pd.DataFrame.from_dict(stock_data["Time Series (5min)"], orient="index", dtype=float)
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()
            df.columns = ["Open", "High", "Low", "Close", "Volume"]

            open_price = df.iloc[0]["Open"]
            close_price = df.iloc[-1]["Close"]
            change = close_price - open_price

            if change > 0:
                gainers[company] = change
            else:
                losers[company] = change
        else:
            st.warning(f"⚠ Could not fetch data for {company} ({symbol}).")

    # Display Top Gainer
    if gainers:
        top_gainer = max(gainers, key=gainers.get)
        st.subheader(f"📈 Top Gainer: {top_gainer}")
        symbol = companies[top_gainer]
        stock_data = get_stock_data(symbol)
        
        if stock_data and "Time Series (5min)" in stock_data:
            df = pd.DataFrame.from_dict(stock_data["Time Series (5min)"], orient="index", dtype=float)
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()
            df.columns = ["Open", "High", "Low", "Close", "Volume"]

            st.metric(label="📈 Open Price", value=f"${df.iloc[0]['Open']:.2f}")
            fig_gainer = px.line(df, x=df.index, y="Close", title=f"{top_gainer} Stock Price")
            st.plotly_chart(fig_gainer)
        else:
            st.warning(f"⚠ Could not fetch data for {top_gainer} ({symbol}).")

    # Display Top Loser
    if losers:
        top_loser = min(losers, key=losers.get)
        st.subheader(f"📉 Top Loser: {top_loser}")
        symbol = companies[top_loser]
        stock_data = get_stock_data(symbol)
        
        if stock_data and "Time Series (5min)" in stock_data:
            df = pd.DataFrame.from_dict(stock_data["Time Series (5min)"], orient="index", dtype=float)
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()
            df.columns = ["Open", "High", "Low", "Close", "Volume"]

            st.metric(label="📉 Open Price", value=f"${df.iloc[0]['Open']:.2f}")
            fig_loser = px.line(df, x=df.index, y="Close", title=f"{top_loser} Stock Price")
            st.plotly_chart(fig_loser)
        else:
            st.warning(f"⚠ Could not fetch data for {top_loser} ({symbol}).")
# AI Stock Recommendation Section
elif st.session_state.page == "🤖 AI Stock Recommendation":
    st.title("🤖 AI-powered Stock Recommendations")

    # Fetch data
    data = {}
    for company, symbol in companies.items():
        stock_data = get_stock_data(symbol)
        if "Time Series (5min)" in stock_data:
            df = pd.DataFrame.from_dict(stock_data["Time Series (5min)"], orient="index").astype(float)
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()

            # Calculate features
            close_prices = df["4. close"]
            returns = close_prices.pct_change()
            momentum = (close_prices.iloc[-1] / close_prices.iloc[0]) - 1
            volatility = returns.std()
            avg_volume = df["5. volume"].mean()

            data[company] = {
                "momentum": momentum,
                "volatility": volatility,
                "avg_volume": avg_volume
            }

    if data:
        # Prepare data for ML
        feature_df = pd.DataFrame.from_dict(data, orient="index")

        # Create simple label: 1 if momentum > 0 else 0
        feature_df["target"] = feature_df["momentum"].apply(lambda x: 1 if x > 0 else 0)

        # Split features and target
        X = feature_df[["momentum", "volatility", "avg_volume"]]
        y = feature_df["target"]

        # Train Random Forest Classifier
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier()
        model.fit(X, y)

        # Predict
        feature_df["prediction"] = model.predict(X)

        # Show recommended stocks
        st.subheader("📈 Recommended Stocks to Buy:")
        recommended = feature_df[feature_df["prediction"] == 1]
        
        if not recommended.empty:
            st.table(recommended[["momentum", "volatility", "avg_volume"]])
        else:
            st.info("No strong buy signals at the moment.")
    else:
        st.warning("⚠ Could not fetch data for AI recommendation.")
