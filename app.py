import streamlit as st
from streamlit_option_menu import option_menu

from components.mood_tracker import mood_tracker_page

st.set_page_config(page_title="Mental Health Check-in App", layout="wide")

st.title("Welcome to Mood Mate!")

# Top menu bar
selected = option_menu(
    None,
    ["Mood Tracker", "Journal", "Trends"], #, "Chatbot"],
    icons=["emoji-smile", "book", "bar-chart"], #, "chat"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if selected == "Mood Tracker":
    mood_tracker_page() 

elif selected == "Journal":
    st.subheader("Journal")
    # TODO: Add journaling UI here

elif selected == "Trends":
    st.subheader("Trends")
    # TODO: Add visualization here

# elif selected == "Chatbot":
#     st.subheader("Chatbot")
#     # TODO: Add chatbot UI here