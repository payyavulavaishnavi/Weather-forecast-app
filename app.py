import os
import pytz
import pyowm
import streamlit as st
from datetime import datetime
import plotly.graph_objects as go

# Set your OWM API key
API_KEY = '641a8661c62578d375ddb9f981f47e4d'  # Make sure to replace this with your actual API key
owm = pyowm.OWM(API_KEY)
mgr = owm.weather_manager()

degree_sign = u'\N{DEGREE SIGN}'

st.title("5 Day Weather Forecast")
st.write("### Write the name of a City and select the Temperature Unit and Graph Type from the sidebar")

place = st.text_input("NAME OF THE CITY :", "")

if not place:
    st.write("Input a CITY!")
    st.stop()

unit = st.selectbox("Select Temperature Unit", ("Celsius", "Fahrenheit"))
g_type = st.selectbox("Select Graph Type", ("Line Graph", "Bar Graph"))

unit_c = 'celsius' if unit == 'Celsius' else 'fahrenheit'

def get_temperature():
    days = []
    dates = []
    temp_min = []
    temp_max = []
    try:
        forecaster = mgr.forecast_at_place(place, '3h')
        forecast = forecaster.forecast
        for weather in forecast:
            day = datetime.utcfromtimestamp(weather.reference_time())
            date = day.date()
            if date not in dates:
                dates.append(date)
                temp_min.append(None)
                temp_max.append(None)
                days.append(date)
            temperature = weather.temperature(unit_c)['temp']
            if temp_min[-1] is None or temperature < temp_min[-1]:
                temp_min[-1] = temperature
            if temp_max[-1] is None or temperature > temp_max[-1]:
                temp_max[-1] = temperature
    except Exception as e:
        st.write(f"Could not retrieve data for {place}. Please check the city name and try again.")
        st.write(f"Error details: {e}")
        st.stop()
    return days, temp_min, temp_max

def plot_temperatures(days, temp_min, temp_max):
    fig = go.Figure(
        data=[
            go.Bar(name='Minimum Temperatures', x=days, y=temp_min),
            go.Bar(name='Maximum Temperatures', x=days, y=temp_max)
        ]
    )
    fig.update_layout(barmode='group')
    return fig

def plot_temperatures_line(days, temp_min, temp_max):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=temp_min, name='Minimum Temperatures'))
    fig.add_trace(go.Scatter(x=days, y=temp_max, name='Maximum Temperatures'))
    return fig

def draw_bar_chart():
    days, temp_min, temp_max = get_temperature()
    fig = plot_temperatures(days, temp_min, temp_max)
    st.plotly_chart(fig)
    st.title("Minimum and Maximum Temperatures")
    for i in range(len(days)):
        st.write(f"### {temp_min[i]}{degree_sign} --- {temp_max[i]}{degree_sign}")

def draw_line_chart():
    days, temp_min, temp_max = get_temperature()
    fig = plot_temperatures_line(days, temp_min, temp_max)
    st.plotly_chart(fig)
    st.title("Minimum and Maximum Temperatures")
    for i in range(len(days)):
        st.write(f"### {temp_min[i]}{degree_sign} --- {temp_max[i]}{degree_sign}")

def other_weather_updates():
    forecaster = mgr.forecast_at_place(place, '3h')
    st.title("Impending Temperature Changes :")
    if forecaster.will_have_fog():
        st.write("### FOG Alert!")
    if forecaster.will_have_rain():
        st.write("### Rain Alert")
    if forecaster.will_have_storm():
        st.write("### Storm Alert!")
    if forecaster.will_have_snow():
        st.write("### Snow Alert!")
    if forecaster.will_have_tornado():
        st.write("### Tornado Alert!")
    if forecaster.will_have_hurricane():
        st.write("### Hurricane Alert!")
    if forecaster.will_have_clouds():
        st.write("### Cloudy Skies")
    if forecaster.will_have_clear():
        st.write("### Clear Weather!")

def cloud_and_wind():
    obs = mgr.weather_at_place(place)
    weather = obs.weather
    cloud_cov = weather.clouds
    winds = weather.wind()['speed']
    st.title("Cloud coverage and wind speed")
    st.write(f"### The current cloud coverage for {place} is {cloud_cov}%")
    st.write(f"### The current wind speed for {place} is {winds} mph")

def sunrise_and_sunset():
    obs = mgr.weather_at_place(place)
    weather = obs.weather
    st.title("Sunrise and Sunset Times :")
    india = pytz.timezone("Asia/Kolkata")
    ss = weather.sunset_time(timeformat='iso')
    sr = weather.sunrise_time(timeformat='iso')
    st.write(f"### Sunrise time in {place} is {sr}")
    st.write(f"### Sunset time in {place} is {ss}")

def updates():
    other_weather_updates()
    cloud_and_wind()
    sunrise_and_sunset()

if __name__ == '__main__':
    if st.button("SUBMIT"):
        if g_type == 'Line Graph':
            draw_line_chart()
        else:
            draw_bar_chart()
        updates()
