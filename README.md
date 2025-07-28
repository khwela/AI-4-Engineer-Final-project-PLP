# Home Affairs AI Assistance
The Smart Home Affairs AI Assistant is a Streamlit-based web application designed to assist South African citizens with various Home Affairs services. The app provides features such as uploading digital IDs, booking appointments, interacting with an AI chatbot, and accessing an admin dashboard for simulated statistics.

Main App: https://ai-4-engineer-final-project-plp-weotef4tgvcuhaxptmql7u.streamlit.app/


Register page : https://chatbot-zs0khnt6q9m.streamlit.app/


# Features


1. Digital ID Upload:
-Users can scan and upload their ID or passport using their device's camera.
-Uploaded files are stored locally in the scanned_ids directory.


2. Appointment Booking:
-Users can book appointments for services such as:
-New ID
-Passport Renewal
-Birth Certificate
-Marriage Certificate
-Appointments include selecting a province, branch, date, and time.


Document Upload:
-Users can upload supporting documents (e.g., PDFs, images, Word files).
-Uploaded files are stored locally in the uploaded_documents directory.


AI Chatbot:
-Users can interact with a chatbot powered by OpenAI's GPT-3.5 model.
-The chatbot answers questions about Home Affairs services, such as passport renewal, ID requirements, and branch hours.


Admin Dashboard:
-Displays simulated statistics for services like New ID, Passport Renewal, and Birth Certificate bookings.
Includes a bar chart visualization.



### How It Works
1. **Session Management**:
   - The app uses Streamlit's session state to manage user authentication and chatbot history.

2. **File Handling**:
   - Uploaded files are saved locally in predefined directories (`scanned_ids` and uploaded_documents).

3. **Chatbot Integration**:
   - The chatbot uses OpenAI's API to process user queries and provide relevant responses.

4. **Data Storage**:
   - User data (e.g., email, name, phone, password) is stored in a CSV file (`users.csv`).

---



### Requirements
- Python 3.8 or higher
- Libraries:
  - `streamlit`
  - `pandas`
  - `openai`
  - `python-dotenv`
  - `Pillow`





### How to run it on your own machine

1. Install the requirements

   $ pip install -r requirements.txt
   

2. Run the app
   
   $ streamlit run streamlit_app.py
   
