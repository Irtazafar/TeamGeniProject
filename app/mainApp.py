import streamlit as st

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #00acc1;
        color: white;
        border-radius: 8px;
        font-size: 16px;
        margin-top: 10px;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #ccc;
        padding: 10px;
        font-size: 14px;
    }
    .stSelectbox>div>div>div {
        border-radius: 8px;
        border: 1px solid #ccc;
        padding: 10px;
        font-size: 14px;
    }
    .stFormSubmitButton {
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Function to handle login
def handle_login(username, password):
    if username == "admin" and password == "password":  # Placeholder for actual authentication
        st.session_state.logged_in = True
        st.session_state.username = username
    else:
        st.error("Invalid username or password")

# Function to handle signup (Placeholder)
def handle_signup(username, password, disease):
    # Placeholder for actual signup logic
    st.success("User registered successfully. You can now log in.")
    st.session_state.show_login = True
    st.session_state.show_signup = False

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'show_login' not in st.session_state:
    st.session_state.show_login = True
if 'show_signup' not in st.session_state:
    st.session_state.show_signup = False

# Login/signup forms
if not st.session_state.logged_in:
    if st.session_state.show_login and not st.session_state.show_signup:
        st.header("🔑 Login")
        with st.form(key='login_form'):
            username = st.text_input("👤 Username")
            password = st.text_input("🔒 Password", type="password")
            submit_button = st.form_submit_button(label='Login')
            if submit_button:
                handle_login(username, password)
        if st.button("Don't have an account? ✍️ Sign Up"):
            st.session_state.show_login = False
            st.session_state.show_signup = True
            st.experimental_rerun()

    elif st.session_state.show_signup and not st.session_state.show_login:
        st.header("✍️ Sign Up")
        with st.form(key='signup_form'):
            new_username = st.text_input("👤 Choose a Username")
            new_password = st.text_input("🔒 Choose a Password", type="password")
            disease = st.selectbox("Select Your Disease", ["Diabetes", "Hypertension", "Heart Disease", "Other"])
            other = st.text_input("If selected Other, specify:")
            signup_button = st.form_submit_button(label='Sign Up')
            if signup_button:
                handle_signup(new_username, new_password, disease)
        if st.button("Already have an account? 🔑 Login"):
            st.session_state.show_signup = False
            st.session_state.show_login = True
            st.experimental_rerun()

else:
    st.title("🏥 Virtual Nurse App")
    st.write("Empathy-driven AI to manage your health effectively. 🌟")

    # Tabs navigation
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🏠 Home", "🩺 Symptom Checker", "⏰ Reminders", "📈 Health Monitoring", "📚 Educational Resources", "🚨 Emergency Alerts"])

    with tab1:
        st.header("Chat with Your Virtual Nurse 💬")
        user_input = st.text_input("You: ", "")
        if user_input:
            st.write("Virtual Nurse: I'm here to help you with your health needs. 😊")
            
    with tab2:
        st.header("Symptom Checker 🩺")
        symptoms = st.text_input("Describe your symptoms:")
        if st.button("Check Symptoms"):
            st.write("Based on your symptoms, here's what you should do... (Placeholder for AI-powered triage)")

    with tab3:
        st.header("Reminders ⏰")
        reminder_type = st.selectbox("Reminder Type", ["Medication 💊", "Appointment 🗓️"])
        if reminder_type == "Medication 💊":
            med_name = st.text_input("Medication Name")
            dosage = st.text_input("Dosage")
            reminder_time = st.time_input("Reminder Time")
            if st.button("Set Reminder"):
                st.write(f"Reminder set for {med_name} at {reminder_time}.")
        else:
            appointment_details = st.text_input("Appointment Details")
            appointment_time = st.time_input("Appointment Time")
            if st.button("Set Reminder"):
                st.write(f"Reminder set for appointment at {appointment_time}.")

    with tab4:
        st.header("Health Monitoring 📈")
        st.write("Connect your wearable device to monitor your health in real-time. (Placeholder for integration)")

    with tab5:
        st.header("Educational Resources 📚")
        st.write("Access personalized educational content to manage your health. (Placeholder for content)")

    with tab6:
        st.header("Emergency Alerts 🚨")
        st.write("Get immediate help in case of an emergency. (Placeholder for alerts)")

    st.sidebar.title("About")
    st.sidebar.info("This virtual nurse app is developed to provide empathetic and effective healthcare management. 🌟")
