import streamlit as st
import joblib
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
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        st.error(f"Data file {filename} not found. Please ensure the file is available.")
        return pd.DataFrame()  # Return an empty DataFrame

def plot_forex_data(df, symbol, timeframe):
    """Plot the Forex data with indicators for the selected symbol and timeframe."""
    if df.empty:
        return go.Figure()  # Return an empty figure if DataFrame is empty

    sample = df.tail(500).copy()

    # Calculate Fibonacci retracement levels
    high_price = sample['high'].max()
    low_price = sample['low'].min()
    diff = high_price - low_price
    fibonacci_levels = {
        'Fibonacci_0.236': high_price - 0.236 * diff,
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
            Forex trading offers substantial opportunities but also comes with significant risks due to market volatility.
            </div>
            """, 
            unsafe_allow_html=True)
    
        # Divider for better separation
        st.markdown("---")
    
        # Displaying the second image centered and larger
        st.markdown(
            """
            <div style="text-align: center;">
                <img src="https://goldenlifenewspaper.com/wp-content/uploads/2024/06/indicator-1.jpg" alt="Image 1" width="1200">
            </div>
            """, 
            unsafe_allow_html=True)
    
        # Section with description centered
        st.markdown(
            """
            <div style='text-align: center; font-size: 22px;'>
            Technical analysis in Forex involves using past price data to predict future movements.
            Traders use indicators like moving averages, RSI, MACD, and Fibonacci retracements to make informed decisions.
            However, it's crucial to combine technical analysis with other factors and maintain a disciplined approach to risk management.
            </div>
            """, 
            unsafe_allow_html=True)
    
        # Divider for better separation
        st.markdown("---")
    
        # Displaying the third image centered and larger
        st.markdown(
            """
            <div style="text-align: center;">
                <img src="https://goldenlifenewspaper.com/wp-content/uploads/2024/06/indicator-2.jpg" alt="Image 1" width="1200">
            </div>
            """, 
            unsafe_allow_html=True)
    
        # Section with description centered
        st.markdown(
            """
            <div style='text-align: center; font-size: 22px;'>
            Understanding and mastering technical analysis tools is essential for traders to navigate the complex Forex market effectively.
            Combining various indicators can provide a comprehensive view, enhancing the potential for successful trades.
            </div>
            """, 
            unsafe_allow_html=True)
    
    elif page == "Prediction":
        # Page title
        st.title("Forex Market Analysis and Prediction")

        # Divider for better separation
        st.markdown("---")

        # User selection for symbol and timeframe
        symbol = st.selectbox("Select a currency pair:", symbols)
        timeframe = st.selectbox("Select a timeframe:", timeframes)

        # Load the selected model
        model_filename = get_model_filename(symbol, timeframe)
        try:
            model = joblib.load(model_filename)
        except (FileNotFoundError, AttributeError) as e:
            st.error(f"Model could not be loaded: {e}")
            return

        # Load and display the Forex data
        df = load_currency_data(symbol, timeframe)
        if df.empty:
            return  # Do not proceed if data is not available

        st.subheader(f"Forex Data for {symbol} ({timeframe})")
        st.dataframe(df.tail(10))

        # Plot the data with technical indicators
        fig = plot_forex_data(df, symbol, timeframe)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
