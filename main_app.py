# Smart Home Affairs Assistant using Streamlit

import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import os
import openai
from dotenv import load_dotenv


# Session states
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Load users
users_file = "users.csv"
if not os.path.exists(users_file):
    pd.DataFrame(columns=["email", "name", "phone", "password", "first_time"]).to_csv(users_file, index=False)

users_df = pd.read_csv(users_file)


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
tabs = st.tabs(["📄 Digital ID Upload", "📅 Book Appointment","📁 Upload Documents", "🤖 Chatbot (Mock)", "📊 Admin Dashboard"])


# --- Tab 1: Scan Digital ID ---
with tabs[0]:
    st.header("📷 Scan Your ID or Passport")
    name = st.text_input("Full Name", key="scan_full_name")
    id_number = st.text_input("ID Number", key="scan_id_number")
    upload_id = st.checkbox("Upload ID")
    upload_passport = st.checkbox("Upload Passport")

    if upload_id:
        st.subheader("📸 Scan ID")
        id_image = st.camera_input("Take a picture of your ID")
        if id_image:
            id_dir = "scanned_ids"
            os.makedirs(id_dir, exist_ok=True)
            image = Image.open(id_image)
            image.save(os.path.join(id_dir, f"{id_number}_{name.replace(' ', '_')}_ID.jpg"))
            st.success("ID scanned and saved.")

    if upload_passport:
        st.subheader("📸 Scan Passport")
        passport_image = st.camera_input("Take a picture of your Passport")
        if passport_image:
            id_dir = "scanned_ids"
            os.makedirs(id_dir, exist_ok=True)
            image = Image.open(passport_image)
            image.save(os.path.join(id_dir, f"{id_number}_{name.replace(' ', '_')}_Passport.jpg"))
            st.success("Passport scanned and saved.")

# --- Tab 2: Appointment Booking ---
with tabs[1]:
    full_name = st.text_input("Full Name", key="appt_full_name")
    email = st.text_input("Email Address", key="appt_email")
    phone = st.text_input("Phone Number", key="appt_phone")
    service = st.selectbox("Select a service", ["New ID", "Passport Renewal", "Birth Certificate", "Marriage Certificate"])
    province = st.selectbox("Select Province", ["Gauteng", "KZN", "Western Cape", "Eastern Cape"])
    branch = st.selectbox("Select Branch", ["Johannesburg Central", "Durban Office", "Cape Town Civic", "Port Elizabeth"])
    date = st.date_input("Select Appointment Date")
    time = st.time_input("Select Appointment Time")
    

    if st.button("Confirm Booking"):
        booking = {
            "Full Name": full_name,
            "Email": email,
            "Phone": phone,
            
            "Service": service,
            "Province": province,
            "Branch": branch,
            "Date": date.strftime("%Y-%m-%d"),
            "Time": time.strftime("%H:%M")
        }
        st.success(f"Appointment confirmed for {booking['Full Name']} ({booking['Email']}, {booking['Phone']}) for {booking['Service']} on {booking['Date']} at {booking['Time']} in {booking['Branch']}, {booking['Province']}")

# --- Tab 3: Upload Documents ---
with tabs[2]:
    st.header("📁 Upload Supporting Documents")
    st.markdown("Upload any number of personal or legal documents below.")
    uploaded_file = st.file_uploader("Choose a file to upload", type=["pdf", "jpg", "jpeg", "png", "docx"], key="multiple_uploads")
    upload_dir = "uploaded_documents"
    os.makedirs(upload_dir, exist_ok=True)
    if uploaded_file:
        save_path = os.path.join(upload_dir, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success(f"{uploaded_file.name} uploaded successfully.")

    st.markdown("### 📄 Uploaded Files (Oldest to Newest):")
    uploaded_files = sorted(os.listdir(upload_dir))
    for file in uploaded_files:
        st.write(f"📎 {file}")
        
        
# --- Tab 4: Chatbot using OpenAI ---
with tabs[3]:
    st.header("🤖 AI Chatbot Assistant")
    st.markdown("Ask any question about Home Affairs services.")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "system", "content": "You are a helpful assistant for the South African Department of Home Affairs. Answer user questions clearly and helpfully."}
        ]

    # User input
    user_input = st.text_input("You:")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        try:
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.chat_history
            )
            reply = response.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
        except openai.error.AuthenticationError:
            st.error("Invalid API key. Please check your OpenAI API key.")
        except openai.error.RateLimitError:
            st.error("You have exceeded your API quota. Please check your OpenAI account.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Display chat history
    for msg in st.session_state.chat_history[1:]:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Bot:** {msg['content']}")

# --- Tab 5: Admin Dashboard ---
with tabs[4]:
    st.header("📊 Admin Dashboard")
    st.markdown("_Simulated statistics for demo purposes_")
    stats = pd.DataFrame({
        "Service": ["New ID", "Passport Renewal", "Birth Certificate"],
        "Bookings": [120, 85, 45]
    })
    st.bar_chart(stats.set_index("Service"))


    # Place rest of app here (upload, bookings, digital ID etc.)
