import streamlit as st
import pandas as pd
import psycopg2

st.title("Real-Time Anomaly Dashboard")

conn = psycopg2.connect(database="anomalies", user="user", password="pass", host="localhost", port="5432")
df = pd.read_sql("SELECT * FROM frauds", conn)

st.write("Detected Anomalies:")
st.dataframe(df)
