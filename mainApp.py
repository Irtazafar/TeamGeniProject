import pycountry
import streamlit as st
import openai
from streamlit_option_menu import option_menu
from datetime import datetime

# region prompts
promptChatbot = """
You are an expert healthcare professional with extensive knowledge in various health conditions and diseases. Your role is to provide accurate, evidence-based answers to the questions users ask about their health, diseases, or conditions. Respond to the user's concerns in an empathetic and supportive manner, as a caring nurse would. Use phrases like "I understand," "I'm here to help," and "That sounds difficult." Guide them on how to manage their symptoms step-by-step or provide clear answers to their questions. Always ensure your responses are factual and based on the latest medical guidelines. Here are some examples of how to structure your responses:

1. Acknowledge the user's feelings:
   - "I understand how challenging this must be for you."
   - "That sounds difficult, but I'm here to help you."

2. Provide clear, factual information:
   - "Based on current medical guidelines, it's important to..."
   - "Research shows that..."

3. Offer step-by-step guidance or answers:
   - "To manage your symptoms, you can try the following steps:..."
   - "Here are some strategies that can help:..."

4. Encourage and support the user:
   - "Remember, you're not alone in this."
   - "If you have any more questions or need further assistance, feel free to ask."

Example Interaction:
User: "I have arthritis, so can I climb a flight of stairs?"
Virtual Nurse: "I understand that dealing with arthritis can be very painful. It's important to listen to your body and not push yourself too hard. Generally, moderate physical activity can be beneficial for arthritis, but it's crucial to do it in a safe and controlled manner. Here are some tips to help you manage climbing stairs with arthritis:
1. Take your time and go at a pace that feels comfortable.
2. Use handrails for support if available.
3. If possible, try to use the stronger leg to lead when going up, and the weaker leg when going down.
4. Consider using assistive devices like a cane if needed.
Remember to consult with your healthcare provider before making any changes to your physical activity routine."

User: "I have been experiencing frequent headaches. What can I do to alleviate them?"
Virtual Nurse: "I'm sorry to hear that you're experiencing frequent headaches. I understand how disruptive they can be. Here are some steps you can take to manage and potentially reduce your headaches:
1. Stay hydrated by drinking plenty of water throughout the day.
2. Ensure you are getting enough sleep and maintaining a regular sleep schedule.
3. Try to identify and avoid potential triggers, such as certain foods, stress, or bright lights.
4. Practice relaxation techniques like deep breathing, meditation, or gentle yoga.
5. Over-the-counter pain relievers can be helpful, but make sure to use them as directed.
If your headaches persist or worsen, it's important to consult with a healthcare provider to rule out any underlying conditions."

Keep your responses clear, concise, and compassionate. Your goal is to provide the best possible care and support to the users.
"""

symptom_checker_prompt = """
You are a symptom checker chatbot designed to assist users in identifying and understanding their health symptoms. Your primary goal is to gather comprehensive information about the user's symptoms to determine whether they require immediate medical attention or if their condition can be managed at home. When a user reports any discomfort or symptom, follow these steps:

Acknowledge and Empathize:
- Begin by acknowledging the user's concern and expressing empathy, such as "I'm sorry to hear that you're experiencing discomfort."

Ask for Detailed Symptoms:
- Prompt the user to describe their symptoms in detail using open-ended questions, like "Can you please describe all the symptoms you're experiencing?"

Specific Symptom Questions:
- For each symptom reported, ask specific follow-up questions to gather more information. For instance, if the user mentions back pain, ask:
  - "Can you describe the location of the pain? Is it in the upper, middle, or lower back?"
  - "How would you rate the pain on a scale of 1 to 10?"
  - "Is the pain sharp, dull, or throbbing?"
  - "Did the pain start suddenly or gradually?"
  - "Have you experienced any recent injuries or strains?"
  - "Do you have any other symptoms like fever, numbness, or tingling?"

Assess Severity and Urgency:
- Based on the user's responses, determine the severity and urgency of the situation. For example:
  - If severe, sudden pain, numbness, or other serious symptoms are described, recommend immediate medical attention: "Based on what you've described, it’s important that you seek medical attention immediately. Please visit your nearest emergency room or contact a healthcare professional right away."
  - If symptoms are mild or manageable at home, provide appropriate home care advice: "It seems like your symptoms may be manageable at home. Here are some steps you can take to alleviate your discomfort: [provide detailed home care advice]. However, if your symptoms worsen or do not improve, please consult a healthcare professional."

Provide Clear Guidance:
- Ensure the user understands the next steps, whether it’s seeking immediate medical care or managing symptoms at home.

Encourage Follow-Up:
- Encourage the user to check back in if they have any more questions or if their symptoms change, with a reminder like "Feel free to reach out again if you have any more questions or if your symptoms change."
"""

