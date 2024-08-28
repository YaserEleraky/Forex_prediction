import streamlit as st
import warnings
import joblib 
import pandas 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sklearn
from sklearn.exceptions import InconsistentVersionWarning
warnings.filterwarnings(action='ignore', category=InconsistentVersionWarning)

# Set the page configuration
st.set_page_config(
    page_title="Forex Market Analysis",
    page_icon="💹",
    layout="wide"
)

# Home Page Title
st.markdown("<h1 style='text-align: center;'>💹Empowering Your Forex Trading Journey</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>📈Stay ahead in the market with real-time insights and analysis.</h2>", unsafe_allow_html=True)

# Introduction to Forex Trading
st.markdown("<h2 style='text-align: center; color: #4CAF50;'>Welcome to the Forex Market Analysis Platform</h2>", unsafe_allow_html=True)
st.write("""
    The Forex market, or Foreign Exchange market, is the largest financial market in the world, operating 24 hours a day, five days a week. 
    It plays a vital role in the global economy by setting exchange rates and facilitating international trade and investment. 
    Our platform offers essential tools and insights to help you navigate this dynamic market with confidence.
""")
st.markdown("---")

# Detailed Explanations of Forex Market Topics
st.markdown("<h2 style='text-align: center; color: #4CAF50;'>Understanding Key Forex Market Topics</h2>", unsafe_allow_html=True)

# Forex Market
st.markdown("<h3 style='color: #2196F3;'>1. Forex Market</h3>", unsafe_allow_html=True)
st.write("""
    **Topic: Understanding the Forex Market**

    **Explanation:** 
    The foreign exchange market, commonly known as forex or FX, is a global marketplace for trading national currencies against one another. 
    It is the largest and most liquid financial market in the world, with daily trading volumes exceeding $6 trillion. 
    The forex market operates 24 hours a day, five days a week, and involves a wide range of participants including banks, financial institutions, corporations, governments, and individual traders. 
    Currencies are traded in pairs (e.g., EUR/USD, GBP/JPY), and the market is influenced by various factors including economic indicators, geopolitical events, and market sentiment.
""")
st.markdown("---")

# Economic Calendar
st.markdown("<h3 style='color: #2196F3;'>2. Economic Calendar</h3>", unsafe_allow_html=True)
st.write("""
    **Topic: The Importance of the Economic Calendar in Forex Trading**

    **Explanation:** 
    An economic calendar is a tool used by forex traders to keep track of economic events and data releases that can impact currency markets. 
    These events include interest rate decisions, employment reports, inflation data, and GDP figures. 
    The economic calendar provides scheduled times and forecasts for these releases, allowing traders to anticipate market movements and make informed trading decisions. 
    For example, a surprise increase in interest rates by a central bank can lead to an appreciation of the currency, while lower-than-expected employment figures might cause a currency to depreciate. 
    Understanding the economic calendar helps traders manage risk and capitalize on market opportunities.
""")
st.markdown("---")

# Technical Analysis and Indicators
st.markdown("<h3 style='color: #2196F3;'>3. Technical Analysis and Indicators</h3>", unsafe_allow_html=True)
st.write("""
    **Topic: The Role of Technical Analysis and Indicators in Forex Trading**

    **Explanation:** 
    Technical analysis involves analyzing historical price data and trading volumes to forecast future price movements in the forex market. 
    Traders use various tools and indicators to identify trends, support and resistance levels, and potential entry and exit points. 
    Common indicators include Moving Averages, Relative Strength Index (RSI), and Bollinger Bands. 
    Technical analysis is based on the premise that historical price movements and patterns can provide insights into future price action. 
    While it does not consider fundamental factors, it helps traders make decisions based on price trends and patterns.
""")
st.markdown("---")

# Fundamental Analysis and News
st.markdown("<h3 style='color: #2196F3;'>4. Fundamental Analysis and News</h3>", unsafe_allow_html=True)
st.write("""
    **Topic: Fundamental Analysis and Its Impact on Forex Markets**

    **Explanation:** 
    Fundamental analysis in forex trading involves evaluating economic, political, and social factors that influence a currency’s value. 
    This includes analyzing economic indicators such as interest rates, inflation, and GDP growth, as well as news events like geopolitical tensions, trade policies, and central bank announcements. 
    By understanding these factors, traders can assess the overall health of an economy and predict how these factors might impact currency values. 
    For instance, strong economic data can lead to currency appreciation, while political instability might lead to depreciation. 
    Fundamental analysis helps traders understand the broader economic context behind currency movements.
""")
st.markdown("---")

# Economic Calendar Section
st.markdown("<h2 style='text-align: center; color: #4CAF50;'>Stay Informed with Real-Time Economic Events</h2>", unsafe_allow_html=True)
st.write("""
    An economic calendar is crucial for tracking significant financial events, such as government reports and policy decisions, that influence currency prices. 
    Monitoring these events enables traders to anticipate market movements and adapt their strategies accordingly. 
    Below, you'll find an economic calendar from Myfxbook, providing real-time updates on global economic events.
""")



