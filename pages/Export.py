import streamlit as st
from components.db_connection import get_data
from components.filters import apply_filters

def render():
    st.title("Export Anomaly Data")
    df = get_data()
    filtered_df = apply_filters(df)

    csv = filtered_df.to_csv(index=False)
    st.download_button("Download CSV", csv, "anomalies_filtered.csv", mime="text/csv")
