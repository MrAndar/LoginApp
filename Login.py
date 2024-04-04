import pandas as pd
import streamlit as st


# Validate username and password
def validate_user_pass(user, pass_arg):
    df = pd.read_csv("users.csv")
    return ((df['username'] == user) & (df['password'] == pass_arg)).any()


st.title("Login")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if validate_user_pass(username, password):
        st.success("Logging in...")
    else:
        st.error("Invalid username or password.")