st.components.v1.html("""
<!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <div class="tradingview-widget-copyright">
    <a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank">
      <span class="blue-text">Track all markets on TradingView</span>
    </a>
  </div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>
  {
    "colorTheme": "dark",
    "isTransparent": false,
    "width": "2020",
    "height": "800",
    "locale": "en",
    "importanceFilter": "-1,0,1",
    "countryFilter": "us,ca,eu,au,de,jp,ch,gb"
  }
  </script>
</div>
<!-- TradingView Widget END -->
""", height=600 , width=2020)

st.markdown("---")

# Forex Market Section for Major Currency Pairs
st.markdown("<h2 style='text-align: center; color: #4CAF50;'>Live Forex Market Data for Major Currency Pairs</h2>", unsafe_allow_html=True)
st.write("""
    Monitor real-time exchange rates for major currency pairs. This live feed helps you track market fluctuations and make informed trading decisions. 
    Below is a live market widget showcasing the latest prices for key currency pairs.
""")

# Embedding a TradingView widget for live Forex market data
st.components.v1.iframe(
    src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_0325b&symbol=FX:EURUSD&interval=1&theme=dark&style=1&timezone=Etc%2FUTC&withdateranges=1&hide_side_toolbar=1&allow_symbol_change=1&save_image=1&details=1&calendar=1&hotlist=1&studies=[]&study_legend=1&show_popup_button=1&popup_width=1000&popup_height=650&locale=en",
    width=2000,  # Adjust the width as needed
    height=800,  # Adjust the height as needed
    scrolling=True
)
st.markdown("---")
st.subheader('Real-Time Forex Heat Map')
st.components.v1.html("""
<!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Track all markets on TradingView</span></a></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-forex-heat-map.js" async>
  {
  "width": "2000",
  "height": 500,
  "currencies": [
    "EUR",
    "USD",
    "JPY",
    "GBP",
    "CHF",
    "AUD",
    "CAD"
  ],
  "isTransparent": false,
  "colorTheme": "dark",
  "locale": "en",
  "backgroundColor": "#1D222D"
}
  </script>
</div>
<!-- TradingView Widget END -->""" , height=500,width=2000)
st.markdown("---")
# Technical Analysis Section
st.markdown("<h2 style='text-align: center; color: #4CAF50;'>Harness the Power of Technical Analysis</h2>", unsafe_allow_html=True)
st.write("""
    Technical analysis involves examining historical price data and using statistical indicators to identify market trends and patterns. 
    Traders use tools such as moving averages, trend lines, and momentum indicators like RSI and MACD to make informed trading decisions. 
    By analyzing price charts and patterns, traders can predict future market movements and optimize their trading strategies.
""")

st.header("Real-Time Market Data for Major Currency Pairs")
st.write("""
    Access up-to-date market data for major currency pairs, including the latest prices, daily changes, and key metrics. 
    This section helps you stay informed and make strategic trading decisions based on real-time information.
""")


# Embed the TradingView Ticker Tape widget
st.components.v1.html("""
<!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <div class="tradingview-widget-copyright">
    <a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank">
      <span class="blue-text">Track all markets on TradingView</span>
    </a>
  </div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
  {
    "symbols": [
      {
        "description": "EUR/USD",
        "proName": "FX:EURUSD"
      },
      {
        "description": "Dollar Index USDX",
        "proName": "PEPPERSTONE:USDX"
      },
      {
        "description": "Euro Index EURX",
        "proName": "PEPPERSTONE:EURX"
      },
      {
        "description": "GOLD",
        "proName": "OANDA:XAUUSD"
      },
      {
        "description": "USD/CAD",
        "proName": "FX:USDCAD"
      },
      {
        "description": "USD/CHF",
        "proName": "FX:USDCHF"
      },
      {
        "description": "USD/JPY",
        "proName": "FX:USDJPY"
      },
      {
        "description": "GBP/USD",
        "proName": "FX:GBPUSD"
      },
      {
        "description": "AUD/USD",
        "proName": "OANDA:AUDUSD"
      }
    ],
    "showSymbolLogo": true,
    "isTransparent": false,
    "displayMode": "compact",
    "colorTheme": "dark",
    "locale": "en"
  }
  </script>
</div>
<!-- TradingView Widget END -->
""", height=100)


# Example placeholder for a technical analysis tool
st.write("**[Interactive Technical Analysis Chart Here]**")

# Fundamental Analysis Section
st.markdown("<h2 style='text-align: center; color: #4CAF50;'>Understand Market Movements with Fundamental Analysis</h2>", unsafe_allow_html=True)
st.write("""
    Fundamental analysis examines the underlying economic factors influencing currency prices, including economic indicators, central bank policies, and geopolitical events. 
    By evaluating these factors, traders can predict long-term currency trends and make informed trading decisions. 
    For instance, strong economic growth and rising interest rates in a country can lead to a stronger currency.
""")
# Example placeholder for fundamental analysis content
st.write("**[Market News and Reports Here]**")

# Closing Statement
st.write("""
    Our platform integrates technical and fundamental analysis to provide a comprehensive approach to Forex trading. 
    Whether you're focusing on short-term trades or long-term investments, the insights and tools available here will support your trading decisions and enhance your market strategy.
""")
