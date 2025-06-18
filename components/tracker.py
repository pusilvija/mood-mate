import streamlit as st
from datetime import date
import os
import numpy as np
from dotenv import load_dotenv
from datetime import datetime 
import pandas as pd
from client.sql_client import DatabricksSQLClient


TRACKER_TABLE = "mood_mate.app.tracker_entry"

load_dotenv()

client = DatabricksSQLClient()


def tracker_page():
    create_tracker_table()

    st.subheader("Select the entries you want to add:")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    with col1:
        mood_selected = st.checkbox("Mood", value=True)
    with col2:
        sleep_selected = st.checkbox("Sleep", value=True)
    with col3:
        exercise_selected = st.checkbox("Exercise", value=False)
    with col4:
        caffeine_selected = st.checkbox("Caffeine", value=False)
    with col5:
        water_selected = st.checkbox("Water", value=False)
    with col6:
        screen_selected = st.checkbox("Screen Time", value=False)
    with col7:
        meditation_selected = st.checkbox("Meditation", value=False)

    now = datetime.now()

    if mood_selected:
        st.subheader("Mood Tracker")
        mood_options = {
            "😀 Happy": "happy",
            "😢 Sad": "sad",
            "😠 Angry": "angry",
            "😨 Anxious": "anxious",
            "😐 Neutral": "neutral",
            "😴 Tired": "tired"
        }
        mood = st.radio("Select your mood:", list(mood_options.keys()), horizontal=True)
        mood_rating = st.slider("Rate your mood (1=Low, 10=High):", 1, 10, 5)

    if sleep_selected:
        st.subheader("Sleep Tracker")
        sleep_quality = st.radio("Rate your sleep quality:", ["Poor", "Average", "Good", "Excellent"], horizontal=True)
        sleep_duration = st.slider("How many hours did you sleep last night?", 0, 12, 7)

    if exercise_selected:
        st.subheader("Exercise Tracker")
        exercise_duration = st.slider("How many minutes did you exercise today?", 0, 120, 30)
        exercise_type = st.selectbox("What type of exercise did you do?", ["None", "Running", "Cardio", "Strength Training", "Yoga", "Other"])

    if caffeine_selected:
        st.subheader("Caffeine Intake Tracker")
        caffeine_intake = st.slider("How many cups of coffee did you consume today?", 0, 10, 2)

    if water_selected:
        st.subheader("Water Intake Tracker")
        water_intake = st.slider("How many glasses of water did you drink today?", 0, 20, 8)

    if screen_selected:
        st.subheader("Screen Time Tracker")
        screen_time = st.slider("How many hours did you spend on screens today?", 0, 12, 5)

    if meditation_selected:
        st.subheader("Meditation Tracker")
        meditation_duration = st.slider("How many minutes did you meditate today?", 0, 60, 10)


    tracker_entry = pd.DataFrame({
        "mood": [mood_options[mood] if mood_selected else None],
        "mood_rating": [mood_rating if mood_selected else None],
        "sleep_hours": [sleep_duration if sleep_selected else None],
        "sleep_quality": [sleep_quality if sleep_selected else None],
        "exercise_duration": [exercise_duration if exercise_selected else None],
        "exercise_type": [exercise_type if exercise_selected else None],
        "caffeine_intake": [caffeine_intake if caffeine_selected else None],
        "water_intake": [water_intake if water_selected else None],
        "screen_time": [screen_time if screen_selected else None],
        "meditation_duration": [meditation_duration if meditation_selected else None],
        "entry_date": [now.strftime('%Y-%m-%d %H:%M:%S')]
    })

    st.write(tracker_entry)  


    if st.button("Submit entry"):
            row_data = tracker_entry.loc[0].to_dict()
            client.insert_row(TRACKER_TABLE, row_data)
            st.success(f"Tracker entry saved successfully for {now.strftime('%Y-%m-%d %H:%M:%S')}!")


def create_tracker_table():
    query = f"SHOW TABLES IN mood_mate.app"
    cursor = client.conn.cursor()
    cursor.execute(query)
    tables = [row[1] for row in cursor.fetchall()]
    cursor.close()

    if "tracker_entry" not in tables:
        columns = """
            mood STRING,
            mood_rating INT,
            sleep_hours INT,
            sleep_quality STRING,
            exercise_duration INT,
            exercise_type STRING,
            caffeine_intake INT,
            water_intake INT,
            screen_time INT,
            meditation_duration INT,
            entry_date TIMESTAMP
        """
        client.create_table("mood_mate", "app", "tracker_entry", columns)
