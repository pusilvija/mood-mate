import streamlit as st
import pandas as pd
from client.sql_client import DatabricksSQLClient

# Load the database client
client = DatabricksSQLClient()

TRACKER_TABLE = "mood_mate.app.tracker_entry"

def trends_page():
    st.title("Trend Analysis")
    st.subheader("Explore correlations between tracker data")

    # Fetch data from the tracker table
    query = f"SELECT * FROM {TRACKER_TABLE}"
    data = pd.read_sql(query, client.conn)

    if data.empty:
        st.warning("No data available in the tracker table.")
        return

    # Filter numeric columns and exclude specific columns
    numeric_columns = data.select_dtypes(include=["number"]).columns
    excluded_columns = ["mood", "sleep_quality"]
    selectable_columns = [col for col in numeric_columns if col not in excluded_columns]

    if not selectable_columns:
        st.warning("No numeric columns available for correlation analysis.")
        return

    # Allow users to select columns for correlation analysis
    col1, col2 = st.columns(2)

    with col1:
        x_axis = st.selectbox("Select X-axis column:", selectable_columns)
    with col2:
        y_axis = st.selectbox("Select Y-axis column:", selectable_columns)

    # Display the correlation value
    if x_axis and y_axis:
        correlation = data[x_axis].corr(data[y_axis])
        st.write(f"Correlation between {x_axis} and {y_axis}: {correlation:.2f}")

        # Plot the trend chart
        st.line_chart(data[[x_axis, y_axis]])
