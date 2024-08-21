import streamlit as st
import joblib
from sklearn.externals import joblib
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# Set the page configuration

st.set_page_config(
    page_title="Forex Market Analysis",
    page_icon="💹",
    layout="wide"
)

# Define the list of symbols and timeframes
symbols = ['USDX', 'EURX', 'XAUUSD', 'EURUSD', 'AUDUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'USDCAD']
timeframes = ['M30', 'H1', 'H4', 'D1']

def get_model_filename(symbol, timeframe):
    """Generate the model filename based on the symbol and timeframe."""
    return f'{symbol.lower()}_{timeframe.lower()}.pkl'

def get_dataframe_filename(symbol, timeframe):
    """Generate the dataframe filename based on the symbol and timeframe."""
    return f'forex_{symbol.lower()}_{timeframe.lower()}.csv'

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
            ##### **open:** Opening price of the forex pair for the time period.
            ##### **EMA_5:** 5-period exponential moving average.
            ##### **EMA_8:** 8-period exponential moving average.
            ##### **EMA_13:** 13-period exponential moving average.
            ##### **log_return:** Logarithmic return of the forex pair.
            ##### **lag1_close:** Closing price lagged by one period.
            ##### **lag2_close:** Closing price lagged by two periods.
            ##### **open_macd_diff:** Difference between open price and MACD line for period .
            ### Open-MACD Difference (`open_macd_diff`)
            ```python
            ['open_macd_diff'] = ['open'] -['MACD_Line']
            ```
            ### **Explanation**: Calculates the difference between the opening price and the MACD line. This feature helps to analyze how the opening price compares to the MACD indicator, which is used to identify trading signals.
            ##### **previous_open:** Opening price of the previous period.
            ##### **previous_open2:** Opening price lagged by two periods.
            ##### **previous_high:** Highest price of the previous period.
            ##### **previous_high2:** Highest price lagged by two periods.
            ##### **previous_low:** Lowest price of the previous period.
            ##### **previous_low2:** Lowest price lagged by two periods.
            ##### **previous_pip_value:** Pip value of the previous period.
            """, unsafe_allow_html=True
        )

    
    elif page == "Prediction":
        
        st.sidebar.title("Prediction")
        symbol = st.sidebar.radio('Select Symbol', symbols)
        timeframe = st.sidebar.radio('Select Timeframe', timeframes)
        st.title(f"Prediction For {symbol} On {timeframe}📈")
        # Load the model
        model_filename = get_model_filename(symbol, timeframe)
        model = joblib.load(model_filename)

        # Display the plot of the latest data
        df = load_currency_data(symbol, timeframe)
        fig = plot_forex_data(df, symbol, timeframe)
        st.plotly_chart(fig)

        # Prediction Inputs
        st.subheader('Enter Feature Values')
        open = st.number_input('Open', format="%.2f")
        EMA_5 = st.number_input('EMA_5', format="%.2f")
        EMA_8 = st.number_input('EMA_8', format="%.2f")
        EMA_13 = st.number_input('EMA_13', format="%.2f")
        lag1_close = st.number_input('Lag1_Close', format="%.2f")
        lag2_close = st.number_input('Lag2_Close', format="%.2f")
        previous_open = st.number_input('Previous_Open', format="%.2f")
        previous_high = st.number_input('Previous_High', format="%.2f")
        previous_low = st.number_input('Previous_Low', format="%.2f")
        previous_open2 = st.number_input('Previous_Open2', format="%.2f")
        previous_high2 = st.number_input('Previous_High2', format="%.2f")
        previous_low2 = st.number_input('Previous_Low2', format="%.2f")
        previous_pip_value = st.number_input('Previous_Pip_Value', format="%.2f")
        open_macd_diff = st.number_input('Open_MACD_Diff', format="%.2f")

        # Create a DataFrame with the input features
        data = pd.DataFrame({
            'open': [open],
            'EMA_5': [EMA_5],
            'EMA_8': [EMA_8],
            'EMA_13': [EMA_13],
            'lag1_close': [lag1_close],
            'lag2_close': [lag2_close],
            'previous_open': [previous_open],
            'previous_high': [previous_high],
            'previous_low': [previous_low],
            'previous_open2': [previous_open2],
            'previous_high2': [previous_high2],
            'previous_low2': [previous_low2],
            'previous_pip_value': [previous_pip_value],
            'open_macd_diff': [open_macd_diff]
        })

        # Button to make predictions
        if st.button('Predict'):
            # Make predictions with the selected model
            prediction = model.predict(data)
            st.write(f'Prediction: {prediction[0]}')

if __name__ == '__main__':
    main()
