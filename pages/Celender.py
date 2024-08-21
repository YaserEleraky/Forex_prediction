import streamlit as st
from sklearn.externals import joblib
import joblib
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Forex Market Analysis",
    page_icon="💹",
    layout="wide"
)

def get_model_filename(currency):
    return f'{currency.lower()}.pkl'

def get_dataframe_filename(currency):
    return f'{currency.lower()}_event.csv'

def load_currency_data(currency):
    filename = get_dataframe_filename(currency)
    return pd.read_csv(filename)

def main():
    # Create a sidebar with navigation options
    page = st.sidebar.radio("Navigation", ["About","Prediction"])
    if page == "About":
        # Title and image centered
        st.title("📈 Fundamental Analysis Economic Events 🌟")
        st.markdown("---")

        # Centered images
        st.markdown(
            """
            <div style="text-align: center;">
                <img src="https://c.mql5.com/i/og/mql5-calendar.png" alt="forex Logo" style="width: 100%; max-width: 1020px; height: auto; margin-bottom: 20px;">
            </div>
            """,
            unsafe_allow_html=True
        )

        # Add a horizontal line
        st.markdown("---")

        # Project description
        st.markdown(
            """
                # 📈 Starting Your Forex Market Project: Key Points to Consider 🌟
                   #####  The Forex market is the largest financial market globally, trading over $6 trillion daily.<br>
                   #####  This project aims to enhance forex trading strategies by leveraging economic calendar data.<br>
                   #####  By analyzing key economic events, such as GDP releases, employment reports, and central bank meetings,traders can better predict market movements.<br>
                   #####  The focus is on understanding how these events impact currency pairs, with a particular emphasis on comparing forecasted versus actual data.<br>
                   #####  The goal is to provide traders with actionable insights,helping them make informed and strategic decisions in the forex market.
            """,
            unsafe_allow_html=True
        )

        # Add a horizontal line
        st.markdown("---")

        # Key Components list
        st.markdown(
            """
            <div style="text-align: center;">
                <img src="https://www.smarttechid.com/wp-content/uploads/2014/11/DATACARD-LOGO.jpg" alt="NTSB Logo" style="width: 100%; max-width: 600px; height: auto; margin-bottom: 20px;">
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("""
    # Columns

    #### **Currency 💱**: Indicates the specific currency or currency pair that the event is expected to impact.
    #### **Event 📝**: Describes the type of economic event, such as a GDP release, employment report, interest rate decision, or central bank speech.
    #### **Impact ⚡**: Categorizes the expected impact of the event on the currency market (low, medium, high).
    #### **Previous 📉**: Shows the previous period's data for the same event.
    #### **Consensus 📊**: Represents the market’s forecast or expected outcome for the event.
    #### **Actual 📈**: The actual data or result released during the event.
    #### **Datetime 🕒**: Specifies the exact date and time when the event is scheduled to occur.
""")

        # Add another horizontal line
        st.markdown("---")


    elif page == "Prediction":

        impact = pd.read_csv("impact.csv")
        st.sidebar.subheader("Impact Data")
        st.sidebar.dataframe(impact)
        # Sidebar for currency selection
        currency = st.sidebar.radio(
            "Select Currency",
            ['EUR', 'USD', 'GBP', 'CHF', 'NZD', 'CAD', 'AUD', 'JPY']
        )

        st.title(f'Model Prediction For {currency}')
        # Load the model for the selected currency
        model_filename = get_model_filename(currency)
        model = joblib.load(model_filename)
        
        # Load the DataFrame for the selected currency
        df = load_currency_data(currency)

        # Display the selected currency and model filename
        st.sidebar.write(f"Selected Currency: {currency}")
        st.sidebar.write(f"Model File: {model_filename}")
        st.write("Encoder Data")
        st.dataframe(df)

        # Input fields for each feature
        previous = st.number_input('Previous', format="%.2f")
        consensus = st.number_input('Consensus', format="%.2f")
        consensus_lag = st.number_input('Consensus_Lag', format="%.2f")
        actual_lag = st.number_input('Actual_Lag', format="%.2f")
        previous_lag = st.number_input('Previous_Lag', format="%.2f")
        impact_encoder = st.number_input('Impact_encoder', format="%.2f")
        n_event_encoder = st.number_input('N_Event_encoder', format="%.2f")

        # Create a DataFrame with the input features
        data = pd.DataFrame({
            'Previous': [previous],
            'Consensus': [consensus],
            'Consensus_Lag': [consensus_lag],
            'Actual_Lag': [actual_lag],
            'Previous_Lag': [previous_lag],
            'Impact_encoder': [impact_encoder],
            'N_Event_encoder': [n_event_encoder]
        })

        # Button to make predictions
        if st.button('Predict'):
            # Make predictions with the selected model
            prediction = model.predict(data)
            st.write(f'Prediction: {prediction[0]}')



if __name__ == '__main__':
    main()
