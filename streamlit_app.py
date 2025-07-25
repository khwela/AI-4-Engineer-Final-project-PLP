import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
import random
import datetime 


def generate_otp():
    return random.randint(100000, 999999)

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


# SMTP Email Sending Function
def send_otp_email(email, otp):
    sender_email = "your_email@gmail.com"  # Replace with your email
    sender_password = "your_app_password"  # Replace with your app password
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create the email content
    subject = "Your OTP Code"
    body = f"Your OTP code is: {otp}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = email

    try:
        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade the connection to secure
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        st.success("OTP email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        st.error("Authentication failed. Please check your email and App Password.")
    except smtplib.SMTPException as e:
        st.error(f"Failed to send email: {e}")
        

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

        # Generate and store OTP in session state
        otp = generate_otp()
        st.session_state["otp"] = otp
        send_otp_email(email, otp)
        st.success("An OTP has been sent to your email. Please enter it below to complete registration.")

    # OTP Verification
    if "otp" in st.session_state:
        entered_otp = st.text_input("Enter the OTP sent to your email", key="register_otp")
        if st.button("Verify OTP", key="verify_otp_button"):
            if entered_otp == str(st.session_state["otp"]):  # Compare as string
                new_user = pd.DataFrame([[email, name, phone, password, True]], columns=users_df.columns)
                users_df = pd.concat([users_df, new_user], ignore_index=True)
                users_df.to_csv(users_file, index=False)
                st.success("Registration complete! You can now log in.")
                del st.session_state["otp"]  # Clear OTP from session state
            else:
                st.error("Invalid OTP. Please try again.")

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
                st.error("Invalid password.")
    else:
              st.error("Invalid email.")

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
