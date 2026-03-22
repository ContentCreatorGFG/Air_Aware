from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from prophet import Prophet
from datetime import datetime
from twilio.rest import Client

# CONFIG 
st.set_page_config(page_title="AirAware", layout="wide")

# Load environment variables from .env
load_dotenv()

# Twilio credentials (read from .env)
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")

# OpenWeather API key (read from .env)
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# TITLE
st.markdown("<h1 style='color:blue;font-size:50px;'>AirAware</h1>", unsafe_allow_html=True)
st.subheader("Smart Air Quality Monitoring")

# AQI CATEGORY
def get_category(a):
    if a <= 50: return "Good", "green"
    elif a <= 100: return "Moderate", "orange"
    elif a <= 150: return "Poor", "blue"
    elif a <= 200: return "Unhealthy", "red"
    elif a <= 300: return "Very Unhealthy", "purple"
    else: return "Hazardous", "maroon"

def send_sms_alert(phone_number, city, aqi, category):
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH)
        message = client.messages.create(
            body=f"⚠️ Air Quality Alert!\nCity: {city}\nAQI: {aqi} ({category})\nStay safe!",
            from_=TWILIO_PHONE,
            to=phone_number
        )
        return message.sid
    except Exception as e:
        st.error(f"SMS failed: {e}")
        return None

# NAViGATION
tab = st.sidebar.radio("Navigation", ["Dashboard","History","Prediction","Analysis","Health"])

#CITIES
cities = ["Delhi","Mumbai","Lucknow","Varanasi","Bengaluru","Kolkata","Chennai","Hyderabad","Jaipur","Ahmedabad","Surat","Patna","Indore","Nagpur","Pune"]
city = st.selectbox("Select City", ["Select City"] + cities)
phone = st.text_input("Enter Phone Number (+91XXXXXXXXXX)")

if city == "Select City":
    st.stop()

# API CALL
def fetch(city):
    geo = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city},IN&limit=1&appid={API_KEY}").json()
    lat, lon = geo[0]["lat"], geo[0]["lon"] if geo else (22,80)
    data = requests.get(f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}").json()
    return lat, lon, data["list"][0]

lat, lon, data = fetch(city)
aqi = data["main"]["aqi"] * 50
cat, color = get_category(aqi)
pollutants = data["components"]

# DASHBOARD
if tab == "Dashboard":
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"<div style='background:#222;padding:20px;border-radius:10px;text-align:center;color:white'><h3>City</h3><h2>{city}</h2></div>", unsafe_allow_html=True)
    col2.markdown(f"<div style='background:#222;padding:20px;border-radius:10px;text-align:center;color:{color}'><h3>AQI</h3><h2>{int(aqi)}</h2></div>", unsafe_allow_html=True)
    col3.markdown(f"<div style='background:#222;padding:20px;border-radius:10px;text-align:center;color:white'><h3>Category</h3><h2 style='color:{color}'>{cat}</h2></div>", unsafe_allow_html=True)

    st.write("Enter your phone number in E.164 format (e.g., +919876543210)")
    if st.button("Send SMS Alert"):
        if phone.startswith("+") and len(phone) >= 10:
            if aqi > 150:
                sid = send_sms_alert(phone, city, aqi, cat)
                if sid: st.success(f"🚨 SMS Alert Sent! (ID: {sid})")
            else:
                st.info("AQI is not high enough to trigger an alert.")
        else:
            st.error("Invalid phone number format. Use +91XXXXXXXXXX")

    # AQI Scale
    st.subheader("AQI Scale")
    labels = [
        ("Good (0-50)", "green"),
        ("Moderate (51-100)", "orange"),
        ("Poor (101-150)", "blue"),
        ("Unhealthy (151-200)", "red"),
        ("Very Unhealthy (201-300)", "purple"),
        ("Hazardous (301+)", "maroon")
    ]
    cols = st.columns(6)
    for i,(text,c) in enumerate(labels):
        cols[i].markdown(f"<div style='background:{c};padding:12px;border-radius:10px;color:white;text-align:center'>{text}</div>", unsafe_allow_html=True)

# HISTORY
if tab == "History":
    if "hist" not in st.session_state: st.session_state.hist = []
    st.session_state.hist.append({"Time": datetime.now(), "AQI": aqi})
    df = pd.DataFrame(st.session_state.hist)

    st.subheader("7-Day Weekly Trend (LIVE)")
    fig1 = px.line(df.tail(7), x="Time", y="AQI", markers=True, title="AQI vs Time (Weekly)")
    st.plotly_chart(fig1)

    st.subheader("30-Day Monthly Trend (LIVE)")
    fig2 = px.line(df.tail(30), x="Time", y="AQI", markers=True, title="AQI vs Time (Monthly)")
    st.plotly_chart(fig2)

# PREDICTION
if tab == "Prediction":
    df = pd.DataFrame({"ds": pd.date_range(end=datetime.today(), periods=30),
                       "y": [aqi+i for i in range(30)]})
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=7)
    fc = model.predict(future)
    fc.rename(columns={"ds":"Date","yhat":"Predicted AQI"}, inplace=True)

    st.subheader("7-Day Prophet Forecast")
    fig3 = px.bar(fc.tail(7), x="Date", y="Predicted AQI", color="Predicted AQI", title="Predicted AQI vs Date")
    st.plotly_chart(fig3)
    fc["Category"] = fc["Predicted AQI"].apply(lambda x: get_category(x)[0])
    st.write(fc.tail(7)[["Date","Predicted AQI","Category"]])

# ANALYSIS
if tab == "Analysis":
    st.subheader("Pollutant Levels")
    df_poll = pd.DataFrame(pollutants.items(), columns=["Pollutant","µg/m³"])
    fig4 = px.bar(df_poll, x="Pollutant", y="µg/m³", color="µg/m³", title="Pollutant Concentrations")
    st.plotly_chart(fig4)
    st.subheader("Pollutant Distribution")
    fig5 = px.pie(df_poll, names="Pollutant", values="µg/m³", hole=0.4)
    st.plotly_chart(fig5)

# HEALTH
if tab == "Health":
    if aqi <= 100:
        st.success("🌿 Safe for outdoor | 🏃 Exercise allowed | 🪟 Ventilate home")
    elif aqi <= 200:
        st.warning("⚠️ Limit outdoor | 😷 Wear mask | 🏠 Close windows")
    else:
        st.error("🚫 Avoid outdoor | 😷 N95 mask | 🏠 Stay indoors")







































































































































































































































































































































































































































































































































































































































































