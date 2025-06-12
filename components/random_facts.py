import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_random_fact():
    response = requests.get(
        "https://api.api-ninjas.com/v1/facts?category",
        headers={"X-Api-Key": os.getenv("NINJAS_API_KEY")}
    )
    if response.status_code == 200:
        fact = response.json()[0]["fact"]
        st.markdown(
            f"""
            <div style="
                background-color: #ecfadc;
                padding: 15px;
                border-radius: 10px;
                border: 1px solid #ddd;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            ">
                <h4 style="color: #333; margin-bottom: 10px;">Random Fact:</h4>
                <p style="color: #555; font-size: 16px;">{fact}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error("Could not fetch a random fact right now. Please try again later.")