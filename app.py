import streamlit as st
from streamlit_option_menu import option_menu

from components.tracker import tracker_page
from components.random_facts import get_random_fact

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
    st.subheader("Journal")
    # TODO: Add journaling UI here

elif selected == "Trends":
    st.subheader("Trends")
    # TODO: Add visualization here

# elif selected == "Chatbot":
#     st.subheader("Chatbot")
#     # TODO: Add chatbot UI here