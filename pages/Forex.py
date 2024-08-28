import streamlit as st
import numpy as np
import joblib
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# Set the page configuration
import warnings
from sklearn.exceptions import InconsistentVersionWarning
from PIL import Image

warnings.filterwarnings(action='ignore', category=InconsistentVersionWarning)

st.set_page_config(
    page_title="Forex Market Analysis",
    page_icon="💹",
    layout="wide"
)

# Define the list of symbols and timeframes
symbols = ['USDX', 'EURX', 'XAUUSD', 'EURUSD', 'AUDUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'USDCAD']
timeframes = ['M30', 'H1', 'H4', 'D1']
pip_sizes = {
            'USDX': 0.0001,
            'EURX': 0.0001,
            'XAUUSD': 0.0001,
            'EURUSD': 0.0001,
            'AUDUSD': 0.0001,
            'GBPUSD': 0.0001,
            'USDJPY': 0.01,    # Specific pip size for USDJPY
            'USDCHF': 0.0001,
            'USDCAD': 0.0001
        }
        # Function to calculate pip value based on a single input value
def calculate_pip_value(exchange_rate, pip_size, trade_size):
    """Calculate the pip value based on a single exchange rate."""
    if exchange_rate == 0:
        st.error("Error: Exchange rate cannot be zero.")
        return None
    return (pip_size / exchange_rate) * trade_size
def make_prediction(model, features, input_values):
    """Make predictions using the provided model."""
    # Convert input values to a DataFrame
    data = pd.DataFrame([input_values], columns=features)
    
    # Preprocess the features (ensure they are numeric)
    data_preprocessed = preprocess_features(data, features)
    
    # Make the prediction
    prediction = model.predict(data_preprocessed)
    
    return prediction

def preprocess_features(data, features):
    """Preprocess features to ensure they are all numeric."""
    for col in features:
        if np.issubdtype(data[col].dtype, np.datetime64):
            data[col] = data[col].astype(np.int64)  # Convert datetime to int (Unix timestamp)
    
    numeric_features = [col for col in features if np.issubdtype(data[col].dtype, np.number)]
    
    # Ensure all required features are present
    missing_features = set(features) - set(numeric_features)
    if missing_features:
        raise ValueError(f"Missing features for preprocessing: {missing_features}")
    
    return data[numeric_features]
def get_model_filename(symbol, timeframe):
    """Generate the model filename based on the symbol and timeframe."""
    return f'{symbol}_{timeframe}.pkl'

def get_dataframe_filename(symbol, timeframe):
    """Generate the dataframe filename based on the symbol and timeframe."""
    return f'forex_{symbol}_{timeframe}.csv'

def load_currency_data(symbol, timeframe):
    """Load the CSV file for the selected symbol and timeframe."""
    filename = get_dataframe_filename(symbol, timeframe)
    return pd.read_csv(filename)

def plot_forex_data(df, symbol, timeframe):
    """Plot the Forex data with indicators for the selected symbol and timeframe."""
    sample = df.tail(500).copy()
    
    # Calculate Fibonacci retracement levels
    high_price = sample['high'].max()
    low_price = sample['low'].min()
    diff = high_price - low_price
    fibonacci_levels = {
        'Fibonacci_0.236': high_price,
        'Fibonacci_0.382': high_price - 0.382 * diff,
        'Fibonacci_0.618': high_price - 0.618 * diff,
        'Fibonacci_0.786': high_price - 0.786 * diff,
        'Fibonacci_0.886': high_price - 0.886 * diff,
        'Fibonacci_1.146': low_price
    }
    for level, value in fibonacci_levels.items():
        sample[level] = value

    # Create the figure with subplots
    fig = make_subplots(
        rows=6, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.4, 0.15, 0.15, 0.15, 0.15, 0.1],
        subplot_titles=(
            'Candlestick Chart with Moving Averages and EMAs',
            'MACD',
            'RSI',
            'ATR',
            'Volume',
            ''  # Empty subplot for spacing
        ),
        specs=[
            [{}],  # Candlestick chart
            [{}],  # MACD
            [{}],  # RSI
            [{}],  # ATR
            [{}],  # Volume
            [{'type': 'domain'}]  # Empty domain to adjust spacing
        ]
    )

    # Add Candlestick chart with Moving Averages and EMAs to the first subplot
    fig.add_trace(go.Candlestick(
        x=sample.index,
        open=sample['open'],
        high=sample['high'],
        low=sample['low'],
        close=sample['close'],
        name='Candlestick',
        increasing=dict(line=dict(color='green'), fillcolor='rgba(0, 255, 0, 0.3)'),
        decreasing=dict(line=dict(color='red'), fillcolor='rgba(255, 0, 0, 0.3)')
    ), row=1, col=1)

    # Add Moving Averages and EMAs
    ma_colors = {
        'MA_5': 'blue',
        'MA_20': 'orange',
        'MA_50': 'green',
        'MA_200': 'purple',
        'MA_400': 'grey'
    }
    ema_colors = {
        'EMA_5': 'cyan',
        'EMA_8': 'magenta',
        'EMA_13': 'red'
    }

    for ma, color in ma_colors.items():
        if ma in sample.columns:
            fig.add_trace(go.Scatter(
                x=sample.index,
                y=sample[ma],
                mode='lines',
                name=ma,
                line=dict(color=color, width=2)
            ), row=1, col=1)

    for ema, color in ema_colors.items():
        if ema in sample.columns:
            fig.add_trace(go.Scatter(
                x=sample.index,
                y=sample[ema],
                mode='lines',
                name=ema,
                line=dict(color=color, width=2, dash='dash')
            ), row=1, col=1)

    # Add Fibonacci Retracements
    fibonacci_colors = {
        'Fibonacci_0.236': 'gold',
        'Fibonacci_0.382': 'silver',
        'Fibonacci_0.618': 'red',
        'Fibonacci_0.786': 'blue',
        'Fibonacci_0.886': 'orange',
        'Fibonacci_1.146': 'grey'
    }

    for level, color in fibonacci_colors.items():
        fig.add_trace(go.Scatter(
            x=sample.index,
            y=sample[level],
            mode='lines',
            name=level,
            line=dict(color=color, dash='dash' if '0.' in level else 'solid', width=1.5)
        ), row=1, col=1)

    # Add MACD
    if 'MACD_Line' in sample.columns and 'MACD_Signal' in sample.columns:
        fig.add_trace(go.Scatter(
            x=sample.index,
            y=sample['MACD_Line'],
            mode='lines',
            name='MACD Line',
            line=dict(color='green', width=2)
        ), row=2, col=1)

        fig.add_trace(go.Scatter(
            x=sample.index,
            y=sample['MACD_Signal'],
            mode='lines',
            name='MACD Signal',
            line=dict(color='red', width=2)
        ), row=2, col=1)

    # Add RSI
    if 'RSI' in sample.columns:
        fig.add_trace(go.Scatter(
            x=sample.index,
            y=sample['RSI'],
            mode='lines',
            name='RSI',
            line=dict(color='blue', width=2)
        ), row=3, col=1)

    # Add ATR
    if 'ATR' in sample.columns:
        fig.add_trace(go.Scatter(
            x=sample.index,
            y=sample['ATR'],
            mode='lines',
            name='ATR',
            line=dict(color='purple', width=2)
        ), row=4, col=1)

    # Add Volume
    if 'volume' in sample.columns:
        fig.add_trace(go.Bar(
            x=sample.index,
            y=sample['volume'],
            name='Volume',
            marker_color='lightgrey',
            opacity=0.6
        ), row=5, col=1)

    # Update layout with dark theme and better formatting
    fig.update_layout(
        title=f'Comprehensive Indicator Analysis for {symbol} ({timeframe})',
        xaxis_title='Time',
        xaxis_rangeslider_visible=False,
        height=2000,  # Height in pixels
        width=3000,  # Width in pixels
        template='plotly_dark',
    )

    return fig

