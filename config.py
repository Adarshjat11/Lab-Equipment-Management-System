import streamlit as st

def get_admins():
    return dict(st.secrets["admins"])

