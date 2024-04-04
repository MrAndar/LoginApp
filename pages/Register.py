import pandas as pd
import streamlit as st
import re


def validation_alphanum(user):
    return bool(re.search(r'[a-zA-Z]', user)) and bool(re.search(r'\d', user))


def validation_symbols(pass_local):
    return bool(re.search(r'[^a-zA-Z0-9]', pass_local))


def validate_registration(user, pass_arg, confirm_password):
    df = pd.read_csv("users.csv")
    errors = []

    # Checks username
    if len(user) < 8:
        errors.append("Username must be 8 or more chars")
    elif not validation_alphanum(user):
        errors.append("Username must contains letters and numbers")
    elif (df['username'] == user).any():
        errors.append("Username already exists.")

    # Checks password
    if len(pass_arg) < 8:
        errors.append("Password must be 8 or more chars")
    elif not validation_alphanum(pass_arg):
        errors.append("Password must contains letters and numbers")
    elif not validation_symbols(pass_arg):
        errors.append("Password must contain symbol(s)")

    # Checks confirmed password
    if pass_arg != confirm_password:
        errors.append("Passwords do not match")

    return errors


def add_user(user, pass_arg, filename="users.csv"):

    # Convert new user to dict
    new_user = {"username": [user], "password": [pass_arg]}
    # Convert dict to dataframe
    new_user_df = pd.DataFrame(new_user)

    # reading users from file as dataframe
    df = pd.read_csv(filename)
    # Combining new user df with file df
    df = pd.concat([df, new_user_df])
    # Overwriting users in file
    df.to_csv(filename, index=False)


# Widgets
st.title("Register")

register_info = '''
Username requirements:
- 8 or more characters
- must contain letters and numbers

Password requirements:
- 8 or more characters
- must contain letters and numbers
- must contain a symbol
'''

st.info(register_info)

username = st.text_input("Username")
password = st.text_input("Password", type="password")
confirm_pass = st.text_input("Confirm Password", type="password")

if st.button("Register"):
    validation_errors = validate_registration(username, password, confirm_pass)
    if not validation_errors:
        add_user(username, password)
        st.success("Registration successful.")
    else:
        for item in validation_errors:
            st.error(item)
