import streamlit as st
import requests

import numpy as np
import pandas as pd

## Markdown to style and fill content in your page
st.markdown("""
            # 😸🐶 AI generate NFT for your pet
            """)

st.image("https://thenftunicorn.com/wp-content/uploads/2022/06/Metaimage_petaverse-1.jpg")

col1, col2 = st.columns(2)

with col1:
  date = st.date_input("Please enter date")

with col2:
  time = st.time_input("Please enter time")


psngr_count = st.slider("How many passengers are you?", 1, 10)

pickup = st.text_input("Your pickup address")

if pickup:
  geo_url = f"https://nominatim.openstreetmap.org/search?q={pickup}&format=jsonv2"
  res = requests.get(geo_url).json()
  try:
    pickup_lat = res[0]['lat']
    pickup_lon = res[0]['lon']
  except IndexError:
    st.write("🤯 sorry we couldn't find you, please try again!")

dropoff = st.text_input("Your dropoff address")

if dropoff:
  geo_url = f"https://nominatim.openstreetmap.org/search?q={dropoff}&format=jsonv2"
  res = requests.get(geo_url).json()
  try:
    dropoff_lat = res[0]['lat']
    dropoff_lon = res[0]['lon']
  except IndexError:
    st.write("🤯 sorry we couldn't find you, please try again!")

if st.button("Predict Fare"):
  params = {
    "pickup_datetime": f"{date} {time}",
    "pickup_latitude": pickup_lat,
    "pickup_longitude": pickup_lon,
    "dropoff_latitude": dropoff_lat,
    "dropoff_longitude": dropoff_lon,
    "passenger_count": psngr_count
  }
  api_url = "https://taxifare-api-x4gzhnh2ta-uw.a.run.app/predict"
  res = requests.get(api_url, params).json()

  st.write("""
          <style>
            .headline {
                font-family: MicSans,sans-serif;
                font-size: 20px;
                font-weight: 700;
                line-height: 1.5;
                background-color: black;
                box-shadow: 8px 1px 0 3px black, -8px 1px 0 3px black;
                color: pink;
                padding: 20px;
            }
          </style>
          """
          + f'<h1 class="headline">{round(res["fare"], 2)} USD</h1>'
          , unsafe_allow_html=True)