educational_resources_prompt = """
You are a knowledgeable medical educator. Please provide a list of educational topics that would be beneficial for users to learn about. Include a variety of topics such as common diseases, anatomy and physiology, nutrition, healthy eating, mental health, fitness, and preventive healthcare. For each topic, provide a detailed explanation that can be displayed under each topic tab in a user-friendly web application.
"""

emergency_numbers_prompt = """
You are an expert in global emergency services. Please provide the emergency phone numbers for police, fire, and ambulance services in the following country: {}.
"""


# endregion

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
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 8px;
        background-color: #fff;
        margin-bottom: 20px;
    }
    .user-message {
        background-color: #e1f5fe;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        text-align: right;
    }
    .bot-message {
        background-color: #f1f8e9;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables for authentication, API key, and conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'symptom_conversation' not in st.session_state:
    st.session_state.symptom_conversation = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'medication_reminders' not in st.session_state:
    st.session_state.medication_reminders = []
if 'appointment_reminders' not in st.session_state:
    st.session_state.appointment_reminders = []
if 'educational_topics' not in st.session_state:
    st.session_state.educational_topics = []

# Sidebar for API key input and navigation
with st.sidebar:
    st.sidebar.header("API Key Configuration")
    api_key_input = st.text_input("Enter your OpenAI API Key", value=st.session_state.api_key, type="password")
    if st.button("Save API Key"):
        st.session_state.api_key = api_key_input
        st.success("API Key saved!")

    option = option_menu(None, ["🏠 Home", "🩺 Symptom Checker", "⏰ Reminders", "📈 Health Monitoring",
                                "📚 Educational Resources", "🚨 Emergency Alerts"],
                         icons=["icon", "icon", "icon", "icon", "icon", "icon"],
                         menu_icon="cast", default_index=0, orientation="vertical")
client = openai.OpenAI(
    api_key=st.session_state.api_key,
    base_url="https://api.aimlapi.com",
)

# Function to handle OpenAI API interaction
def ask_openai(messages, role="virtual_nurse"):
    chat_prompt = promptChatbot if role == "virtual_nurse" else symptom_checker_prompt
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": chat_prompt}] + messages,
        temperature=0.7,
        max_tokens=640,
    )

    response = chat_completion.choices[0].message.content
    return response


def get_educational_topics():
    prompt = [{"role": "system", "content": educational_resources_prompt}]
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=0.7,
        max_tokens=1000,
    )
    response = chat_completion.choices[0].message.content
    topics = response.split("\n\n")
    return topics

def get_emergency_numbers(country):
    prompt = [{"role": "system", "content": emergency_numbers_prompt.format(country)}]
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=0.7,
        max_tokens=1000,
    )
    response = chat_completion.choices[0].message.content
    return response



# Home page interaction with virtual nurse
if option == "🏠 Home":
    st.header("Chat with Your Nurse Serena 💬")
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.conversation:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Input bar at the bottom
    with st.form(key='input_form', clear_on_submit=True):
        user_input = st.text_input("You: ", "")
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        st.session_state.conversation.append({"role": "user", "content": user_input})
        with st.spinner('Fetching response...'):
            response = ask_openai(st.session_state.conversation)
        st.session_state.conversation.append({"role": "assistant", "content": response})
        st.experimental_rerun()

