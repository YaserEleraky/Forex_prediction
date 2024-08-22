import streamlit as st
import joblib
import pandas as pd
import spacy

# Set page configuration
st.set_page_config(
    page_title="Forex Market Analysis",
    page_icon="💹",
    layout="wide"
)


# Get the path for models directory
def get_model_path(currency):
    return os.path.join('models', f'{currency}.pkl')import os
import streamlit as st
import joblib
import pandas as pd

# Get the path for impact data
def get_impact_path():
    path = os.path.join('data', 'impact.csv')
    st.write(f"Debug: Impact path is {path}")  # Debug statement
    return path

# Get the path for models
def get_model_path(currency):
    path = os.path.join('models', f'{currency}.pkl')
    st.write(f"Debug: Model path for {currency} is {path}")  # Debug statement
    return path

# Get the path for data files
def get_data_path(currency):
    path = os.path.join('data', f'{currency.lower()}_event.csv')
    st.write(f"Debug: Data path for {currency} is {path}")  # Debug statement
    return path

def main():
    page = st.sidebar.radio("Navigation", ["About", "Prediction"])

    if page == "About":
        st.title("📈 Fundamental Analysis Economic Events 🌟")
        st.markdown("---")

        st.markdown(
            """
            <div style="text-align: center;">
                <img src="https://c.mql5.com/i/og/mql5-calendar.png" alt="forex Logo" style="width: 100%; max-width: 1020px; height: auto; margin-bottom: 20px;">
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        st.markdown(
            """
                # 📈 Starting Your Forex Market Project: Key Points to Consider 🌟
                   ##### The Forex market is the largest financial market globally, trading over $6 trillion daily.<br>
                   ##### This project aims to enhance forex trading strategies by leveraging economic calendar data.<br>
                   ##### By analyzing key economic events, such as GDP releases, employment reports, and central bank meetings, traders can better predict market movements.<br>
                   ##### The focus is on understanding how these events impact currency pairs, with a particular emphasis on comparing forecasted versus actual data.<br>
                   ##### The goal is to provide traders with actionable insights, helping them make informed and strategic decisions in the forex market.
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

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

        st.markdown("---")

    elif page == "Prediction":
        impact_path = get_impact_path()
        if os.path.exists(impact_path):
            impact = pd.read_csv(impact_path)
            st.sidebar.dataframe(impact)
        else:
            st.error(f"Impact file '{impact_path}' not found.")
            return

        currency = st.sidebar.radio(
            "Select Currency",
            ['EUR', 'USD', 'GBP', 'CHF', 'NZD', 'CAD', 'AUD', 'JPY']
        )

        if currency:
            st.title(f'Model Prediction For {currency}')
            
            model_path = get_model_path(currency)
            if os.path.exists(model_path):
                model = joblib.load(model_path)
            else:
                st.error(f"Model file '{model_path}' not found.")
                return

            dataframe_path = get_data_path(currency)
            if os.path.exists(dataframe_path):
                df = pd.read_csv(dataframe_path)
                st.dataframe(df)
            else:
                st.error(f"Data file '{dataframe_path}' not found.")
                return

            previous = st.number_input('Previous', format="%.2f")
            consensus = st.number_input('Consensus', format="%.2f")
            consensus_lag = st.number_input('Consensus_Lag', format="%.2f")
            actual_lag = st.number_input('Actual_Lag', format="%.2f")
            previous_lag = st.number_input('Previous_Lag', format="%.2f")
            impact_encoder = st.number_input('Impact_encoder', format="%.2f")
            n_event_encoder = st.number_input('N_Event_encoder', format="%.2f")

            data = pd.DataFrame({
                'Previous': [previous],
                'Consensus': [consensus],
                'Consensus_Lag': [consensus_lag],
                'Actual_Lag': [actual_lag],
                'Previous_Lag': [previous_lag],
                'Impact_encoder': [impact_encoder],
                'N_Event_encoder': [n_event_encoder]
            })

            if st.button('Predict'):
                try:
                    prediction = model.predict(data)
                    st.write(f'Prediction: {prediction[0]}')
                except Exception as e:
                    st.error(f"Error making prediction: {e}")

if __name__ == "__main__":
    main()


# Get the path for data files
def get_data_path(currency):
    return os.path.join('data', f'{currency.lower()}_event.csv')

def get_impact_path():
    return os.path.join('data', 'impact.csv')

def main():
    # Create a sidebar with navigation options
    page = st.sidebar.radio("Navigation", ["About", "Prediction"])

    if page == "About":
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

        st.markdown("---")

        # Project description
        st.markdown(
            """
                # 📈 Starting Your Forex Market Project: Key Points to Consider 🌟
                   ##### The Forex market is the largest financial market globally, trading over $6 trillion daily.<br>
                   ##### This project aims to enhance forex trading strategies by leveraging economic calendar data.<br>
                   ##### By analyzing key economic events, such as GDP releases, employment reports, and central bank meetings, traders can better predict market movements.<br>
                   ##### The focus is on understanding how these events impact currency pairs, with a particular emphasis on comparing forecasted versus actual data.<br>
                   ##### The goal is to provide traders with actionable insights, helping them make informed and strategic decisions in the forex market.
            """,
            unsafe_allow_html=True
        )

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

        st.markdown("---")

    elif page == "Prediction":
        impact_path = get_impact_path()
        if os.path.exists(impact_path):
            impact = pd.read_csv(impact_path)
            st.sidebar.dataframe(impact)
        else:
            st.error(f"Impact file '{impact_path}' not found.")
            return

    currency = st.sidebar.radio(
            "Select Currency",
            ['EUR', 'USD', 'GBP', 'CHF', 'NZD', 'CAD', 'AUD', 'JPY']
        )

    if currency:
        st.title(f'Model Prediction For {currency}')
            
        model_path = get_model_path(currency)
        if os.path.exists(model_path):
            model = joblib.load(model_path)
        else:
            st.error(f"Model file '{model_path}' not found.")
            return

        dataframe_path = get_data_path(currency)
        if os.path.exists(dataframe_path):
            df = pd.read_csv(dataframe_path)
            st.dataframe(df)
        else:
            st.error(f"Data file '{dataframe_path}' not found.")
            retur   
        previous = st.number_input('Previous', format="%.2f")
        consensus = st.number_input('Consensus', format="%.2f")
        consensus_lag = st.number_input('Consensus_Lag', format="%.2f")
        actual_lag = st.number_input('Actual_Lag', format="%.2f")
        previous_lag = st.number_input('Previous_Lag', format="%.2f")
        impact_encoder = st.number_input('Impact_encoder', format="%.2f")
        n_event_encoder = st.number_input('N_Event_encoder', format="%.2f")  
        data = pd.DataFrame({
            'Previous': [previous],
            'Consensus': [consensus],
            'Consensus_Lag': [consensus_lag],
            'Actual_Lag': [actual_lag],
            'Previous_Lag': [previous_lag],
            'Impact_encoder': [impact_encoder],
            'N_Event_encoder': [n_event_encoder]
        })

    if st.button('Predict'):
        try:
            prediction = model.predict(data)
            st.write(f'Prediction: {prediction[0]}')
        except Exception as e:
            st.error(f"Error making prediction: {e}")

if __name__ == "__main__":
    main()

