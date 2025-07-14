# Smart Home Affairs Assistant using Streamlit

import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Home Affairs AI Assistant", layout="wide")

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

# --- Tab 1: Digital ID Upload ---
with tabs[0]:
    st.header("📄 Upload Your Digital ID")
    name = st.text_input("Full Name")
    id_number = st.text_input("ID Number")
    uploaded_file = st.file_uploader("Upload your ID or Passport (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])

    if st.button("Save Document"):
        if name and id_number and uploaded_file:
            upload_dir = "uploaded_ids"
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"ID for {name} uploaded successfully!")
        else:
            st.warning("Please fill all fields and upload a file.")

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

# --- Tab 3: Chatbot Placeholder ---
with tabs[2]:
    st.header("🤖 AI Chatbot Assistant")
    st.markdown("_Note: This is a placeholder. Integrate OpenAI or Dialogflow for full functionality._")
    user_input = st.text_input("Ask me anything about Home Affairs services")
    if user_input:
        st.info(f"You asked: {user_input}")
        st.success("This is a mock response. You can connect this to a real AI model.")

# --- Tab 4: Admin Dashboard ---
with tabs[3]:
    st.header("📊 Admin Dashboard")
    st.markdown("_Simulated statistics for demo purposes_")
    stats = pd.DataFrame({
        "Service": ["New ID", "Passport Renewal", "Birth Certificate"],
        "Bookings": [120, 85, 45]
    })
    st.bar_chart(stats.set_index("Service"))
