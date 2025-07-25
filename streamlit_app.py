import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
import random
import datetime 


# Initialize session state variables
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user_email" not in st.session_state:
    st.session_state["user_email"] = None

# Path to the CSV file storing user data
users_file = "C:\\2025 COHORT FEB\\AI For Software Engineering\\Final  project\\users.csv"

# Ensure the users file exists
if not os.path.exists(users_file):
    pd.DataFrame(columns=["email", "name", "phone", "password", "first_time"]).to_csv(users_file, index=False)

# Load the users DataFrame
users_df = pd.read_csv(users_file)


# Registration Function
def register_user():
    global users_df  # Declare users_df as global to modify it
    st.subheader("Register")
    name = st.text_input("Full Name", key="register_name")
    email = st.text_input("Email", key="register_email")
    phone = st.text_input("Phone", key="register_phone")
    password = st.text_input("Password", type="password", key="register_password")

    if st.button("Register", key="register_button"):
        if email in users_df["email"].values:
            st.warning("User already exists. Please log in.")
            return

        # Add the new user to the DataFrame
        new_user = pd.DataFrame([[email, name, phone, password, True]], columns=users_df.columns)
        users_df = pd.concat([users_df, new_user], ignore_index=True)
        users_df.to_csv(users_file, index=False)
        st.success("Registration complete! You can now log in.")

# Login Function
def login_user():
    global users_df  # Declare users_df as global to access it
    st.subheader("Log In")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        user = users_df[users_df["email"] == email]
        if not user.empty and password == user.iloc[0]["password"]:
            st.session_state["authenticated"] = True
            st.session_state["user_email"] = email
            st.success("Login successful!")
        else:
            st.error("Invalid email or password.")

# Main App Function
def main_app():
    st.title("Welcome to the Main App!")
    st.markdown(f"Hello, **{st.session_state['user_email']}**! You are now logged in.")
    st.button("Log Out", on_click=logout)

# Logout Function
def logout():
    st.session_state["authenticated"] = False
    st.session_state["user_email"] = None
    st.experimental_rerun()

# App Flow
if not st.session_state["authenticated"]:
    st.title("Home Affairs App")
    st.markdown("Please register or log in to continue.")
    tab1, tab2 = st.tabs(["Register", "Log In"])

    with tab1:
        register_user()
    with tab2:
        login_user()
else:
    main_app()
