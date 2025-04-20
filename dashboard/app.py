import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import OperationalError
from streamlit_autorefresh import st_autorefresh
import altair as alt

st.set_page_config(page_title="Real-Time Anomaly Dashboard", layout="wide")

# Auto-refresh every 10 seconds (10000 ms)
st_autorefresh(interval=10000, limit=None, key="auto-refresh")

st.title("Real-Time Anomaly Dashboard")

try:
    conn = psycopg2.connect(
        database="anomalies",
        user="user",
        password="pass",
        host="localhost",
        port="5432"
    )

    df = pd.read_sql("SELECT * FROM frauds", conn)

    st.write("Detected Anomalies:")
    st.dataframe(df)

    if not df.empty:
        chart = alt.Chart(df).mark_bar().encode(
            x='location:N',
            y='amount:Q',
            color='location:N'
        ).properties(
            title="Anomalous Transaction Amounts by Location"
        )

        st.altair_chart(chart, use_container_width=True)

except OperationalError as e:
    st.error("Failed to connect to the database. Please check credentials and Docker status.")
    st.code(str(e))
