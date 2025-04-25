import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime
from datetime import timedelta

# Page configuration
st.set_page_config(page_title="Weather Dashboard", layout="wide")
st.title("Weather Dashboard")

# Sidebar for inputs
st.sidebar.header("Settings")
location = st.sidebar.text_input("Enter City", "New York")
today = datetime.datetime.now().date()
date_range = st.sidebar.date_input("Date Range", [today, today + timedelta(days=5)])
temp_unit = st.sidebar.radio("Temperature Unit", ["Celsius", "Fahrenheit"], index=0)

# Generate mock weather data
def get_weather_data(start_date, end_date, temp_unit):
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    base_temp = 25 if temp_unit == "Celsius" else 77
    
    np.random.seed(42)
    temp_high = np.random.normal(base_temp, 3, size=len(date_range))
    temp_low = temp_high - np.random.uniform(5, 10, size=len(date_range))
    humidity = np.random.uniform(30, 90, size=len(date_range))
    precipitation = np.random.exponential(5, size=len(date_range))
    
    conditions = ['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain', 'Heavy Rain']
    weather_icons = ['☀️', '⛅', '☁️', '🌦️', '🌧️']
    
    df = pd.DataFrame({
        'Date': date_range,
        'Temp_High': np.round(temp_high, 1),
        'Temp_Low': np.round(temp_low, 1),
        'Humidity': np.round(humidity, 1),
        'Precipitation': np.round(precipitation, 1),
        'Condition_Index': np.minimum(np.floor(precipitation / 4), 4).astype(int)
    })
    
    df['Condition'] = [conditions[i] for i in df['Condition_Index']]
    df['Icon'] = [weather_icons[i] for i in df['Condition_Index']]
    
    return df

# Get data based on inputs
start_date, end_date = date_range if len(date_range) == 2 else (date_range[0], date_range[0])
weather_data = get_weather_data(start_date, end_date, temp_unit)

# Weather forecast display
st.header(f"Weather Forecast for {location}")

# Display condition icons and temperatures in a grid
cols = st.columns(min(7, len(weather_data)))
for idx, (i, day) in enumerate(weather_data.iterrows()):
    if idx < len(cols):
        cols[idx].metric(
            day['Date'].strftime('%a, %b %d'),
            f"{day['Icon']} {day['Condition']}",
            f"{day['Temp_High']}° / {day['Temp_Low']}°"
        )

# Temperature chart
st.subheader("Temperature Forecast")
temp_fig = px.line(
    weather_data, 
    x='Date', 
    y=['Temp_High', 'Temp_Low'],
    labels={'value': f'Temperature ({temp_unit})'},
    title=f"Temperature Forecast"
)
st.plotly_chart(temp_fig, use_container_width=True)

# Precipitation chart
st.subheader("Precipitation Forecast")
precip_fig = px.bar(
    weather_data, 
    x='Date', 
    y='Precipitation',
    labels={'Precipitation': 'Precipitation (mm)'},
    title=f"Precipitation Forecast"
)
st.plotly_chart(precip_fig, use_container_width=True)

# Data table
st.subheader("Weather Data")
display_data = weather_data[['Date', 'Temp_High', 'Temp_Low', 'Humidity', 'Precipitation', 'Condition']].copy()
display_data.columns = ['Date', f'High Temp ({temp_unit})', f'Low Temp ({temp_unit})', 'Humidity (%)', 'Precipitation (mm)', 'Condition']
st.dataframe(display_data, use_container_width=True)

st.caption("Note: This is a demo using mock data.")