# Symptom Checker and Triage
elif option == "🩺 Symptom Checker":
    st.header("Symptom Checker 🩺")
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.symptom_conversation:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Input bar at the bottom
    with st.form(key='symptom_input_form', clear_on_submit=True):
        symptoms_input = st.text_input("Describe your symptoms:", "")
        submit_button = st.form_submit_button(label='Send')

    if submit_button and symptoms_input:
        st.session_state.symptom_conversation.append({"role": "user", "content": symptoms_input})
        with st.spinner('Fetching response...'):
            response = ask_openai(st.session_state.symptom_conversation, role="symptom_checker")
        st.session_state.symptom_conversation.append({"role": "assistant", "content": response})
        st.experimental_rerun()

# Medication and Appointment Reminders
elif option == "⏰ Reminders":
    st.header("Reminders ⏰")
    reminder_type = st.selectbox("Reminder Type", ["Medication 💊", "Appointment 🗓️"])
    if reminder_type == "Medication 💊":
        med_name = st.text_input("Medication Name")
        dosage = st.text_input("Dosage")
        reminder_date = st.date_input("Reminder Date")
        reminder_time = st.time_input("Reminder Time")
        if st.button("Set Reminder"):
            reminder_datetime = datetime.combine(reminder_date, reminder_time)
            st.session_state.medication_reminders.append(
                {"name": med_name, "dosage": dosage, "datetime": reminder_datetime})
            st.success(f"Reminder set for {med_name} at {reminder_datetime}.")
    else:
        appointment_details = st.text_input("Appointment Details")
        appointment_date = st.date_input("Appointment Date")
        appointment_time = st.time_input("Appointment Time")
        if st.button("Set Reminder"):
            appointment_datetime = datetime.combine(appointment_date, appointment_time)
            st.session_state.appointment_reminders.append(
                {"details": appointment_details, "datetime": appointment_datetime})
            st.success(f"Reminder set for appointment at {appointment_datetime}.")

    st.header("Upcoming Reminders")
    st.subheader("Medications")
    for reminder in st.session_state.medication_reminders:
        st.write(
            f"{reminder['datetime'].strftime('%A, %B %d, %Y at %I:%M %p')}: Take {reminder['dosage']} of {reminder['name']}")

    st.subheader("Appointments")
    for reminder in st.session_state.appointment_reminders:
        st.write(f"{reminder['datetime'].strftime('%A, %B %d, %Y at %I:%M %p')}: {reminder['details']}")

# Health Monitoring and Data Logging
elif option == "📈 Health Monitoring":
    st.header("Health Monitoring 📈")
    st.write("Connect your wearable device to monitor your health in real-time. (Placeholder for integration)")

# Educational Resources
elif option == "📚 Educational Resources":
    st.header("Educational Resources 📚")

    # Refresh button
    if st.button('Refresh Topics'):
        with st.spinner('Fetching educational topics...'):
            st.session_state.educational_topics = get_educational_topics()

    # Fetch educational topics if not already done
    if not st.session_state.educational_topics:
        with st.spinner('Fetching educational topics...'):
            st.session_state.educational_topics = get_educational_topics()

    # Display educational topics in tabs
    topics = st.session_state.educational_topics
    if topics:
        tabs = st.tabs([topic["title"] for topic in topics])
        for tab, topic in zip(tabs, topics):
            with tab:
                st.markdown(f"### {topic['title']}\n\n{topic['content']}")

# Emergency Alerts
elif option == "🚨 Emergency Alerts":
    st.header("Emergency Alerts 🚨")

    countries = [country.name for country in pycountry.countries]
    selected_country = st.selectbox("Select a country", countries)

    if st.button("Get Emergency Numbers"):
        with st.spinner('Fetching emergency numbers...'):
            emergency_numbers = get_emergency_numbers(selected_country)
        st.markdown(f"### Emergency Numbers for {selected_country}\n\n{emergency_numbers}")


st.sidebar.title("About")
st.sidebar.info("This virtual nurse app is developed to provide empathetic and effective healthcare management. 🌟")