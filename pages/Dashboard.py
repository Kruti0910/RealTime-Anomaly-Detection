import streamlit as st
from components.db_connection import get_data
from components.filters import apply_filters

def render():
    st.title("Real-Time Anomaly Dashboard")
    df = get_data()
    filtered_df = apply_filters(df)

    st.metric("Total Anomalies", len(df))
    st.metric("Filtered View", len(filtered_df))

    st.dataframe(filtered_df, use_container_width=True)
