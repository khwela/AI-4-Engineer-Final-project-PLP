# Smart Home Affairs Assistant using Streamlit

import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Home Affairs AI Assistant", layout="wide")

def home_affairs_bot(user_input):
    user_input = user_input.lower()
    if "passport" in user_input:
        return "You can renew your passport at any Home Affairs branch. Book online!"
    elif "id" in user_input:
        return "New IDs require your birth certificate and fingerprints."
    elif "hours" in user_input or "open" in user_input:
        return "Most branches are open from 8:00 AM to 3:30 PM on weekdays."
    else:
        return "Sorry, I don’t understand that. Please ask about IDs, passports, or bookings."



# --- App Title ---
st.title("🇿🇦 Smart Home Affairs AI Assistant")
st.markdown("""
This app helps South African citizens:
- Upload and store digital IDs
- Book appointments
- Interact with an AI assistant for FAQs
""")

# --- Tabs ---
tabs = st.tabs(["📄 Digital ID Upload", "📅 Book Appointment", "🤖 Chatbot (Mock)", "📊 Admin Dashboard"])

# --- Tab 1: Scan Digital ID ---
with tabs[0]:
    st.header("📷 Scan Your ID or Passport")
    name = st.text_input("Full Name")
    id_number = st.text_input("ID Number")
    scanned_image = st.camera_input("Take a picture of your ID or Passport")

    if st.button("Save Scanned ID"):
        if name and id_number and scanned_image:
            scan_dir = "scanned_ids"
            os.makedirs(scan_dir, exist_ok=True)
            image = Image.open(scanned_image)
            file_path = os.path.join(scan_dir, f"{id_number}_{name.replace(' ', '_')}.jpg")
            image.save(file_path)
            st.success(f"ID for {name} scanned and saved successfully!")
        else:
            st.warning("Please fill in your name and ID number, and scan your ID.")

# --- Tab 2: Appointment Booking ---
with tabs[1]:
    st.header("📅 Book an Appointment")
    service = st.selectbox("Select a service", ["New ID", "Passport Renewal", "Birth Certificate", "Marriage Certificate"])
    province = st.selectbox("Select Province", ["Gauteng", "KZN", "Western Cape", "Eastern Cape"])
    branch = st.selectbox("Select Branch", ["Johannesburg Central", "Durban Office", "Cape Town Civic", "Port Elizabeth"])
    date = st.date_input("Select Appointment Date")
    time = st.time_input("Select Appointment Time")

    if st.button("Confirm Booking"):
        booking = {
            "Service": service,
            "Province": province,
            "Branch": branch,
            "Date": date.strftime("%Y-%m-%d"),
            "Time": time.strftime("%H:%M")
        }
        st.success(f"Appointment confirmed for {booking['Service']} on {booking['Date']} at {booking['Time']} in {booking['Branch']}, {booking['Province']}")

# --- Tab 3: Chatbot using ChatterBot ---
with tabs[2]:
    st.header("🤖 AI Chatbot Assistant")
    st.markdown("Ask about Home Affairs services (e.g., ID, passport, booking)")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("You:")
    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        bot_response = home_affairs_bot(user_input)
        st.session_state.chat_history.append(("bot", bot_response))

    for sender, message in st.session_state.chat_history:
        if sender == "user":
            st.markdown(f"**You:** {message}")
        else:
            st.markdown(f"**Bot:** {message}")

# --- Tab 4: Admin Dashboard ---
with tabs[3]:
    st.header("📊 Admin Dashboard")
    st.markdown("_Simulated statistics for demo purposes_")
    stats = pd.DataFrame({
        "Service": ["New ID", "Passport Renewal", "Birth Certificate"],
        "Bookings": [120, 85, 45]
    })
    st.bar_chart(stats.set_index("Service"))
