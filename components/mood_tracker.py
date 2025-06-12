import streamlit as st
from datetime import date
import os
from dotenv import load_dotenv
from datetime import datetime 
import pandas as pd
from client.sql_client import DatabricksSQLClient


MOOD_ENTRY_TABLE = "mood_mate.app.mood_entry"

client = DatabricksSQLClient()
load_dotenv()
def mood_tracker_page():
    st.subheader("How are you feeling today?")

    mood_options = {
        "😀 Happy": "happy",
        "😢 Sad": "sad",
        "😠 Angry": "angry",
        "😨 Anxious": "anxious",
        "😐 Neutral": "neutral",
        "😴 Tired": "tired"
    }

    mood = st.radio(
        "Select your mood:",
        list(mood_options.keys()),
        horizontal=True
    )

    rating = st.slider("Rate your mood (1=Low, 10=High):", 1, 10, 5)

    now = datetime.now()

    if st.button("Submit mood entry"):
        row_data = {
            "mood": mood_options[mood],
            "rating": rating,
            "entry_date": now.strftime('%Y-%m-%d %H:%M:%S')
        }
        client.insert_row(MOOD_ENTRY_TABLE, row_data)
        st.success(f"Entry saved! Mood: {mood}, Rating: {rating}, Date: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# # create table
        # client = DatabricksSQLClient()
        # columns = """
        #     id INT,
        #     mood STRING,
        #     rating INT,
        #     entry_date TIMESTAMP
        # """
        # client.create_table("mood_mate", "app", "mood_entry", columns)
        # st.success("Table created successfully!")
