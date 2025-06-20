import streamlit as st
from streamlit_option_menu import option_menu

from components.journal import journal_page
from components.tracker import tracker_page
from components.random_facts import get_random_fact
from components.trends import trends_page

st.set_page_config(page_title="Mental Health Check-in App", layout="wide")

st.title("Welcome to Mood Mate!")

# Top menu bar
selected = option_menu(
    None,
    ["Tracker", "Journal", "Trends"], #, "Chatbot"],
    icons=["emoji-smile", "book", "bar-chart"], #, "chat"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if selected == "Tracker":
    tracker_page() 
    # get_random_fact()

elif selected == "Journal":
    journal_page()

elif selected == "Trends":
    trends_page()
    # TODO: Add visualization here

# elif selected == "Chatbot":
#     st.subheader("Chatbot")
#     # TODO: Add chatbot UI here