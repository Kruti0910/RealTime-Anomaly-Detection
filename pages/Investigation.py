import streamlit as st
from components.db_connection import get_data

def render():
    st.title("User Investigation Tool")
    df = get_data()
    user_id = st.text_input("Search by User ID")

    if user_id:
        result = df[df["user_id"].astype(str) == user_id.strip()]
        st.write(f"Results for User ID {user_id}:")
        st.dataframe(result)
