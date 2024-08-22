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


# Function to get model filename
def get_model_filename(currency):
    return f'models/{currency}.pkl'

# Function to get data file for currency events
def get_dataframe_filename(currency):
    return f'data/{currency.lower()}_event.csv'

# Function to get impact data file
def get_impact_filename():
    return 'data/impact.csv'

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
        # Load impact data
        impact_filename = get_impact_filename()
        try:
            impact = pd.read_csv(impact_filename)
            st.sidebar.dataframe(impact)
        except FileNotFoundError:
            st.error(f"Impact file '{impact_filename}' not found.")
            return
        except Exception as e:
            st.error(f"Error loading impact data: {e}")
            return

        # Sidebar for currency selection
        currency = st.sidebar.radio(
            "Select Currency",
            ['EUR', 'USD', 'GBP', 'CHF', 'NZD', 'CAD', 'AUD', 'JPY']
        )

        if currency:
            st.title(f'Model Prediction For {currency}')
            
            # Load the model for the selected currency
            model_filename = get_model_filename(currency)
            try:
                model = joblib.load(model_filename)
            except FileNotFoundError:
                st.error(f"Model file '{model_filename}' not found.")
                return
            except Exception as e:
                st.error(f"Error loading model: {e}")
                return
            
            # Load the DataFrame for the selected currency
            dataframe_filename = get_dataframe_filename(currency)
            try:
                df = pd.read_csv(dataframe_filename)
                st.dataframe(df)
            except FileNotFoundError:
                st.error(f"Data file '{dataframe_filename}' not found.")
                return
            except Exception as e:
                st.error(f"Error loading data: {e}")
                return

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
                try:
                    # Make predictions with the selected model
                    prediction = model.predict(data)
                    st.write(f'Prediction: {prediction[0]}')
                except Exception as e:
                    st.error(f"Error making prediction: {e}")

if __name__ == "__main__":
    main()

