import streamlit as st
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY)

# Set page configuration
st.set_page_config(
    page_title="Smart Converter",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 18px;
            color: #444;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #000;
        }
        .footer {
            position: fixed;
            bottom: 10px;
            right: 15px;
            color: gray;
            font-size: 14px;
        }
    </style>
""", unsafe_allow_html=True)

# Application title
st.sidebar.markdown("## 🔄 Smart Converter")
st.sidebar.markdown("Built with Gemini AI")

# API functions
def get_gemini_response(prompt):
    if not GEMINI_API_KEY:
        st.sidebar.warning("⚠️ Gemini API key not set. Using fallback mode.")

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text


def get_currency_rates():
    CURRENCY_API_URL = "https://open.er-api.com/v6/latest/USD"
    response = requests.get(CURRENCY_API_URL)
    data = response.json()
    rates = data["rates"]
    rates["timestamp"] = data["time_last_update_utc"]
    return rates


def create_ai_prompt(text):
    return f"""
    You are a Smart Unit Converter. Your job is to convert units and currencies accurately. 
    - Always return the converted value and its unit. 
    - Format the response as: [value] [unit] (Example: '5 meters' or '10.5 USD').
    - Do not introduce yourself or explain how you work. Focus only on conversion. 
    - If the user says "hi", respond with "Hello! I am a Smart Unit Converter. How can I assist you?"  
    - For all other inputs, return only the converted value and unit.  
    - If conversion is not possible, say "Invalid input. Please enter a valid unit or currency."  
    Convert: {text}
    """


# Sidebar selection
st.sidebar.subheader("Choose Converter")
converter_type = st.sidebar.radio(
    "Converter Type", ["Unit Converter", "Currency Converter"]
)

# Title
st.title("🔄 Smart Converter")

# Tabs
tab1, tab2 = st.tabs(["💬 Chat Interface", "📊 Selection Interface"])

# ----------- Tab 1: Chat Interface -----------
with tab1:
    st.subheader("Natural Language Conversion")
    st.info("Type things like:\n- 'Convert 10 USD to INR'\n- '5 meters in feet'")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask your conversion..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Converting..."):
                ai_prompt = create_ai_prompt(prompt)
                response = get_gemini_response(ai_prompt)
                st.markdown(f"✅ {response}")
                st.session_state.messages.append({"role": "assistant", "content": response})

# ----------- Tab 2: Selection Interface -----------
with tab2:
    st.subheader("Manual Selection Conversion")

    if converter_type == "Unit Converter":
        category = st.selectbox(
            "Measurement Category",
            ["Length", "Weight", "Volume", "Temperature", "Area", "Time", "Data", "Speed"]
        )

        units = {
            "Length": ["Meter", "Kilometer", "Centimeter", "Millimeter", "Inch", "Foot", "Yard", "Mile"],
            "Weight": ["Gram", "Kilogram", "Milligram", "Pound", "Ounce", "Ton"],
            "Volume": ["Liter", "Milliliter", "Cubic Meter", "Gallon", "Quart", "Pint", "Cup"],
            "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
            "Area": ["Square Meter", "Square Kilometer", "Square Centimeter", "Square Inch", "Square Foot", "Acre", "Hectare"],
            "Time": ["Second", "Millisecond", "Minute", "Hour", "Day", "Week", "Month", "Year"],
            "Data": ["Byte", "Kilobyte", "Megabyte", "Gigabyte", "Terabyte", "Bit"],
            "Speed": ["Meter per Second", "Kilometer per Hour", "Mile per Hour", "Knot"]
        }

        col1, col2 = st.columns(2)
        with col1:
            from_unit = st.selectbox("From", units[category])
            value = st.number_input("Value", value=1.0, step=0.1)

        with col2:
            to_unit = st.selectbox("To", units[category])

        if st.button("Convert Units"):
            with st.spinner("Processing..."):
                prompt = f"Convert {value} {from_unit} to {to_unit}"
                result = get_gemini_response(create_ai_prompt(prompt))
                st.success(result)

    else:
        with st.spinner("Fetching currency rates..."):
            rates = get_currency_rates()
            currencies = [k for k in rates.keys() if k != "timestamp"]
            last_updated = rates["timestamp"]

        st.caption(f"💱 Exchange rates updated: {last_updated}")

        col1, col2 = st.columns(2)
        with col1:
            from_currency = st.selectbox("From Currency", currencies)
            amount = st.number_input("Amount", value=1.0, step=0.1)

        with col2:
            to_currency = st.selectbox("To Currency", currencies)

        if st.button("Convert Currency"):
            prompt = f"Convert {amount} {from_currency} to {to_currency}"
            result = get_gemini_response(create_ai_prompt(prompt))
            st.success(result)

# ----------- Footer -----------
st.markdown(
    "<div class='footer'>👨‍💻 Created by <b>Ubaid Raza</b></div>",
    unsafe_allow_html=True
)
