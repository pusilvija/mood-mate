import streamlit as st
from datetime import datetime
import pandas as pd
from client.sql_client import DatabricksSQLClient

# Load the database client
client = DatabricksSQLClient()

JOURNAL_TABLE = "mood_mate.app.journal_entry"

def journal_page():
    create_journal_table()
    st.subheader("Write down your thoughts and feelings")

    entry_date = datetime.now().date()
    entry_time = datetime.now().time()
    journal_text = st.text_area("What's on your mind?", placeholder="Write your journal entry here...")

    if st.button("Save Entry"):
        if journal_text.strip():
            entry_datetime = datetime.combine(entry_date, entry_time)
            journal_entry = pd.DataFrame({
                "entry_date": [entry_datetime.strftime('%Y-%m-%d %H:%M:%S')],
                "journal_text": [journal_text]
            })
            row_data = journal_entry.loc[0].to_dict()
            client.insert_row(JOURNAL_TABLE, row_data)
            st.success(f"Journal entry saved successfully for {entry_datetime.strftime('%Y-%m-%d %H:%M:%S')}!")
        else:
            st.error("Journal entry cannot be empty.")

    st.subheader("Your Past Entries")
    query = f"SELECT * FROM {JOURNAL_TABLE} ORDER BY entry_date DESC"
    past_entries = pd.read_sql(query, client.conn)

    if past_entries.empty:
        st.info("No journal entries found.")
    else:
        for _, row in past_entries.iterrows():
            st.write(f"**{row['entry_date']}**")
            st.write(row['journal_text'])
            st.markdown("---")

def create_journal_table():
    query = f"SHOW TABLES IN mood_mate.app"
    cursor = client.conn.cursor()
    cursor.execute(query)
    tables = [row[1] for row in cursor.fetchall()]
    cursor.close()

    if "journal_entry" not in tables:
        columns = """
            journal_text STRING,
            entry_date TIMESTAMP
        """
        client.create_table("mood_mate", "app", "journal_entry", columns)
