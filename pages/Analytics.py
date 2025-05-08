import streamlit as st
import altair as alt
from components.db_connection import get_data
from components.filters import apply_filters

def render():
    st.title("Analytics and Trends")
    df = get_data()
    df = apply_filters(df)

    st.subheader("Anomalies by Location")
    chart = alt.Chart(df).mark_bar().encode(
        x='location:N',
        y='amount:Q',
        color='location:N'
    )
    st.altair_chart(chart, use_container_width=True)

    st.subheader("Trend Over Time")
    trend = alt.Chart(df).mark_line(point=True).encode(
        x='datetime:T',
        y='amount:Q',
        tooltip=["user_id", "amount", "datetime"]
    )
    st.altair_chart(trend, use_container_width=True)