def main():
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["About", "Prediction"])

    if page == "About":

        st.title("📈 Technical Analysis And Indicators 🌟")
    
        # Divider for better separation
        st.markdown("---")

        # Displaying the first image centered and larger
        st.markdown(
                """
                <div style="text-align: center;">
                    <img src="https://goldenlifenewspaper.com/wp-content/uploads/2024/06/robots-2.jpg" alt="NTSB Logo" width="1020">
                </div>
                """,
                unsafe_allow_html=True)
        # Section with description centered
        st.markdown(
            """
            <div style='text-align: center; font-size: 22px;'>
            The Forex market is the largest financial market globally, trading over $6 trillion daily. 
            It involves buying and selling currencies to profit from exchange rate movements.
            </div>
            """, unsafe_allow_html=True
        )

        # Divider for better separation
        st.markdown("---")

        # Key Points List with centered header
        st.markdown("<h2 style='text-align: center;'>Key Points to Consider</h2>", unsafe_allow_html=True)
        st.markdown(
            """
            ##### **Introduction to Forex Market 🌍:** The Forex market is the largest financial market globally, trading over $6 trillion daily. It involves buying and selling currencies to profit from exchange rate movements.
            ##### **Understanding Pip Values 💰:** A pip is the smallest price change in a currency pair. Calculating pip values helps in assessing the impact of price movements on trading outcomes.
            ##### **Objective of the Project 🎯:** The project aims to analyze forex market data, compute pip values, and derive actionable insights to enhance trading strategies.
            ##### **Data Collection and Preparation 📊:** Collect data from reliable sources, clean and prepare it for analysis to ensure quality results.
            ##### **Methodology 🔍:** Use statistical methods and machine learning algorithms for data analysis. Calculate pip values using the formula: `Pip_Value = (pip_size / exchange_rate) * trade_size`.
            ##### **Visualizations and Insights 📉:** Create charts and graphs to visualize pip values, market trends, and trading signals. Interpret data to make informed trading decisions.
            ##### **Implications for Trading Strategies 🚀:** Refine trading strategies based on pip value calculations and data insights. Explore advanced techniques for deeper market analysis.
            ##### **Next Steps 🗺️:** Apply the findings to real-world trading scenarios and continuously improve the analysis and methodology for better results.
            """, unsafe_allow_html=True
        )

        # Divider for better separation
        st.markdown("---")

        # Displaying the second image centered and larger
        st.markdown(
                """
                <div style="text-align: center;">
                    <img src="https://www.smarttechid.com/wp-content/uploads/2014/11/DATACARD-LOGO.jpg" alt="NTSB Logo" width="600">
                </div>
                """,
                unsafe_allow_html=True
)

        # Alert Box with information and list of columns for prediction centered
        st.markdown(
            """
            <div style='text-align: center; font-size: 50px;'>
            <strong>Forex Market</strong>

            ### This project focuses on enhancing forex trading strategies through advanced analysis techniques. It involves calculating the pip value to determine the financial impact of price movements and analyzing extensive forex market data to uncover actionable insights. The goal is to support traders with precise calculations and detailed data, facilitating more informed and strategic decision-making in the forex market.
            ### Columns For Prediction
            </div>
           
            """, unsafe_allow_html=True
        )
        
        # List of columns for prediction with increased font size
        st.markdown(
    """
    ## Feature Descriptions
    
    ### Input Fields for Feature Values
    
    **Open**: Opening price of the forex pair for the time period. This is the price at which the forex pair started trading in the selected period.
    
    **Previous_Open**: Opening price of the previous period. This helps in comparing the current opening price with that of the previous period.
    
    **Previous_High**: Highest price of the previous period. This indicates the peak price reached in the previous period.
    
    **Previous_Low**: Lowest price of the previous period. This shows the lowest price reached in the previous period.
    
    **Lag1_Close**: Closing price from 1 period ago. This provides the closing price from the immediately preceding period.
    
    **Previous_Open2**: Opening price from 2 periods ago. This helps in analyzing the trend over a slightly longer time frame.
    
    **Previous_High2**: Highest price from 2 periods ago. This is useful for comparing historical high prices.
    
    **Previous_Low2**: Lowest price from 2 periods ago. This is useful for comparing historical low prices.
    
    **Lag2_Close**: Closing price from 2 periods ago. This gives a view of how the closing price has evolved over the past two periods.

    ### Input Fields for Indicators
    
    **EMA_5**: 5-period exponential moving average. This smooths out price data over the past 5 periods to identify the trend direction.
    
    **EMA_8**: 8-period exponential moving average. This smooths out price data over the past 8 periods for a slightly longer trend analysis.
    
    **EMA_13**: 13-period exponential moving average. This helps in understanding the trend over a more extended period.
    
    **MACD_Signal**: MACD Signal Line value. This is used to identify the trend and potential buy/sell signals.
    
    **MACD_Line**: MACD Line value. This helps in determining the relationship between short-term and long-term price trends.
    
    **Prev_EMA_5**: 5-period EMA from the previous period. Useful for comparing the current EMA with the previous period's value.
    
    **Prev_EMA_8**: 8-period EMA from the previous period. Useful for trend comparison with the previous period.
    
    **Prev_EMA_13**: 13-period EMA from the previous period. Provides context for longer-term trend analysis.
    
    **Prev_MACD_Signal**: MACD Signal Line value from the previous period. Helps in evaluating changes in trend signals.
    
    **Prev_MACD_Line**: MACD Line value from the previous period. Useful for assessing the trend's momentum.

    """, unsafe_allow_html=True
)

    
    elif page == "Prediction":
        def preprocess_features(data, features):
            """Preprocess features to ensure they are all numeric and consistent."""
            for col in features:
                if np.issubdtype(data[col].dtype, np.datetime64):
                    data[col] = data[col].astype(np.int64)  # Convert datetime to int (Unix timestamp)

            numeric_features = [col for col in features if np.issubdtype(data[col].dtype, np.number)]
            return data[numeric_features]

        def make_prediction(model, features, input_values):
            """Make predictions using the provided model."""
            # Convert input values to a DataFrame
            data = pd.DataFrame([input_values], columns=features)

            # Preprocess the features (ensure they are numeric)
            data_preprocessed = preprocess_features(data, features)

            # Ensure the data is passed without feature names if necessary
            data_preprocessed = data_preprocessed.values  # Convert to NumPy array

            # Make the prediction
            prediction = model.predict(data_preprocessed)

            return prediction

         # Sidebar for symbol and timeframe selection
        st.sidebar.title("Prediction")

        # Select Symbol and Timeframe
        symbol = st.sidebar.radio('Select Symbol', symbols)
        timeframe = st.sidebar.radio('Select Timeframe', timeframes)

        # Display the title with selected symbol and timeframe
        st.title(f"Prediction For {symbol} On {timeframe}📈")

        # Automatically update and display the pip size for the selected symbol
        pip_size = pip_sizes[symbol]
        st.write(f"Selected symbol: **{symbol}** | Pip size: **{pip_size}**")

        # Load the model
        model_filename = get_model_filename(symbol, timeframe)
        model = joblib.load(model_filename)

        # Load and plot the latest data for the selected symbol
        df = load_currency_data(symbol, timeframe)
        fig = plot_forex_data(df, symbol, timeframe)
        st.plotly_chart(fig)

        # Prediction Inputs
        st.subheader('Enter Feature Values')

        # Creating two columns for input fields
        col1, col2 = st.columns(2)

        # Input fields in the first column
        with col1:
            open_price = st.number_input('Enter the opening price (Open)', format="%.5f")
            EMA_5 = st.number_input('Enter the 5-period Exponential Moving Average (EMA_5)', format="%.5f")
            EMA_8 = st.number_input('Enter the 8-period Exponential Moving Average (EMA_8)', format="%.5f")
            EMA_13 = st.number_input('Enter the 13-period Exponential Moving Average (EMA_13)', format="%.5f")
            MACD_Signal = st.number_input('Enter the MACD Signal Line value (MACD_Signal)', format="%.8f")
            MACD_Line = st.number_input('Enter the MACD Line value (MACD_Line)', format="%.8f")
            previous_open2 = st.number_input('Enter the opening price from 2 periods ago (Previous_Open2)', format="%.5f")
            previous_high2 = st.number_input('Enter the highest price from 2 periods ago (Previous_High2)', format="%.5f")
            previous_low2 = st.number_input('Enter the lowest price from 2 periods ago (Previous_Low2)', format="%.5f")
            lag2_close = st.number_input('Enter the closing price from 2 periods ago (Lag2_Close)', format="%.5f")

        # Input fields in the second column
        with col2:
            previous_open = st.number_input('Enter the previous period\'s opening price (Previous_Open)', format="%.5f")
            previous_high = st.number_input('Enter the previous period\'s highest price (Previous_High)', format="%.5f")
            previous_low = st.number_input('Enter the previous period\'s lowest price (Previous_Low)', format="%.5f")
            lag1_close = st.number_input('Enter the closing price from 1 period ago (Lag1_Close)', format="%.5f")
            prev_EMA_5 = st.number_input('Enter the 5-period Exponential Moving Average from the previous period (Prev_EMA_5)', format="%.5f")
            prev_EMA_8 = st.number_input('Enter the 8-period Exponential Moving Average from the previous period (Prev_EMA_8)', format="%.5f")
            prev_EMA_13 = st.number_input('Enter the 13-period Exponential Moving Average from the previous period (Prev_EMA_13)', format="%.5f")
            prev_MACD_Signal = st.number_input('Enter the MACD Signal Line value from the previous period (Prev_MACD_Signal)', format="%.8f")
            prev_MACD_Line = st.number_input('Enter the MACD Line value from the previous period (Prev_MACD_Line)', format="%.8f")
            previous_pip_value = st.number_input('Enter the Pip Value from the previous period (Previous_Pip_Value)', format="%.8f")
        # Calculate the MACD differences
        open_macd_diff = open_price - MACD_Line
        prev_open_macd_diff = previous_open - prev_MACD_Line
        
        # Calculate `previous_pip_value` dynamically
        trade_size = 100000  # 1 standard lot
        previous_pip_value = calculate_pip_value(lag1_close, pip_size, trade_size)

        # Only proceed if the pip value was successfully calculated (not None)
        if previous_pip_value is not None:
            # Display the calculated `previous_pip_value`
            st.markdown(f"## Calculated Previous Pip Value: {previous_pip_value:.10f}")
            st.markdown(f"## Open MACD Difference: {open_macd_diff:.8f}")
            st.markdown(f"## Previous Open MACD Difference: {prev_open_macd_diff:.8f}")
            # Button to make predictions
        if st.button('Predict'):
            # Define the features for preprocessing
            feature_names = [
                'open_price', 'EMA_5', 'EMA_8', 'EMA_13', 'MACD_Signal', 'lag1_close', 'lag2_close',
                'previous_open', 'previous_high', 'previous_low', 'previous_open2', 'previous_high2',
                'previous_low2', 'previous_pip_value', 'open_macd_diff', 'prev_EMA_5', 'prev_EMA_8',
                'prev_EMA_13', 'prev_open_macd_diff', 'prev_MACD_Signal'
            ]
            
            # Collect input values
            input_values = {
                'open_price': open_price, 'EMA_5': EMA_5, 'EMA_8': EMA_8, 'EMA_13': EMA_13,
                'MACD_Signal': MACD_Signal, 'lag1_close': lag1_close,
                'lag2_close': lag2_close, 'previous_open': previous_open, 'previous_high': previous_high,
                'previous_low': previous_low, 'previous_open2': previous_open2, 'previous_high2': previous_high2,
                'previous_low2': previous_low2, 'previous_pip_value': previous_pip_value, 'open_macd_diff': open_macd_diff,
                'prev_EMA_5': prev_EMA_5, 'prev_EMA_8': prev_EMA_8, 'prev_EMA_13': prev_EMA_13,
                'prev_open_macd_diff': prev_open_macd_diff, 'prev_MACD_Signal': prev_MACD_Signal,
            }

            # Ensure that the number of input values matches the expected number of features
            if len(input_values) != len(feature_names):
                st.error(f"Mismatch between input values and feature names: {len(input_values)} vs {len(feature_names)}")
                return
            # Convert the dictionary to a DataFrame
            df = pd.DataFrame(list(input_values.items()), columns=['Feature', 'Value'])

            # Split the DataFrame into two parts horizontally
            half = len(df) // 2
            df_part1 = df.iloc[:half].reset_index(drop=True)
            df_part2 = df.iloc[half:].reset_index(drop=True)

            # Create a new DataFrame by combining the two parts horizontally
            df_combined = pd.concat([df_part1, df_part2], axis=1)

            # Rename the columns to distinguish between the two halves
            df_combined.columns = ['Feature 1', 'Value 1', 'Feature 2', 'Value 2']

            # Display the combined DataFrame
            st.dataframe(df_combined)

            # Make prediction using the make_prediction function
            try:
                prediction = make_prediction(model, feature_names, input_values)
                adjustment = 0.0265
                adjusted_prediction = prediction[0] + adjustment

                # Display the prediction value
                st.markdown(f""" # Original Prediction :  {prediction[0]:.10f}\n""")

                buy_icon = Image.open("buy-button.png")
                sell_icon = Image.open("selling.png")

                if adjusted_prediction > open_price:
                    st.image(buy_icon, width=215)
                    st.markdown(""" # Signal: **BUY** """)
                elif adjusted_prediction < open_price:
                    st.markdown(""" # Signal: **SELL** """)
                    st.image(sell_icon, width=215)
                else:
                    st.write("Signal: **HOLD**")
            except Exception as e:
                st.error(f"Error during prediction: {e}")

if __name__ == '__main__':
    main()